# Glossary

```{glossary}
append
    The `append()` method adds an element to the end of a {term}`list`. 

    For instance, if the {term}`variable` `my_list` is defined as `[1, 2, 3]`, after we run the code `my_list.append(4)` once, `my_list` will be equal to `[1, 2, 3, 4]`.

arguments

    The arguments to a {term}`function` are {term}`variable`s defined as part of the function itself. In a {term}`function definition`, the arguments appear between the {term}`parentheses` following the function name. Arguments may be optional or required. In the following example, the function `my_func` is defined to take one argument, `x`, to which the function adds 5. When we call `my_func`, we provide a value between parentheses, which is assigned to the variable `x` within the function.

        def my_func(x):     # defining my_func with one required argument, x
            return x + 5    # Adds 5 to the value of x and returns it
        
        print(my_func(10))  # calling my_func --> prints 15

assert statement

    Python code, using the `assert` keyword, that performs a logical test. Like an {term}`if statement`, an assert statement evaluates the code that follows it as a `Boolean expression`. However, instead of taking some action if the expression evaluates as `True`, the assert statement raises an `AssertionError` if the statement is `False`. (The assert statement does nothing if the expression evaluates as `True`). 

    Assert statements are used primarily for debugging purposes; they are useful for testing certain normal or minimal conditions that your code should handle without error. (In that way, if you subsequently change your code in such a way that it no longer satisfies one of those conditions, the assert statement will let you know.)

attributes

    An attribute is like a {term}`variable` except that it belongs to the {term}`instance` of a Python {term}`class` or {term}`type`. An attribute may refer to a value, or it may be the name of a function, in which case it is called a {term}`method`. For instance `append()` is a method that belongs to instances of the `list` type, an instance of which is automatically created in Python whenever you assign a variable to values enclosed in {term}`square brackets`. Hence we can write `my_list = [1, 2, 3]`, and `my_list` will, by definition, have access to the `append()` method. 

    Because the variable `my_list` has the attribute (method) `append`, we can access the attribute with {term}`dot notation`: `my_list.append()`.

    In defining custom classes, attributes provide a way to associate data with behaviors. For instance, if I am writing a program to keep track of students' grades, I could define a `Student` class, instances of which would have attributes to store information specific to each student, such as name, degree, test scores, etc. 

    Code to define such a class might look like the following:

        class Student:

            def __init__(self, name, degree):           # __init__ method; called when creating an instance of Student
                self.name = name                        # the variable self refers to the instance of Student being created
                self.degree = degree                    # self.name is how we refer to an attribute in the definition of a class
                self.scores = []                        # initializing self.scores to an empty list, assuming we haven't recorded any yet
    
    Then I can create an instance of the `Student` class with the specified attributes:

        student1 = Student('Dolsy Smith', 'MSI')        # Creating an instance; the arguments to `Student()` are used by the `__init__` method.
        print(student1.name)                            # Accessing the `name` attribute -> prints 'Dolsy Smith'

block

    A chunk of Python code separated from the surrounding code by being indented. Blocks are required in the following situations (and in others that we have not seen in Python Camp):
        - in a {term}'function definition`
        - in a {term}`for loop`
        - in an {term}`if statement`
        - in the definition of a Python {term}`class`
    
    Lines of code in the block are executed together. Thus, the block of code in a `for` loop is executed as many times as specified by the loop, while the block of code underneath an `if` statement is executed only if the {term}`Boolean expression` in the `if` statement evaluates to `True`. 

    Blocks can also be nested, in which case, the amount of indentation determines which code belongs to which block. The code below contains three blocks, each nested inside the other.

    ```{image} ./img/nested-blocks.png
    :alt: A diagram of nested blocks in Python
    :width: 500px
    :align: center
    ```

    When run, the code prints `[25.5, 100.99, 50.75]`.

    Ihe convention is to use four spaces (or a tab set to four spaces) as the basic unit of indentation (We say "the basic unit," because when creating nested code blocks, each level of indentation will correspond to one or more instances of the basic unit.)
    
Boolean expression

    Python code that evaluates as either `True` or `False`. Boolean expressions are commonly used inside {term}`if statement`s to create actions that will occur only if certain conditions are met. 

    Boolean expressions will often contain the double equals sign (`==`), which evaluates as `True` if the values/variables on either side of the double equals are considered equivalent. 

    For instance, if the variable `x` is defined as the integer 3, then `x == 3` will evaluate to `True`. 


Boolean operator

    A Python {term}`keyword` used primarily in {term}`if statement`s (see also {term}`Boolean expression`) to evaluate one or more {term}`Boolean value`s (or Python expressions evaluated as Boolean values). For instance, the following block of code prints the phrase "That's me!" only if both expressions in parentheses are `True`:

        if (first_name == 'Dolsy') and (last_name == 'Smith'):
            print("That's me!")

    The Boolean operators in Python are `and`, `or`, and `not`. The following table summarizes their use:

    | Operator | Number of Terms | Evaluates as `True` |
    | -------- | --------------- | ------------------  |
    | and      | 2               | Only if both terms are `True` |
    | or       | 2               | If at least one term is `True`|
    | not      | 1               | If the term is `False` |  

Boolean value

    A special Python {term}`type` used primarily in {term}`Boolean expression`s. There are only two Boolean values: `True` and `False`. But any other Python value can be treated as a Boolean if used inside a Boolean expression. For instance, if `x` is an integer, the following code will divide 2 by `x` unless `x` is 0. (All integers in Python evaluate as `True` except for 0, which evaluates as `False`.)

        if x:
            print(2/x) 

call

    To call a method or function is to instruct Python to execute the function or method's predefined behavior. And a function or method is really just a kind of shortcut: instead of our having to type out the same code whenever we want to perform a certain task (like splitting a string, for instance), we call the function or method in which that behavior has been defined. It's sort of like using the address book on your phone: you can tap `Mom` in order to call or text Mom, instead of having to enter her number every time.

character

    A character is the basic unit of a Python {term}`string`. In Python, characters are defined according to the [Unicode standard](https://home.unicode.org/) by default. Unicode characters comprise the following (and more):
        - Letters of most written alphabets
        - Arabic numerals
        - Punctuation marks
        - Emojis
        - Non-alphabetic scripts (such as Chinese, Japanese kanji, etc.)
        - Common symbols and special characters

    In Python, characters are relevant mostly because we can divide strings into their constituent characters. For instance, if `my_str` is defined as the string `Python Camp`, we can extract the first `P` (the first character) by writing `my_str[0]`.

class

    A Python class is a custom Python data {term}`type`. Classes can have {term}`attributes` and {term}`method`s: that is, associated data and behaviors. 

    Classes allow programmers to model aspects of the real-world in more flexible ways than with the built-in Python types. 

    Classes are defined by writing the {term}`keyword` `class` followed by a name, followed by a colon. The body of the class (an indented {term}`block`) usually contains one or more methods. The special `__init__` method is called when {term}`instance`s of the class are created. 

    You might think of a class as blueprint or template that specifies how data should be stored in memory. If we have a dataset of books, and we want to make sure that for every book, we capture its title, we could create a `Book` class with a required `title` attribute. Then we would be unable to create a new instance of `Book` without providing a title. 

    This templating is more powerful than what is provided by a Python {term}`dictionary`. A dictionary has keys that are associated with values, but there is no easy way to make a given key **required** for any instance of a dictionary. 

collection

    The term **collection** refers to a Python {term}`type` that we use to associate multiple, discrete units of data. An {term}`integer` is not a collection, but a {term}`string`, a {term}`list`, and a {term}`dictionary` are all examples of collections. The following table shows the kind of data we can store in each of these collections, and how the data are associated in memory:

    | Type | Unit of Data | How Stored in Memory |
    | ---- | ------------ | -------------------- |
    | String | Unicode character | Sequentially |
    | List | Any Python type | Sequentially |
    | Dictionary | Keys: numbers or strings; Values: any Python type | Values stored by keys |

colon

    A colon (`:`) is used in Python in three ways:
      1. To signal the start of a code {term}`block`, as in a {term}`for loop`, {term}`if statement`, or {term}`function definition`.
      2. To separate the starting and ending positions in the {term}`slice` of a list or string.
      3. To separate {term}`key`s and {term}`value`s in defining a {term}`dictionary`.

comma

    Commas (`,`) are primarily used in Python in the following ways:
        1. To separate items in the definition of a {term}`list` or {term}`dictionary`.
        2. To separate the {term}`arguments` in a {term}`function definition` or {term}`function call`.

comment

    A line in code not meant to be executed by Python. You can create a comment in one of two ways:
      - By prefixing the line with the hash symbol (`#`)
      - By writing the comment between sets of three quotation marks (`'''`). This approach is useful for comments that span multiple lines.

    We use comments to document our code for ourselves and for others.

conditional logic

    A general term for the set of operations that allow computers to behave differently based on different inputs or conditions. At the most fundamental level, all other mathematical operations in a computer (addition, multiplication, etc.) are implemented using combinations of {term}`Boolean operator`s implemented in electronic circuits. 

    In higher-level languages like Python, when we speak of conditional logic, we're often referring to {term}`if statement`s. 

curly braces

    Curly braces (`{}`) are used when defining a Python {term}`dictionary`. 

dictionary

    A Python {term}`type` that stores data in memory by associating {term}`key`s with {term}`value`s, much in the way terms and definitions are associated in a glossary like this one.

    Dictionaries are defined by enclosing pairs of keys and values inside {term}`curly braces`, as in the following example:

        my_info = {'name': 'Dolsy Smith, 'job_title': 'Librarian'}
    
    To access items in a dictionary, we provide a key inside {term}`square brackets`:

        print(my_info['job_title'])     # Prints "Librarian"

documentation

    Human-readable text that explains how a program or a part of a program is intended to work and/or the rationale for a particular choice made by the programmer. Some documentation resides in separate files from the program itself; an example of this kind of documentation is found on Python docs [website](https://docs.python.org/3/). Other documentation is mixed in with the program code. Such documentation is usually offset by particular characters that tell the computer running this code to ignore the documentation itself. In Python, to include documentation within our code we either prefix a line with a hashtag (`#`) or enclose multiple lines within triple quotes (`'''`).

dot notation

    When an {term}`instance` of a Python {term}`type` (or {term}`class`) has {term}`attributes` or {term}`method`s, we use dot notation to access the attributes/methods. For instance, a {term}`list` has an `append()` method, so for a given list `my_list`, we can write `my_list.append(3)` (to add the integer `3` to the end of the list).

exception

    An error message in Python arising from a problem in the logic of the code or its inputs. As opposed to a syntax error, which will always cause code to fail, an exception is Python's way of saying, "this code might run, EXCEPT not in this case." 

double equals sign

    Two equals-sign symbols together (`==`) are used in `Boolean expression`s to test for equivalence between two variables or values.

    It's important not to confuse the double equals sign with the single equals sign (`=`), which is used to assign values in creating {term}`variable`s.

    Here's a way to remember the difference: **one** equals sign **makes** two things equal, while **two** equals signs **tests** for equality. 

        x = 5           # "Make the variable x equal to 5"
        x == 5          # "Is the variable x equal to 5?" -- in this case, evaluates to `True`

float

    A Python {term}`type` for storing numbers with decimal components, e.g., `10.5`, `3.14159265359`, etc. Unlike some programming languages, Python handles the conversion between floats and {term}`integer`s automatically, so writing `x = 10 + .5` will assign `x` to `10.5`. 

for loop

    A structure for doing iteration, i.e., repeating one or more actions a certain number of times. In Python, `for` loops are designed to be easy to use with {term}`collection` data {term}`type`s, such as dictionaries and lists. The following `for` loop will print each element of the `book_prices` list in order:

        book_prices = [22.99, 11.50, 50.50, 120.25]
        for price in book_prices:                       # The price variable takes on each value from book_prices in order
            print(price)

function

    A Python structure for storing code that can be executed at a later time (any number of times). We create functions by writing a {term}`function definition`, and we use functions by writing a {term}`function call`. 

    Many Python commands are built-in functions, like `print()`, `len()`, `type()`. `int()`, `float()`, etc.

    By defining our own functions, we can reduce redundancy (saving ourselves from having to write the same code over and over whenever we want to perform the same set of actions).

    The function {term}`arguments` represent the function's inputs, and the {term}`return` value represents its output. 

    You might think of a function as the kitchen in a restaurant. When you call a function with arguments, that's like submitting an order. The kitchen knows how to handle orders from the menu, and it generally rejects orders not on the menu. Accordingly, if a function is defined so as to take an integer/float argument, and you call this function with a string, the function code will likely raise an error.

    When a function returns a value, that's like the dish prepared by the kitchen in response to your order. 
    
    When eating at a restaurant, you don't need to cook the dish that you order. Likewise, writing functions allows us to separate the execution of one piece of code from the rest of our code. (This is called encapsulation.) Other people can use functions that we wrote (if we package them and distribute them as Python {term}`module's), and we can reuse the same function in different programs. 

    Writing functions also helps make code more readable by breaking it up into smaller, logically coherent parts.

function body

    The body of a {term}`function` is the {term}`block` of code indented underneath the name of the function in a {term}`function definition`. The function body contains the code that executes when the function is called. 

function call

    We call a {term}`function`` (or {term}`method`) when we write the name of the function followed by parentheses. The parentheses may or may not contain {term}`arguments`, depending on how the function has been defined. But the parentheses are required. (Otherwise, the function is not called.) 

    Calling a function triggers Python to execute the code in the {term}`function definition`. 

function definition

    A function definition starts with the `def` {term}`keyword`, followed by the name of a function, zero or more {term}`arguments` in parenthese, and a colon. The {term}`function body` is indented underneath the first line of the function definition. 

    When Python executes code that **defines** a function, the code in the function body is _not_ executed. It is merely stored in memory, to be executed later when the function is called. (See {term}`function call`.)

    In this way, a function definition is like a {term}`variable` assignment, except that what's being stored in this case is not data, but Python code itself. 

if statement

    We use `if` statements to write code that performs different actions depending on the presence of certain conditions. In the simplest kind of `if` statement, we use one {term}`Boolean expression` to determine whether or not a single {term}`block` of code will be executed. 

    The following code prints `10` only if the {term}`variable` `x` is `5`.

        if x == 5:
            print(x * 2)
    
    To express more complex logic, we can use one or more `elif` statements after an `if` statement to test for alternate conditions, and an `else` statement to trigger behavior that doesn't match any of the express conditions. 

    The following code prints a different message depending on whether a variable matches one of a cetain number of strings or none at all:

        if favorite_language == 'Python':
            print('Good choice!')
        elif favorite_language == 'Ruby':
            print('Another good choice!')
        else:
            print("Sorry, I don't know that language.")         # This will be executed when favorite_language is anything but 'Python' or 'Ruby'

import

    A Python {term}`keyword` used to load into memory some Python code that is stored externally (i.e., not loaded automatically when starting a Python session). Such code often defines Python classes or functions and is called a **module**. There are modules that form part of the basic Python installation (like the `json` module), and there are modules that are created by third parties for use with Python -- also called **packages** -- which must be installed separately before they can be used. For more information on installing third-party modules/packages, see the [Python documentation](https://packaging.python.org/en/latest/tutorials/installing-packages/).

    The term **library** is also used to refer to one or more Python modules that has been packaged together. For instance, the [pandas library](https://pandas.pydata.org/) is a very popular Python library used for data analysis.

indented block

    See {term}`block`.

index

    The position of an element in a {term}`list` or a {term}`character` in a {term}`string`. We can use the index to extract a single element/character, or we can use a range of indices to extract a {term}`slice` (a subset of the string or list). 

    Indices in Python start at `0` (meaning, the first element or character is considered to have an index of 0, not 1) and increase from left to right. 

    We can also use negative numbers for indices, in which case we start with `-1` and count **down** as we move to the **left**. So if `my_list` has 5 elements, the following is `True` (because the indices refer to the same element):

        `my_list[4] == my_list[-1]`
    
    Note that if `my_list` grows to include more than 5 elements, the expression above will not necessarily be `True`, since `4` would no longer be the same index as `-1`.

indexing

    See {term}`index`.

instance

    An instance of a Python {term}`class` a value whose `type` is of that class. 

    For instance, if we write `x = 5`, then `x` will refer to an instance of the type `int` ({term}`integer`).

    Let's say we define a class called `Student` like so:

        class Student:

            def __init__(self, name):
                self.name = name
        
    Then we can create instances of `Student` as follows:

        student1 = Student("Neha")
        student2 = Student("Li")
    
    These instances will be different, because `student1.name` has the value `"Neha"``, and `student2.name` has the value `"Li"`.
 
integer

    A Python {term}`type` for storing numbers without decimal components, e.g., `10`, `300000`, etc. See also {term}`float`.

JSON

    An acronym for Javascript Object Notation, JSON is a very common data format that (despite its name) can be used with any programming language that supports it. JSON works well with Python because the basic JSON data types readily map onto basic Python {term}`type`s (strings, integers/floats, lists, and dictionaries). 

    We use the `json` module to store and read JSON data with Python code.

key

    One of the two required parts of every entry in a Python {term}`dictionary`. A dictionary key is similar to the {term}`index` of a Python {term}`list`, except that list indices are always numeric and always proceed in order, starting from 0, whereas a dictionary key can be any string or number, as long as it's unique (compared to the other keys in the same dictionary).

    But just as each list index points to a different element in the list, each dictionary key is associated with a particular {term}`value` in the dictionary. 

    The following are some examples of data we could store in dictionaries and how we might construct their keys and values.

    | Dataset | Keys | Values |
    | ------- | ---- | ------ |
    | Census data | Zipcodes | Population by zip code | 
    | Class roster | Student ID's | Grades for each student | 
    | Bookstore inventory | ISBN's | Metadata about each book | 

keyword

    A word in the Python programming language that is **reserved**, meaning that you cannot use it for the name of a variable or function. Some examples include `for`, `if`, `import`, `or`, `and`, `not`, and `in`.

    See the Python documentation for the complete list of [keywords](https://docs.python.org/3.8/reference/lexical_analysis.html#keywords).

library

    A term for a set of tools written in Python, usually involving functions and classes, designed to be used by other Python programmers. See {term}`import` for more information.

list

    A Python {term}`type` for storing data sequentially, i.e., in order, where the data to be stored can consist of any mixture of valid Python types. 

    All of the following are valid Python lists:

        my_numbers = [3, 5, 7, 9]                                   # List of integers
        instructors = ['Marcus', 'Alex', 'Debbie', 'Josh', 'Dan']   # List of strings
        misc_data = [45, '07051978', 'librarian', 182]              # List of integers and strings
    
    Note: be careful when creating lists of mixed types (as in the last example above). In using this list, you would need to remember which elements are integers and which are strings purely by their position in the list, which makes it easy to write code that will produce unwanted errors. 

    It's more common to use a {term}`dictionary` to represent complex data of multiple types, since each element in a dictionary has a {term}`key` that can be more descriptive. For example, if our dictionary has an `age` key, we might guess that this key will correspond to a numeric type, not a string. 

list of dictionaries

    A common approach to representing data that consist of multiple elements (like books or university courses or people in a class) where each element has more or less the same set of attributes. (For books, those attributes might be `title`, `author`,` publisher`, etc. For people, `name`, `age`, `email address`, etc.) Each element in the list is a dictionary with the same set of keys; only the values are different. 

loop variable

    The {term}`variable` in a {term}`for loop` that assumes the value of each element in the {term}`collection` over which the loop runs. 

    For instance, given the the following code
    
        for number in [1, 3, 5, 7]:
            print(number * 2)           # Multiples each number by 2
    
    the following table shows the values of the loop variable on each time through the loop (the loop iteration):

    | Loop iteration | Value of `number` |
    | -------------- | ----------------- |
    | 1              | 1                 |
    | 2              | 3                 |
    | 3              | 5                 |
    | 4              | 7                 |

    It's important to note that when a `for` loop is complete, the loop variable still exists, at which point it has the **last** value to which it was assigned in the course of the loop. (In the code above, that would be `7`). Normally, you don't want to use a loop variable _outside_ the code {term}`block` of the `for` loop. However, because Python doesn't raise an error or otherwise warn you if you do so, it's easy to do so by mistake. A good rule of thumb: the loop variable should normally only appear in code indented underneath the `for` loop where the loop variable is defined. 

method

    Basically, the same as a Python {term}`function`, except that a method belongs (by definition) to a particular Python {term}`type` or {term}`class`. We call methods using {term}`dot notation`. 

    Since every {term}`instance` of the type {term}`string` (`str`) has access to the `split()` method, we can use the method like so:

        courses = 'CHEM BISC PHIL ANTH PSCI'
        course_list = courses.split()           # course_list is ['CHEM', 'BISC', 'PHIL', 'ANTH', 'PSCI']

    Methods are essentially a syntactic convenience. As in the example above, they save us the trouble of passing an argument (see {term}`arguments`) to tell the method what specific instance it should be applied to. Since `courses` is defined as an instance of the string type, when we call `courses.split()`, Python assumes that we want to split the string called `courses`. 

    Alternately, we could write `str.split(courses)`, which calls the same method from the `str` type directly, but that way is more verbose (and so seldom, if ever, used).

module

    See {term}`import`.

null value

    A null value represents the absence of a value. A variable that has a null value is basically pointing to an empty address in the computer's memory. In order to represent this situation, Python uses the special {term}`type` called `None`. When you encounter a `None`, it's like a placeholder: there _could_ be a value there, but none has been assigned. 

    Note that if you try to use a {term}`variable` name before assigning it to a value, Python will raise a `NameError`; it won't automatically assign the null value to your variable. (Some languages handle this situation differently.) In Python, null values tend to arise when loading data from external sources, and they often represent missing data: for instance, empty cells in a spreadsheet. 

object

    A generic term for a "thing" in Python and many other programming languages. In Python, every object is an {term}`instance` of a {term}`type`, which can be a built-in type or a user-defined {term}`class`.

parentheses

    Parentheses `()` are used in Python primarily to denote a function or method, either in the {term}`function definition` or the {term}`function call`. The {term}`arguments` to the function/method, if any, appear between the parentheses.

    Parentheses are **not** optional in these situations; if there are no arguments, the parentheses will be empty (but they must be present).

quotation marks

    Python uses pairs of single (`''`) or double (`""`) quotation marks interchangeable to identify {term}`string` values. You can choose whichever style you like (single or double); the only requirement is that, for any given string, you use them consistently. 

    For instance, the following line would produce a syntax error, because the string starts with a double quote but ends with a single quote:

        my_name = "Dolsy Smith'
    
    If you need to use a quotation mark as part of your string, use the other kind of quotation marks to enclose the string itself. For instance, the code below (correctly) assigns a string containing an apostrophe:

        my_message = "Python's a pretty cool language."

return

    The 'return` {term}`keyword` is used in a {term}`function definition` to provide a value back to the code that made the {term}`function call`. 

    See {term}`function` for more information.

slice

    A slice is a subset of a Python {term}`list` or {term}`string`. To create a slice, we use {term}`square brackets` around a pair of numbers separated by a {term}`colon`, where the first number is the position of the first element we want to include, and the last element is **one plus** the position of the last element to include. 

    To take the first three elements of the list `my_list`, we would write `my_list[0:3]`, because the first element is in position 0, and the third element is in position 2 (and 2 + 1 = 3). 

    The fact that the first number in a slice is inclusive and the second number is exclusive does take some getting used to. There's no good reason for it except convention. 

    We can also use some shorthand when taking a slice that starts with the first element in the list or that includes the last element. 

    `my_list[:3]` is the same as `my_list[0:3]`.

    If `my_list` has 5 elements in total, then

    `my_list[3:5]` is the same as `my_list[3:]`. 

square brackets

    Square brackets (`[]`) are used in a few different ways in Python:
        - In defining a {term}`list``: `my_list = [1, 3, 5, 7]`
        - In accessing a value by its {term}`index` in a {term}`string` or list: `print(my_list[2])` (This prints the number '5'.)
        - In creating a {term}`slice` of a string or list: `my_list[0:2]`
        - In accessing the value in a dictionary by its {term}`key`: `print(my_dict['name'])` prints the value associated with the key `name` in `my_dict`.


standard library

    The set of functions, data types, methods, and other tools that are available with the basic installation of Python.

string

    A basic Python {term}`type` comprising a {term}`collection` of {term}`character`s. We can create a sting by enclosing any text (really, anything you can type on your keyboard) between quotation marks. 

    Like elements in {term}`list`s, we can access characters within string by their {term}`index`. We can also create {term}`slice`s of strings. 

    Strings have {term}`method`s, such as `split()`. See the [Python documentation](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) for a complete list.

test

    A test in the context of programming is typically some code designed to check the functionality of other code. For instance, when developing an application, programmers will typically write multiple tests that can be used to confirm that various parts of the application work as intended. This approach is particularly helpful when the application goes through multiple development cycles, receiving bug fixes and enhancements. In such situations, having a suite of tests ensures that changes to one part of the application don't break other parts of the application. 

type

    A Python type is, in essence, a set of behaviors associated with a certain way of representing data. Let's unpack this a bit.

        - We say "a certain way of representing data" rather than "a certain kind of data" because what we might consider the _same_  data in the "real" world -- like a list of numbers -- can be represented in Python by many different types, depending on the use case. 
          - A number can be a {term}`string``: `"07051978"`. 
          - A number can be an {term}`integer`: 7051978
          - A number can be a {term}`float`: 7051978.0
          - Or it could be an instance of another type, like a [date](https://docs.python.org/3/library/datetime.html). 

    We say a "set of behaviors" because Python doesn't "know" what makes a date (as a human construct for measuring time) different, in principle, from any other set of numbers. Rather, each type is associated with certain {term}`attributes` and {term}`method`s that determine how the type can be used. 

    For instance, if our number is represented as a string, we can extract each digit as a single character, or take a {term}`slice` of some subset of digits. If our number is represented as an integer or float, we can add, subtract, multiply, or divide with it. 

    I like to think of a Python type as a kitchen appliance. Each applicance has attachments specially designed to enable it do certain things. A food processor might have a grater attachment, which I can use to shred carrots. I can't shred carrots in a stand mixer, because a stand mixer doesn't have the right attachment. But I can beat eggs or knead flour in a stand mixer, which might be hard or impossible to do in a food processor. 

    Just as cooks choose the right appliance for the task at hand, so programmers choose the kind of `type` to use depending on goals and context. 

value

    The word _value_ is ambiguous when talking about Python. On the one hand, we can talk about any occurence of data as a _value_, as when we say that in defining a {term}`variable`, the value goes on the right of the equals sign. 

    But _value_ is also the technical term for one half of the paired elements that make up a Python {term}`dictionary`, which consists of pairs of {term}`key`s and values. 

    What the two uses of _value_ have in common is that they both refer to something that is being assigned to or associated with something else. 

    Thus, in creating a dictionary, the values fall on the right side of the {term}`colon`s (or on the right side of the equals sign, if we're assigning a single key to its value).

variable

    A variable consists of two parts: a name and a value. The **name** must be a [valid](https://www.asmeurer.com/python-unicode-variable-names/) and unique sequence of characters, _without_ quotation marks; the name will serve as the variable's handle in the program. 

    The **value** can be an {term}`instance` of any valid Python {term}`type`, such as a string, integer, float, list, dictionary -- or an instance of a user-defined {term}`class`.

    Thus, by assigning this long integer to the name `x`

        x = 123456789123456789
    
    we can refer to the variable `x` subsequently in our code in order to work with this number. Whenever we use `x` -- as in `print(x)` or `x = x*2` -- Python will retrieve the variable's value from memory and substitute it for the name `x`.

    In creating variables, we assign a name to a value with the single equals sign. The names goes on the left of the equals sign, the value on the right.

Unicode

    A system for representing characters from the world's many languages along with other symbols (mathematical symbols, emojis, etc.). Python handles Unicode by default, which means that you can use Python to work with text in languages other than English. See {term}`character` for more information. 

white space

    The phrase _white space_ refers to characters created by the spacebar, the tab key, and/or the return/enter key on your keyboard. 

```