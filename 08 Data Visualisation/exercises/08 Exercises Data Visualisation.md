# 08 Exercises: Data Visualisation

## Notes

1. Use Matplotlib. You find the documentation at https://matplotlib.org/stable/api/index.
2. Work in a Jupyter Notebook.

## Task 01

Lissajous curves are defined as

$$
x = A\sin(at + \delta), \qquad y = B\sin(bt).
$$

Create a 4×6 grid to visualise Lissajous curves for different ratios $a/b$ and phases $\delta$.
In the lecture we always passed `layout='constrained'` to the subplots constructor. See how the layout changes with layout set to `None` or `'tight'`.

Then, make the appareance minimal by removing all ticks and gridlines.

## Task 02

Load `src/observations_a.csv` (using NumPy). Have a look at that data using Matplotlib.

Then, create a figure that illustrates the essential findings.

## Task 03

Load `src/observations_b.csv`, which contribute some new measurements to the same data from Task 02. How does this change the dataset? You may want to do a 3d Plot. Create a new figure to illustrate the updated findings.

## Task 04

Save this image from William Cheselden's _Osteographia_ https://www.nlm.nih.gov/exhibition/historicalanatomies/Images/1200_pixels/cheselden_t32.jpg to your harddrive, then load it with Matplotlib.

Create a figure that shows the image; strip the axis, but add an appropriate title, and use Matplotlib's `annotate` to point arrows at some bones and lable them.
