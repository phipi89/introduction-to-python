# 07 Exercises: Numerical Computing

## Notes

1. Where not specified otherwise, use NumPy functions. You find the documentation at https://numpy.org/doc/stable/reference/index.html.
2. Work in a Jupyter Notebook.

## Task 01

Your lab wants to use its new surgical robot to create a craniostomy to place a brain computer interface.

- Create (a NumPy array `xyz` that represents) a circular trajectory in the x-y plane (in 3D cartesian coordinates) with a radius of 15, and of shape (10_000, 3).
- Move the trajectory to the correct location: rotation of 30° around the x-axis > rotation of 60° around the y-axis > shift to [409, 99, 282]. Do this by defining two rotation matrices `Rx`, `Ry`.
- The robot base is at [-500, -100, -100], and its arm has a reach of 1000. Can we access the full trajectory?

## Task 02

`src/pressure.npy` is a microphone recording at a rate of 44_100 Hz.

- Load it using `np.load`. Compute its min, max and mean values.
- Analise `pressure**2`, you will find that something is wrong. What is causing that problem?
- Pad `pressure` with zeros so that its duration is a multiple of 10ms.
- Use `np.reshape` to compute the signal RMS on consecutive 10ms parts using NumPy's `sqrt`, `mean` and `power`. Make sure to incorporate the fix from the previous question.
- We didn't really take advantage of modern notebooks yet. `IPython.display`s `Audio` and `display` allows to display an interactive audio widget to play a waveform. Write that code and listen to it.

## Task 03

In the lecture, we created index coordinates of a 2D array using `np.indices(ct_slice.shape)`. This returns an array containing the x- and y-indices, with shape (2, \*ct_slice.shape).

We then unpacked this into two variables (`y_coords, x_coords`), subtracted the center coordinates, and reassembled it into an array again.
Below is an alternative formulation that tries to directly subtract the center coordinates from the index array. Unfortunately this raises a `ValueError`.

- Describe why this error occurs.
- Describe what shape `center` needs to be, so that broadcasting works.
- Rewrite `center` accordingly.

```python
# ----------------------
# as seen in the lecture

center_y, center_x = 90, 260
y_coords, x_coords = np.indices(ct_slice.shape)

offsets = np.array([
    y_coords - center_y,
    x_coords - center_x
])


# -------------------------------
# alternatively with broadcasting

center = np.array([90, 260])
indices = np.indices(ct_slice.shape)

# this does not work
offsets = indices - center
```

## Task 04

`src/µct.npy` contains data of a micro computed tomography scan of a temporal bone. Data visualisation comes up only next week, so you can use `src.utils.show_image_arrays` (remember you can use `?` to learn how to use it).

- In the lecture we used the 95th slide (along the first axis). Use np.mean to compute digitally reconstructed radiograph (DRR, i.e., an x-ray like image) in the same plane as this slice. Can you still make out the cochlea?
- Count the number of bone voxels in the µct (assume that bone has values >= 700 Hounsfield units), and compute its volume (isotropic voxel spacing of 0.125 mm).
- Find and show three slices (along the three cartesian axes) centrally through the cochlear spiral. Use slicing to crop them to a boundary box close around the cochlea (see https://share.google/images/JzBvDBieTdQnd4BLt for how the cochlea looks like in different orientations).
