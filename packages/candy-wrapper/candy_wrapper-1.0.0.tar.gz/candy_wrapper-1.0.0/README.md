# Candy Wrapper
Candy Wrapper is a "sticky" wrapper for any object, which adds syntax surgar.

This wrapper wraps any object, and give the ability
to add attributes to the object like a dictionary,
much in the same way that pandas dataframs work.

## Installation

You can install candy_wrapper with pip:

```
pip install candy_wrapper
```

Or with poetry:

```
poetry add candy_wrapper
```

## Usage

```python
from candy.candy_wrapper import Wrapper
foo = SomeClass()

# Wrap an object
candy = Wrapper(foo)

# Add an attribute to the object
foo['bar'] = 42

# Access the attribute
print(foo.bar)  # prints 42

# You can also use setattr
setattr(foo,'hey',420)

# And getattr
print(foo['hey'])  # prints 420
```                            
