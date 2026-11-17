# 04: Objects and Classes

## TL;DR

- Classes bundle data (attributes) and functionality (methods)
- They let us define arbitrary custom object types
- Built-in behaviour (e.g., arithmetics or iteration) is implemented through *dunder methods* (`__add__`, `__iter__`, …)

## Abstraction

```python
print('abstraction')
```

This line looks trivial, but behind the scenes it relies on an immense stack of complexity. From sourcing raw materials, manufacturing silicon wafers, and designing CPUs, to building operating systems and compilers: No single person could master it all.

What makes this possible is abstraction. In each layer, experts hide unnecessary detail and expose only what's needed for the next task. The same principle applies in code: Classes let us encapsulate detail and expose the relevant data and functionality, so we can work efficiently without becoming overwhelmed in complexity.

## Self

Below is a simple class example which we saw two weeks ago. Note how every method has a first argument named `self`.

When we construct the instance, we provide only the heart rate and stroke volume. The `__init__` method formally takes three arguments, but we don't supply _self_. That's because Python automatically passes the instance itself as the first argument whenever a method is called.

This allows the method to access and modify the instance's own data. By convention, that first parameter is always named _self_.

```python
class Patient:
    def __init__(self, stroke_volume, heart_rate):    # __init__ expects `self`
        self.stroke_volume = stroke_volume
        self.heart_rate = heart_rate

    def cardiac_output(self):
        return self.stroke_volume * self.heart_rate

pat_a = Patient(0.072, 75)                           # `self` implicitly passed by Python
pat_b = Patient(0.089, 82)

# in pat_a.cardiac_output, self refers to pat_a
# in pat_b.cardiac_output, self refers to pat_b
```

## Dunder Methods

We saw that built-in types such as integers are also classes, just ones that Python already implemented for us. But then, how does Python know for example how to add two integers?

```python
# addition
314 + 159            # 473


# concatenation, uses the same syntax
'314' + '159'        # '314159'
```

The answer is that internally, `a + b` is translated into `a.__add__(b)`. This means that the behaviour of `+` depends only on how the class `a` implements `__add__`.

```python
# addition
314 + 159            
(314).__add__(159)   # under the hood


# concatenation
'314' + '159'
('314').__add__('159')
```

This mechanism is not limited to the plus operator: Every operator or built-in behaviour (arithmetic operations, comparison, iteration, assignment and even calling) corresponds to a special *d*ouble *under*score (aka dunder) method, that classes can define.

We have already seen `__init__`, which automatically runs when an object is created. Dunder methods are invoked by Python itself, and the underscores emphasise their special status.

The elegance of this design is that it's very easy to make our own classes behave like native objects.

### Example

We observed above that `+` can both add numbers and concatenate strings. Let's apply this idea to numerical values in decibel. To sum them, we need to transform them first to linear amplitude, add them, and convert back to decibels. By implementing this inside `__add__`, we can use the `+` operator on two instances and correctly add them.

```python
import math


class decibelValue:
    """Sound Pressure Level in dB re 20 µPa."""
    ref = 20e-6

    def __init__(self, value):
        self.value = value

    def amplitude(self):
        """Return the RMS sound pressure in Pascals."""
        return self.ref * 10**(self.value / 20)
        
    def __add__(self, other):
        """Addition of two coherent sound sources"""
        amplitude = self.amplitude() + other.amplitude()
        dB = 20 * math.log10(amplitude / self.ref)
        return decibelValue(dB)

loud = decibelValue(105)
soft = decibelValue(65)

print((soft + loud).value)     # 105.08642747565284
```

Observe:

- We use docstrings to document the relevant things to know. That way, we automatically create a basic documentation that can be read using help(decibelValue)
- Classes can have class-level constants, here for example the reference pressure.

Let's add some other functionality. We observe for example, that printing a decibelValue does not show its value, but only a default name:

```python
print(loud)       # <__main__.decibelValue object at 0x10cf763c0>
```

That's not very helpful. Print converts its arguments to strings, so we can implement a `__str__` method to manage what is printed. That way, we can print a formatted representation of the objects.

```python
class decibelValue:
    """Sound Pressure Level in dB re 20 µPa."""
    ref = 20e-6

    def __init__(self, value):
        self.value = value

    def amplitude(self):
        """Return the RMS sound pressure in Pascals."""
        return self.ref * 10**(self.value / 20)
        
    def __add__(self, other):
        """Addition of two coherent sound sources"""
        amplitude = self.amplitude() + other.amplitude()
        dB = 20 * math.log10(amplitude / self.ref)
        return decibelValue(dB)

    def __str__(self):
        return f"{self.value:.2f} dB"

loud = decibelValue(105)
print(loud)                     # 105.00 dB
```

## Inheritance

Often, we might have an existing data type that does most of what we want, but we would like to tweak some detail, or add some functionality. For this, classes can _inherit_ from other classes.

```python
from datetime import date


print(date.today())                  # 2026-10-05
```

Let's say we don't like how `date` prints. We can create a new class that matches all functionality `date`, but with a replaced version of the `__str__` method.

```python
class MontyPythonDate(date):
    """Regular date, but represented as days 
    since Monty Python's Live of Brian.
    """

    release_date = date(1979, 8, 17)
    
    def __str__(self):
        delta = self - self.release_date
        return f"{delta.days} days since Monty Python's Live of Brian"
    

print(date.today())                  # 2026-10-05
print(MontyPythonDate.today())       # 17226 days since Monty Python's Live of Brian
```

Let's revisit the Patient class. We might want to add general information such as a name and patient id. One approach towards this is to create a BasePatient class for the general information, and a CardioPatient that inherits from it.

This leads to a subtle issue: When we define a custom `__init__` in CardioPatient, it overrides the `__init__` from BasePatient. Therefore, the attributes name and id will not be set. We need to explicitly initialise BasePatient ourselves. We do this explicitly by calling `BasePatient.__init__`.

```python
class BasePatient:
    def __init__(self, name, id):
        self.name = name
        self.id = id


class CardioPatient(BasePatient):
    def __init__(self, name, id, stroke_volume, heart_rate):
        
        # need to explicitly initialise again
        BasePatient.__init__(self, name, id)
        
        self.stroke_volume = stroke_volume
        self.heart_rate = heart_rate

p = CardioPatient(name='Eric Idle', id=1_000_001,
                  stroke_volume=0.073, heart_rate=68)

# flat hierarchy
p.heart_rate
```

> Note: For this simple example, we call `BasePatient.__init__` explicitly. In general, Python has a function to grab the parent class, called `super`. Equivalently, we can therefore call `super().__init__`. The advantage is that, if the name of BasePatient changes, super() still works. In more complex situations with inheritance from multiple parents, super ensures that all init methods are called once in the right order, so best is to just always stick with the super() notation.

### Composition

It is easy to see that this might get crowded quite fast. The idea of classes is to create structure, but we now cram all data again into the same object. It's conceptually simpler, and often better, to not inherit but _compose_. Inheritance expresses a "is a" relationship, composition expresses a "has a" relationship. Below we change the logic structure such that we keep the basic patient, but extend it with a heart. This introduces a hierarchical structure, the heart_rate for example becomes `p.heart.rate`.

```python
class Heart:
    def __init__(self, stroke_volume, heart_rate):
        self.stroke_volume = stroke_volume
        self.rate = heart_rate


class Patient:
    def __init__(self, name, id, stroke_volume, heart_rate):
        self.name = name
        self.id = id
        self.heart = Heart(stroke_volume, heart_rate)


p = Patient(name='Eric Idle', id=1_000_001,
            stroke_volume=0.073, heart_rate=68)

# nested hierarchy
p.heart.rate
```

## Wrap-Up

- _Abstraction:_ helps us manage and understand larger projects by _exposing only what matters_.
- _Classes bundle data and behavior_, hide internal details, and let us define new object types that behave like built-ins.
- _Every class method receives `self`_, a reference to the instance, so methods can access and modify that instance’s data.
- _Dunder methods:_ lets custom classes _integrate_ naturally _into Python_'s syntax and built-in operations.
- _Inheritance and composition:_ allows us to design _clear, extensible structures_ that scale with complexity.
