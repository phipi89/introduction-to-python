# 07: Numerical Python

## TL;DR

```python
import numpy as np


circle_coords = np.random.rand(1_000_000, 2) * 2 - 1      # broadcasting
inside = np.linalg.norm(circle_coords, axis=-1) <= 1      # vectorisation
pi = 4 * inside.sum() / inside.size                       # convenience
```

NumPy is a great toolbox that brings along datatypes and functions to work with collections of numerical data.

## NumPy Arrays

`numpy.ndarray`s are collections that replace lists for numerical computing. In contrast to lists, which can hold arbitrary elements, each Numpy array holds a single type. Ndarrays are multidimensional and fixed in size. Because they hold a defined number of elements, all of the same data type, NumPy can efficiently manage it in memory.

```python
import numpy as np


python_list = [1, 1.1, 1.2]                 # [int, float, float]

numpy_array = np.array([1, 1.1, 1.2])       # [all floats]

integer_array = numpy_array.astype(int)     # [all ints]
```

## Vectorisation

In physics, we are used to having variables represent multidimensional data. For example, in $\vec{F}=m \vec{a}$, force and acceleration are three dimensional vectors.
NumPy picks up this idea as well. In NumPy, math works directly on collections of elements, and loops become implicit. This improves the readability of code and executes much more efficiently.

The example below illustrates how we can perform math and comparisons directly on arrays of elements (think how this would be implemented in pure Python). NumPy also handles a lot of edge cases for us. The last two elements for example cause division by zero. Instead of raising a `ZeroDivisionError`, NumPy logs a `RuntimeWarning` (*divide by zero encountered*). The calculation is valid (the result of division by zero is `inf`inity).

```python
coffee = np.array([0, 1, 2, 3, 4, 5])
emails = np.array([9, 5, 3, 2, 0, 0])

ratio = coffee / emails                  # array([0., 0.2, 0.666667, 1.5, inf, inf])
motivation = np.arctan(ratio) * 2/np.pi

motivation > 0.5                         # array([False, False, False,  True,  True,  True])
```

Observe: Working with vectors as entities makes our calculations more readable: In plain Python, we would need to use a for loop (or list comprehension) to step through all elements. As a side note, see that NumPy implements (among many other things) trigonometric functions for us.

### Speedup

NumPy runs array operations in efficient, precompiled code. This avoids the overhead of looping through individual elements in Python. The speedup becomes apparent when handling larger arrays. The example below compares computing the standard deviation of a 100 million element list in NumPy versus pure Python, and we observe a significant speedup (Note, for illustration purposes, we do an explicit computation, even though there would be `np.std(l)` for us to use).

```python
# takes 0.3 seconds

l = np.arange(100_000_000)
squared_diffs = (l - np.mean(l)) ** 2 / len(l)
std = (squared_diffs.sum() / len(squared_diffs)) ** 0.5
# Note: there's also np.std(l)


# takes 13 seconds

l = range(100_000_000)
mean = sum(l) / len(l)
squared_diffs = [(e - mean) ** 2 / len(l) for e in l]
std = (sum(squared_diffs) / len(squared_diffs)) ** 0.5
```

## Multidimensional Data

### Examples

NumPy operations operate on any multidimensional array. For the upcoming example, we work with a single slice from a micro computed tomography image of a human temporal bone (source: https://doi.org/10.5281/zenodo.1473724). Such a slice is a 2D array of radiodensity values (in the exercises, you will get your hands on the full 3D version of the CT scan). Everything we see here in two dimensions generalises directly into arbitrary higher (and lower) dimensional arrays.

```python
ct_slice_raw = np.load('µct_slice_raw.npy')

#   array([[-470, -469, ..., -470, -470],
#          [-240, -228, ..., -259, -259],
#          [-192, -211, ..., -249, -220],
#          ...,
#          [-164, -224, ..., -278, -246],
#          [-220, -232, ..., -280, -277],
#          [-469, -470, ..., -470, -470]],
#         shape=(481, 481))
```

![Cell output](media/07%20CT_slice.png)

As an additional example, below we construct a 3D curve that spirals along a cone. This illustrates several useful tools:

- We can use constructors like `ramp`, from which we can build more complex structures.
- `linspace` is convenient for creating linearly spaced values between two endpoints.
- `transpose` (or the shorthand `ndarray.T`) allows to swap rows and columns.

```python
ramp = np.linspace(0, 1, 10_000)
# [0, 0.0001, 0.0002, …]

angles = 6 * 2 * np.pi * ramp

x = ramp * np.sin(angles)
y = ramp * np.cos(angles)
z = 1 - ramp
# all shape (10_000, )

# shape (3, 10_000)
rows = np.array([x, y, z])

# shape (10_000, 3)
cone = rows.T
```

![Cell output](media/07%20cone.png)

## Slicing

The µCT we imported above contains a lot of unnecessary padding around the bone. We can extract regions from NumPy arrays exactly the same as we can slice regular Python lists, using the `list[start:stop:step]` notation. In NumPy, this generalises to multiple dimensions, by accepting touples of slices. In 2D, we can slice along the first and second axis by `ndarray[start_x:stop_x:step_x, start_y:stop_y:step_y]`.

Note: Slicing typically creates a _view_ into the data. The underlying array stays the same in memory. If you need a new array, keeping the old array intact, create a copy using the `ndarray.copy` method.

```python
#                       ↱ 1st dim
ct_slice = ct_slice_raw[170:330, 100:-50]
#                                ↳ 2nd dim
```

![Cell output](media/07%20slicing.png)

```python
cone[-1]                    # shape (3, )            : last point -> (x, y, z)
cone[:, 1]                  # shape (10_000)         : all y-coordinates
cone[:100, 1:]              # shape (100, 2)         : first 100 points' (y, z) pairs
cone[:, :, np.newaxis]      # shape (10_000, 3, 1)   : all points, u wrapped as [u]
```

## Broadcasting

Mathematical operations on two NumPy arrays can still work even if they have unequal shapes.
This behavior is called *broadcasting*. It can seem obscure at first, but it follows naturally from three simple rules, and with a bit of training will start to feel natural.

Below are three examples that illustrate different levels of broadcasting:

- Scalar: a single value applied to every element.
- In-between: A 1D array applied along one axis af a 2D array.
- Matching full shape: Two arrays of the same shape.

```python
cone *= 2                                     # single value: elementwise

# shape 2:                       ()
# shape cone:         (10_000, 3, )
#                                └┘           # matches single elements

up = np.array([0, 0, 1])
cone += up                                    # applied to each matching subsection

# shape up:                   (3, )
# shape cone:         (10_000, 3, )
#                             └───┘           # matches last axis

random_values = np.random.rand(*cone.shape)
cone += random_values                         # same shape: elementwise again

# random_values:      (10_000, 3, )
# shape cone:         (10_000, 3, )
#                     └───────────┘           # matches all axes
```

Observe:

- Broadcasting works when the trailing dimensions of the two arrays are *compatible*.
- The scalar and same-shape situations are trivial: The operation is performed element by element.
- All other cases can be understood as a combination of the scalar and same-shape examples: Think of the smaller array as a single element that is repeated across the larger one. Then, the element-to-element operation follows the same-shape situation.
- In other words, the process is allways: Repeat (i.e., tile) the smaller array until it matches the larger array, and then apply the operation element by element.

## Axes

Many NumPy functions work on arrays of arbitrary dimension. For example, `np.linalg.norm(cone)` returns as single number,(in this case it's 81.65). But conceptually, the cone array represents a collection of coordinates, not a single higher-dimensional entity. What we are are probably rather interested in is the norm of each coordinate. For this purpose, most NumPy functions feature an `axis` keyword argument. When provided, the function operates individually on all one-dimensional sub-arrays that are oriented along that axis.

- `axis=0`: operates along the outermost dimension
- `axis=1`: operates along the second dimension
- …
- `axis=-1` operates along the innermost dimension.

```python
np.linalg.norm(cone)                    # 81.65
np.linalg.norm(cone, axis=0)            # [40.80, 40.85, 57.74]
np.linalg.norm(cone, axis=1)            # [1, 0.9999, 0.9998, …]

# axis                   0  1
# shape cone:      (10_000, 3, )
```

## Masks

Beyond slicing, part an of array can also be accessed with a _mask_. A mask is a boolean array of the same shape as the array we want to index, and indicates for each element in it, whether it is selected. We might, for example, want to compute the average values of all bone voxels in the µCT. Below, we do this in three steps:

- create a boolean mask that matches the bone voxels (typically, bone starts at 700 HU),
- get a view of all bone voxels in `ct_slice` (by applying the mask),
- compute the mean of this view.

```python
# boolean mask of same shape as `ct_slice`
bone_mask = ct_slice > 700

bone_avg = ct_slice[bone_mask].mean()
# 1083.84

bone_ratio = bone_mask.sum() / bone_mask.size
# 46.8%
```

![Cell output](media/07%20boolean%20masks.png)

A more complex scenario is creating a mask ourself. We can for example create a circular mask around a center, and use boolean operations to extract a region of interest from another mask.

> Note: By convention, images in NumPy (and beyond) are typically represented in (row, col) format. This is inverted from cartesian coordinates which are typically given in (col, row) order.

```python
center_y, center_x = 90, 260
y_coords, x_coords = np.indices(ct_slice.shape)

offsets = np.array([
    y_coords - center_y,
    x_coords - center_x
])

circle_mask = np.linalg.norm(offsets, axis=0) < 40

cochlea = circle_mask & ~bone_mask
```

![Cell output](media/07%20boolean%20operations.png)

## Beyond NumPy

NumPy is the foundation of scientific computing in Python.
Its concepts of typed multidimensional arrays, vectorisation and broadcasting are the basis of many other libraries, notably:

- _Pandas_ builds on NumPy to handle labeled, tabular data.
- _Matplotlib_ relies on it for efficient plotting.
- _SciPy, scikit-learn, PyTorch_ and countless others extend these concepts to scientific computation and machine learning.

Take time to internalise these core concepts. Once you understand NumPy, you also understand the data model and performance principles behind most of the Python data ecosystem. Becoming fluent in manipulating multidimensional arrays is the basis to make you effective in nearly any data-science or numerical-computing task.
