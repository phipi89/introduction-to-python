# 07 Exercises: Numerical Computing Solution

## Task 01

```python
import numpy as np


# a)
r = 15
a = np.linspace(0, np.pi * 2, 10_001)[:-1]

x = r * np.sin(a)
y = r * np.cos(a)
z = np.zeros_like(x)

xyz = np.transpose([x, y, z])


# b)
a = np.deg2rad(30)
c, s = np.cos(a), np.sin(a)
Rx = np.array([
    [1, 0,  0],
    [0, c, -s],
    [0, s,  c]
])

a = np.deg2rad(60)
c, s = np.cos(a), np.sin(a)
Ry = np.array([
    [c,  0, s],
    [0,  1, 0],
    [-s, 0, c]
])

# @ in NumPy is matrix multiplication.
# You can also use `np.dot` or `np.matmul`.
trajectory = xyz @ Rx.T @ Ry.T

shift = [409, 99, 282]
trajectory += shift


# c)
base = [-500, -100, -100]
# True, so we can't reach the full trajectory.
any(np.linalg.norm(trajectory - base, axis=-1) > 1000)
```

## Task 02

```python
# a)
pressure = np.load("src/pressure.npy")
pressure.min(), pressure.mean(), pressure.max()


# b)
squared = pressure**2
squared.min(), squared.mean(), squared.max()
```

`pressure**2` becomes partially negative, even though this operation should return only positive elements. The issue is that `pressure` has data type `np.int16` (integers represented by 16 bit). Squaring can reach values not representable by this type, so it overflows. We can fix that by creating a new array with another datatype: `pressure.astype(float)`.

```python
# c)
fs = 44_100
segment_size = fs // 10
n_segments = np.ceil(pressure.size / segment_size).astype(int)
target_size = n_segments * segment_size

pressure_padded = np.pad(pressure, (0, target_size - pressure.size))


# d)
pressure_padded = pressure_padded.astype(float)**2
segments = np.reshape(pressure_padded, (segment_size, -1))
rms = np.power(np.mean(np.sqrt(segments), axis=-1), 2)


# e)
from IPython.display import Audio, display


display(Audio(pressure, rate=fs))
```

## Task 03

```python
# dummy array of same shape
ct_slice = np.empty((481, 481))

center = np.array([90, 260])
indices = np.indices(ct_slice.shape)


# explicit, as seen in lecture
center_y, center_x = center
y_coords, x_coords = indices

offsets_explicit = np.array([
    y_coords - center_y,
    x_coords - center_x
])


# implicit
offsets_broadcasted = indices - center[:, np.newaxis, np.newaxis]

assert np.isclose(offsets_explicit, offsets_broadcasted).all()
```

`center` has shape `(2, )`, while `indices` has shape `(2, 481, 481)`. . To make these arrays compatible for broadcasting, we can add two singleton dimensions to center, giving it shape `(2, 1, 1)`, which we do using np.newaxis. Equivalently, we could manually redefine `center = [[[260]], [[90]]]`.

## Task 04

```python
from src.utils import show_image_arrays


# a)
µct = np.load("src/µct.npy")
show_image_arrays(µct.mean(axis=0))


# b)
volume_mm3 = np.sum(µct > 700) * 0.125**3


# c)
show_image_arrays(
    µct[95, 90:170, 290:390],
    µct[60:110, 125, 290:390],
    µct[60:110, 95:170, 350],
)
```
