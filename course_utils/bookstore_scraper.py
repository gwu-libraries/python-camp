import json
import re
from collections import defaultdict
from datetime import datetime
from time import sleep
import httpx
from bs4 import BeautifulSoup
from scraping_config import course_config, bkstr_config, bkstr_headers
import logging
import click
from tqdm import tqdm
from pathlib import Path

logging.basicConfig()
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PATH_TO_DATA = Path(__file__).parents[1] / 'data'

class CourseSchedScraper:

    def __init__(self, config):
        '''
        config object should contain URL's and parameters for the GW Schedule of Classes website
        '''
        self.base_url = config['schedule_page_url']
        self.params = {'campid': config['campus_id'],
                        'termid': config['term_id']} 
        self.course_url = config['course_page_url']


    def get_depts(self):
        '''
        Scrapes the GW Schedule of Classes to retrieve a list of departments for the term and campus specified in the configuration file
        '''
        logger.info(f'Retrieving department codes for campus ID {self.params["campid"]}, term ID {self.params["termid"]}.')
        self.dept_page = httpx.get(self.base_url, params=self.params)
        try:
            self.dept_page.raise_for_status()
            soup = BeautifulSoup(self.dept_page.text, features="html.parser")
            # Extract links to department pages
            dept_links = soup.find_all("a", href=re.compile(r'.+&subjId=.+'))
            # Extract department codes from links
            self.dept_codes = [d['href'].split('&subjId=')[-1] for d in dept_links]
            return self
        except httpx._exceptions.HTTPStatusError as e:
            logging.error('Failed to load list of departments.')
            logging.error(self.dept_page.text)
            raise e
    
    def get_course_pages(self):
        '''
        Retrieves the first page of course listings for each department
        '''
        self.course_pages = defaultdict(list)
        logger.info('Retrieving course listings for departments.')
        for code in tqdm(self.dept_codes):
            self.params['subjid'] = code
            page = httpx.post(self.course_url, params=self.params)
            try:
                page.raise_for_status()
                self.course_pages[code].append(page.text)
            except httpx._exceptions.HTTPStatusError as e:
                logging.error(f'Failed to load list of courses for dept {code}.')
                logging.error(page.text)
                raise e
        return self

    def get_more_results(self, soup, course_code):
        '''
        Retrieves additional pages of course results for a given department (course code)
        '''
        pages = {t.text for t in soup.find_all('a', href=re.compile('javascript:goToPage')) if t.text != '1'}
        if pages:
            for page in pages:
                self.params['subjid'] = course_code
                response = httpx.post(self.course_url, 
                                params=self.params, 
                                headers={'Content-Type': 'application/x-www-form-urlencoded'}, 
                                data=f"pageNum={page}")
                try:
                    response.raise_for_status()
                    yield response.text   
                except httpx._exceptions.HTTPStatusError as e:
                    logging.error(f'Failed to load page {page} of courses for dept {course_code}.')
                    logging.error(response.text)
                    raise e 
    
    def extract_course_info(self, course_soup, course_code):
        '''
        Extracts the courses metadata from a page of course listings
        '''
        listings = course_soup.find_all('tr', class_="crseRow1")
        for listing in listings:
            course = {'code': course_code}
            info = listing.find_all('td')
            # Course number should reside under the 3rd table element, in the <a> tag
            course['number'] = info[2].a.text.strip()
            # Course section is in the fourth element
            course['section'] = info[3].text.strip()
            # Title and instructor are in the fifth and seventh elements
            course['title'] = info[4].text.strip()
            course['instructor'] = info[6].text.strip()
            yield course

    def build_course_list(self):
        '''
        From a list of department pages, extract courses metadata and get additional results as necessary
        '''
        logger.info('Extracting courses metadata from course listings.')
        self.courses = []
        for course_code, pages in tqdm(self.course_pages.items()):
            soup = BeautifulSoup(pages[0], features="html.parser")
            self.courses.extend([course for course in self.extract_course_info(soup, course_code)])
            more_pages = list(self.get_more_results(soup, course_code))
            if more_pages:
                self.courses.extend([course for page in more_pages
                       for course in self.extract_course_info(BeautifulSoup(page, features="html.parser"), course_code)])
        return self
    
    def scrape_schedule(self):
        '''
        Main method
        '''
        self.get_depts()
        self.get_course_pages()
        self.build_course_list()
        return self

    def save_course_list(self, json_file):
        '''
        Save courses list as JSON (list of dicts)
        '''
        logger.info(f'Saving course metadata to {json_file}.')
        with open(json_file, 'w') as f:
            json.dump(self.courses, f)
        return self

class CaptchaError(Exception):
    '''
    Raised when a captcha is encountered to prevent continued pings against the server
    '''
    pass

class BookstoreScraper:

    def __init__(self, bkstr_config, file_prefix, data_dir):
        '''
        :param bkstr_config: should contain a base_url; values for storeId, langId, catalogId, and requestType; and a json_data dictionary that contains the keys/values for the term and course
        :param file_prefix: prefix for the file to store data from this run
        :param data_dir: path to directory for storing results. Assumes file names begin with the same prefix and conclude with a timestamp in ISO format.
        '''
        self.base_url = bkstr_config['base_url']
        self.params = bkstr_config['params']
        self.json_data = bkstr_config['json_data']
        self.file_prefix = file_prefix
        self.data_dir = Path(data_dir)

    def load_previous(self, course_file_prefix):
        '''
        Loads previously scraped data from the path provided to the init method. Assumes files share the same prefix and end in a timestamp. Also loads course data from the same directory.
        '''
        def get_latest(data_dir, file_prefix):
            previous_files = list(Path(data_dir).glob(f'{file_prefix}*.json'))
            # Sort by timestamp
            if not previous_files:
                return []
            else:
                latest_file = sorted(previous_files)[-1]
                print(latest_file)
                with open(latest_file) as f:
                    return json.load(f)
        self.data = get_latest(self.data_dir, self.file_prefix)
        if self.data:
            logger.info(f'Found {len(self.data)} records.')
        self.courses = get_latest(self.data_dir, course_file_prefix)
        return self

    
    def update_json(self, course):
        '''
        Updates the JSON payload for the bookstore request with course metadata
        '''
        self.json_data['courses'][0].update({'courseDisplayName': course['number'],
                                'departmentDisplayName': course['code'],
                                'divisionDisplayName': '',
                                'sectionDisplayName': course['section'],
                                'courseRefId': ''})
        return self
    
    def fetch_data(self, headers):
        '''
        :param headers: should be a dict of request headers, mimicking those of a specific browser
        '''
        response = response = httpx.post(self.base_url,
                                params=self.params,
                                headers=headers,
                                json=self.json_data)
        try:
            resp_data = response.json()
            if 'blockScript' in resp_data:
                raise CaptchaError
            return resp_data
        except Exception as e:
            logger.error('Error encountered; saving results before exiting.')
            self.cleanup()
            logger.error(response.text)
            raise e
    

    def filter_courses(self, courses):
        '''
        Filter the list of courses against the bookstore data previously acquired, skipping courses that have already been retrieved. 
        :param courses: list of dicts, containing keys "code," "number," and "section"
        '''
        def extract_course_info(bkstr_rec):
            '''
            Extracts department, code, and section info from a single bookstore course record
            '''
            # Assumes this element is a list of one element
            course_info = bkstr_rec['courseSectionDTO'][0]
            return course_info['department'], course_info['course'], course_info['section']
        
        new_courses = []
        # Build set of tuples from previous bookstore data
        bkstr_index = {extract_course_info(d) for d in self.data}
        for course in courses:
            if (course['code'], course['number'], course['section']) not in bkstr_index:
                new_courses.append(course)
                # Add to index to prevent duplication 
                bkstr_index.add((course['code'], course['number'], course['section']))
        return new_courses

    def run_scraper(self, headers):
        self.new_data = []
        courses = self.filter_courses(self.courses)
        logger.info(f'Fetching textbook data for {len(courses)} courses.')
        with tqdm(total=len(courses)) as progress:
            while courses:
                course = courses[0]
                self.update_json(course)
                self.new_data.extend(self.fetch_data(headers))
                courses.pop(0)
                sleep(5)
                progress.update(1)
        self.cleanup()
        return self
    
    def cleanup(self):
        '''
        Saves data to disk before exiting
        '''
        if self.new_data:
            self.data.extend(self.new_data)
            with open(self.data_dir / f'{self.file_prefix}-{datetime.now().isoformat()}.json', 'w') as f:
                json.dump(self.data, f)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--json-file', default=PATH_TO_DATA / f'gw-courses-main-{datetime.now().isoformat()}.json')
def scrape_sched(json_file):
    scraper = CourseSchedScraper(course_config)
    scraper.scrape_schedule().save_course_list(json_file)

@cli.command()
@click.option('--file-prefix', default='gw-books-mc-202302')
@click.option('--data-dir', default=PATH_TO_DATA)
@click.option('--course-file-prefix', default='gw-courses-main')
@click.option('--browser', default='firefox')
def scrape_books(file_prefix, data_dir, course_file_prefix, browser):
    book_scraper = BookstoreScraper(bkstr_config, file_prefix, data_dir)
    book_scraper.load_previous(course_file_prefix)
    book_scraper.run_scraper(headers=bkstr_headers.get(browser))
    

if __name__ == '__main__':
    cli()