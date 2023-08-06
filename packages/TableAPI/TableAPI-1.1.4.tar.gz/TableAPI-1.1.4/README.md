# TableAPI
TableAPI is a very simple "API"  to create tables in the python console.
Its not much but i love this project lmao :)

## Getting Started
To write a simple Table, create a table object with the columns and some simple rows:

```py
table = Table('A', 'B')
table.add_row('This is', 'a simple test')
```
Now we have a table, but how do we render it in the console?
Well, we have to print the build of the table. Very simple.
```py
print(table.build())
```
In the console should be a simple table now.
## Worst Documentation Ever
#### Create a Table
There are two ways to create a Table. First one, define the column titles directly in the constructor:
```py
table = Table('A', 'B')
```
or define the amount of columns and have no titles:
```py
table = Table(2) # Has to be bigger than 0
```
<hr>

#### Build a Table
Simple, it will return a string, which you can print in the console
```py
table = Table('A', 'B')
print(table.build()) # Table#Build() will return the table as a string
```
Here you go ;)
<hr>

#### Define new Header
It is possible to define a new header with following code snippet:
```py
table.set_header('A', 'B')
```
**NOTE:** The amount of strings must match with the amount of columns!
<hr>

#### Add a Row
To add a row to a table just write:
```py
table.add_row('A', 'B')
```
**NOTE:** The amount of strings must match with the amount of columns!
<hr>

#### Remove a Row
To remove a row from a table just write:
```py
table.remove_row(0) # 0 => Row Index
```
**NOTE:** Index must be smaller than row size and bigger than zero, else it will return None!
<hr>

#### Get a Row Object
There is also a way to get the Row object out of the table. You can write:
```py
table.get_row(0) # 0 => Row Index
```
**NOTE:** Index must be smaller than row size and bigger than zero, else it will return None!
<hr>

#### Edit a Field
To Edit a Field of a table in a specific row and column, this snippet could help:
```py
table.edit_field(0, 1)  # 0 => Row Index 
						# 1 => Column Index
```
**NOTE:** Row-Index must be smaller than the row size and bigger than zero!
**NOTE:** Column-Index must be smaller than the column size and bigger than zero!
<hr>

### Exceptions
There are some exceptions that can come up and here is explained, how you can work with them
#### InvalidArgSizeException
This Exception will come up if the argument size is not matching a valid pattern.
For Example, if you write
```py
table = Table(2, 2)
# or
table = Table()
```
it will raise this exception, because you can only define 1 column integer or multiple strings.
If the Constructor is empty, it doesnt work.
<hr>

#### InvalidIndexException
This Exception will raise, if the Index on a function that doesnt return something, cannot find a specific Index like this:
```py
table = Table(1)
table.get_row(200) # There is no row 200
```
The Exception just means, that the index isnt available.
<hr>

#### FieldNotFoundException
This Exception will raise, if the field isnt available:
```py
table = Table(1)
table.edit_field(69, 69) # There is no row 69 and column 69
```
The Exception just means, that the Field on the row-index and column-index isn't available.
<hr>


##### Have fun coding <3
##### ~fluffy