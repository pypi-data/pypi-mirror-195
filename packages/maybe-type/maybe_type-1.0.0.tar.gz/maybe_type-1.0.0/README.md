# maybe_type

## Description
This module adds the Maybe monad to python. That's it!  
Actually, to be more exact, it adds *and does* the following:  
1. The Maybe struct: A type that represents a value that may or may not be present.
2. The with_maybe decorator: A decorator to make a function return it's result wrapped in a Maybe.

## Functions of the Maybe type
* `Maybe.map` Applies a function, that doesn't return a Maybe, to the value, if it is present.
* `Maybe.bind` Applies a function, that returns a Maybe, to the value, if it is present.
* `maybe.extract` Extracts the value, if it is present, otherwise raise an exception.

## Usage / Examples
### Creating a Maybe value
```py
from maybe_type import Maybe, with_maybe

mogus = Maybe(5)
```
### Using the Maybe.map function
```py
def add_one(x):
    return x + 1

mogus.map(add_one)
```
### Using the with_maybe decorator and the Maybe.bind function
```py
@with_maybe
def add_one_maybe(x):
    return x + 1

mogus.bind(add_one_maybe)
```
### Using the Maybe.extract function to extract the value (and then printing it)
```py
mogus_extracted = mogus.extract()
print(mogus_extracted)
```

### Doing it all in one beautiful pipe
```py
mogus_extracted = Maybe(5).map(add_one).bind(add_one_maybe).extract()
print(mogus_extracted)
```

## Why should i use it?
As I just demonstrated, the Maybe type allows us to write beautiful, declarative code using what is reffered to as "pipe lines".
Instead of doing something like
```py
mogus = 5
if mogus:
    mogus = add_one(mogus)

    if mogus:
        mogus = add_one_maybe(mogus)

        if mogus:
            mogus = extract(mogus)

print(mogus)
```
(My eyes started burning halfway through writing that)  
Of course, no one would write such goofy ahh code, as they could just do `print(5 + 2)`, but i think you get the point.