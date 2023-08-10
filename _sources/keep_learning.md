# Python Resources & Where to Go from Here

There are many ways to sustain and deepen your engagement with programming and the Python language beyond Python Camp. We've included examples in various media below to suit a range of learning styles. For information on options for running Python on your own, see [](python-environments) below.

One of the best ways to leep learning is to find practical uses for Python (or programming more generally) in your daily life.

The following are just some of the many things you can do with Python. (The links provided are merely examples and not meant to be exhaustive).

- Automate workflows involving files, directories, etc., on your computer;
- Perform data/statistical [analysis](https://pandas.pydata.org/), [machine learning](https://scikit-learn.org/stable/), and [data visualization](https://matplotlib.org/);
- Create a [website](https://flask.palletsprojects.com/en/2.3.x/);
- Collect data from Internet sources, either by using API's or scraping web pages;
- Use [natural-language processing tools](https://spacy.io/) to analyze large amounts of text;
- Experiment with [large-language models](https://python.langchain.com/docs/get_started/introduction.html) and other forms of AI;
- Create [a game](https://www.pygame.org/wiki/about);
- Edit audio or [video](https://github.com/Zulko/moviepy).

It's hard to learn a programming language without practice, and it can be hard to practice without a context and a goal. If you don't find yourself in a context where you can work alongside others toward shared goals (e.g., a school assignment, a research project, a job), a good approach is to set a concrete, manageable goal for yourself: something you can achieve within a limited amount of time. 

For instance, if you're new to programming and have just completed Python Camp, "building an AI chatbot from scratch" might be a bit too ambitious. Ask yourself, How can I scale it down to my capacity? Maybe you can implement a Python chatbot built by someone else. (One of the advantages of Python is its popularity and the openness of its ecosystem: if you can think of a programming project, there's a good chance someone has tried it in Python and has shared the fruits of their efforts.) To stay with our example, once you get this chatbot working for yourself, maybe you can tweak the code to do something different. And as you progress, a great way to plug into a collaborative context is to contribute to open source projects: maybe the chatbot developer is accepting contributions to the codebase on GitHub, etc. 

Whatever path you take, may your journey be rewarding, and may it lead you where you had not expected! 

## Resources

### Books

Current GW students, faculty, and staff have access to the [Safari Tech Books/O'Reilly Library](https://go.oreilly.com/gwu-edu), which includes a vast collection of online books by major publishers on programming languages and related topics. These include titles from O'Reilly's own series, which are generally well regarded and often considered authoritative texts on a given topic.

There is no shortage of books on Python for beginners, but here are a few to consider:

- [Learning Python](https://learning.oreilly.com/library/view/learning-python-5th/9781449355722/) by Mark Lutz (5th ed.). A classic -- what many a Python developer has cut their teeth on.
- [Automate the Boring Stuff with Python](https://learning.oreilly.com/library/view/automate-the-boring/9781098122584/) by Al Sweigart (2nd ed.). Focused on concrete, practical applications at the right scale for beginners. Also available [for free](https://automatetheboringstuff.com/)
- [Python Cookbook](https://learning.oreilly.com/library/view/python-cookbook-3rd/9781449357337/) by David Beazley and Brian K. Jones (3rd ed.). More of a reference book, but very useful as you progress from a grasp of the basic syntax to an understanding of the most common programming patterns. There are usually many ways to do the same thing in Python, but this book can help you identify a concise, efficient, and safe way.
- [Python Crash Course](https://learning.oreilly.com/library/view/python-crash-course/9781098156664/) by Eric Matthes (3rd ed.) A popular book for beginners that shows up on many "Best Of" lists.
- [Head First Python](https://learning.oreilly.com/library/view/head-first-python/9781492051282/) by Paul Barry (3rd ed.). Departs from the usual exposition- and code-heavy style of most programming books with ample use of visuals and other techniques intended to make learning easier.

Additionally, there are some great open-source books available. 

- [Introduction to Cultural Analytics & Python](https://melaniewalsh.github.io/Intro-Cultural-Analytics/welcome.html) by Melanie Walsh. This book teaches Python from the perspective of working with data in the humanities and social sciences, and it includes executable Jupyter notebooks. (The textbook for Python Camp takes a lot of inspiration from Walsh's book.)
- [Think Python](https://greenteapress.com/wp/think-python-2e/) by Allen B. Downey (2nd ed.). Available in both PDF and HTML format. 


### Multimedia 

- Current GW students, faculty, and staff have access to [LinkedIn Learning](http://go.gwu.edu/linkedinlearning), which has an extensive library of video content about Python. The videos are well produced, modular, and accompanied by exercises and supplemental materials. Check out [Python Essentials](https://www.linkedin.com/learning/python-essential-training-18764650) for an engaging place to start.
- [Python for Everybody](https://www.py4e.com/) is a free Python course developed by Charles Severance. The site includes lecture videos, exercises, and an accompanying textbook.
- [Get Data off the Ground with Python](https://openedx.seas.gwu.edu/courses/course-v1:GW+EngComp1+2018/about) by Lorena Barba is a free online Python course developed at GW. The course is designed for engineering students but might be useful for anyone who wants to learn Python for data analysis. Dr. Barbra's course includes video lectures, self-paced exercises, and autograded content. (The first iteration of Python Camp was based closely on Dr. Barba's curriculum.)

### Python for Research

The [Data Carpentry](https://datacarpentry.org/lessons/) curriculum makes available a range of material for learning about programming in the context of specific academic disciplines. Not all of the lessons focus on Python, but many do, and they are typically geared toward beginners. If you are wondering how Python might prove useful to your research, you might find some relevant examples here.

(python-environments)=
## Python Environments

As a participant in Python Camp, you've been using a hosted JupyterHub environment provided by GW Libraries and Academic Innovation. As you continue your Python journey, you'll probably want a coding environment that provides more flexibility and/or computing power. 

The following are good options, depending on your use case.

### Local Python/Jupyter Installation

If you like the notebook format we've used in Python Camp, you can install the same environment locally on your own computer. The [Anaconda distribution](https://www.anaconda.com/) of Python is free for download, very popular, and comes with the Jupyter Notebook application. On Mac or Windows, just download and install, and then launch the [Navigator](https://docs.anaconda.com/free/navigator/) to open the Notebook interface. 

In addition, the Anaconda distribution comes with wide variety of Python libraries useful for data analysis and visualization. 

### Local Python with IDE

An integrated development environment (IDE) is a popular choice for those who are writing larger scripts or applications in Python. Most IDE's do _not_ use the notebook format by default, so instead of creating a document that contains both Python code and a record of its output (a `.ipynb` file), the IDE user creates a file of just Python code (a `.py` file), which can then be run as a standalone script. 

However, some IDE's now support `.ipynb` files as well, providing similar functionality to a Jupyter Notebook. 

There are several freely available IDE's for use with Python. Microsoft's Visual Studio Code ([VS Code](https://code.visualstudio.com/)) offers a relatively intuitive interface, along with powerful tools for syntax checking, debugging, and more.

### Python Notebooks in the Cloud

If you prefer to work in the cloud, there are a few free options that provide a notebook-style interface alongside other functionality.

- [Google Colab](https://colab.research.google.com/) offers a robust Python environment along with integration with Google Drive. Colab works well for projects involving data sources available on the web or smaller data files that can be uploaded to Drive, but it's not ideal for larger datasets that can't be shared. On the upside, it does offer free access to a GPU (graphics processing unit) for more intensive numeric computation (such as you might undertake in machine learning or deep learning projects). Particularly if your computer is not very powerful, Colab can be a good alternative to doing such computation locally.

- [Kaggle](https://www.kaggle.com) aims to serve as an online community for AI and machine-learning development. In addition to datasets, courses, and coding competitions, it offers free access to Python and other languages in a notebook environment. 

- A relatively new service, [Deepnote](https://deepnote.com) provides cloud-hosted Python notebooks in a sleek interface. At the free tier, the functionality seems similar to Google Colab. (Paid options include the ability to integrate with external storage services and databases.)