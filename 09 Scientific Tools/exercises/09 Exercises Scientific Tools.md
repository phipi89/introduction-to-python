# 09 Exercises: Scientific Tools

## Notes

1. Use Matplotlib, NumPy and SciPy, where not mentioned otherwise.
2. Work in a Jupyter Notebook.
3. As always, create a fresh virtual environment using uv.

## Task 01

Load `src/observations.csv` and visualise the data in a 3D scatter plot, colouring the points by group. They are the same data as last week, but unfortunately in a different coordinate system, so the z-axis does not separate them anymore.

Use *scikit-learn* to perform a principal component analysis and draw the three principal axes in your 3D plot. Then project the data onto the first two principal components and visualise the result in 2D.

## Task 02

Revisit `src/pressure.npy` from Exercise 7.2. Export it as a WAV file, listen to it using an external audio player. How do you expect the dominant frequencies to change over time?

Reimport the WAV into Python, split the audio into consecutive 1-second segments, compute the FFT of each, and plot the prominent frequency peaks over time. Finally, use Matplotlib to visualise the audio as a spectrogram. Can you explain what you observe?

## Task 03

- Download the hip CT image used in the lecture from https://doi.org/10.5281/zenodo.20473746, and import it into Python.
- Create a bone mask and clean it up as demonstrated in the lecture. There, we only retained the largest component. Visualise the different labelled components.
- Generate a surface mesh from the mask and smooth it. Experiment with the smoothing parameters to find suitable values.
- For each vertex of the mesh, identify all bone voxels within a radius of 1 cm and calculate their average density. Finally, visualise the bone density on the surface mesh in a 3D plot.
