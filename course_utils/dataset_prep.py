# coding: utf-8

import json
from random import sample
from itertools import tee, filterfalse
import click

COURSE_META = 'courseSectionDTO'
COURSE_KEYS = ['department', 'course', 'section', 'instructor', 'termName']
TEXT_META = 'courseMaterialResultsList'
TEXT_KEYS = ['title', 'edition', 'author', 'isbn', 'materialType', 'requirementType', 'copyRightYear', 'publisher']
PRINT_INVENTORY = 'printItemDTOs'
E_INVENTORY = 'digitalItemDTOs'
INVENTORY_KEYS = ['typeCondition', 'priceDisplay', 'binding',]

def extract_print_inventory(course_dict):
    for record in course_dict.get(PRINT_INVENTORY, {}).values():
        yield dict([(k, course_dict.get(k)) for k in TEXT_KEYS] + [(k, record[k]) for k in INVENTORY_KEYS if record.get(k)] + [('item_type', 'print')])

def extract_e_inventory(course_dict):
    for record in course_dict.get(E_INVENTORY, []):
        yield dict([(k, course_dict.get(k)) for k in TEXT_KEYS] + [(k, record[k]) for k in INVENTORY_KEYS if record.get(k)] + [('item_type', 'digital')])

def extract_data(bkst_data):
    cleaned_data = []
    for course in bkst_data:
        course_dict = {k: course[COURSE_META][0].get(k) for k in COURSE_KEYS}
        course_dict['texts'] = []
        for text in course[COURSE_META][0].get(TEXT_META, []):
            for i in extract_print_inventory(text):
                course_dict['texts'].append(i)
            for i in extract_e_inventory(text):
                course_dict['texts'].append(i)
        cleaned_data.append(course_dict)
    return cleaned_data


def dedupe_courses(data):
    courses_seen = []
    for course in data:
        course_key = " ".join([course[k] for k in COURSE_KEYS if course[k]])
        if not course_key in courses_seen:
            courses_seen.append(course_key)
            yield course

def partition(pred, iterable):
    """Partition entries into false entries and true entries.

    If *pred* is slow, consider wrapping it with functools.lru_cache().
    """
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return list(filterfalse(pred, t1)), list(filter(pred, t2))


def reshuffle_data(data, key, factor=2):
    # weighted shuffle: ensures that elements with the key are distributed more toward the beginning of the dataset
    # factor is the proportion of elements with the key to weight, i.e., 2 = 1/2
    without, with_key = partition(lambda x: x.get(key), data)
    n = len(with_key) // factor
    front_list = with_key[:n] + without[:n]
    back_list = with_key[n:] + without[n:]
    return sample(front_list, k=len(front_list)) + sample(back_list, k=len(back_list))
    
@click.command()
@click.option('--infile', default='../data/bookstore-data.json')
@click.option('--outfile', default='../textbook/static-assets/data/bookstore-data.json')
def main(infile, outfile):
    with open(infile) as f:
        bkst_data = json.load(f)
    cleaned_data = extract_data(bkst_data)
    
    if len({" ".join([course[k] for k in COURSE_KEYS if course[k]]) for course in cleaned_data}) == len(cleaned_data):
        cleaned_data = [c for c in dedupe_courses(cleaned_data)]
    
    with open(outfile, 'w') as f:
        json.dump(reshuffle_data(cleaned_data, 'texts'), f, indent=4)





