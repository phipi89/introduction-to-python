# 09 Scientific Tools

## TL;DR

```python
def model(t, A, k):
    return A * np.exp(-k*t)

filtered = scipy.ndimage.gaussian_filter1d(y, sigma=2)
params, _ = scipy.optimize.curve_fit(model, t, filtered)
```

## Ecosystem

One of Python's greatest strengths is its ecosystem of scientific libraries. We don't need to implement everything ourselves: specialised packages provide tools for reading data, numerical computations, signal processing, optimisation, and visualisation.

In this lecture, we'll analyse two different examples. The aim is to get a feeling for how data exploration and scientific computing can be approached in Python, and what can be achieved with relatively little code.

## Signal Processing

### Electrocardiogram

Many scientific measurements are recorded as time series: sequences of numbers sampled at regular intervals. In this first example we'll have a look at an electrocardiogram (from https://doi.org/10.13026/kfzx-aw45). These come as a *Waveform Database* (WFDB). As is very often the case, someone already implemented a parser for us:

```python
import wfdb


# you'll find custom parsers for almost everything
data, info = wfdb.rdsamp('00001_hr')

fs = info['fs']
ecg = data[:, 0]
t = np.arange(len(ecg)) / fs

fig, ax = plt.subplots()
ax.plot(t, ecg, lw=0.5)
ax.set_xlabel('Time (s)')
ax.set_ylabel('ECG (mV)')
```

![Cell output](media/09%20ECG%2001%20raw.png)

You see that the underlying data is stored in a NumPy array. That's great, we already learned how to work with them.

Often, we want to extract particular events or features from a signal. SciPy provides a large collection of algorithms for such tasks, including peak detection, filtering, and frequency analysis.

```python
import scipy.signal


peaks, _ = scipy.signal.find_peaks(
    ecg,
    prominence=0.6,
)

plt.plot(t, ecg, lw=0.5)
plt.scatter(t[peaks], ecg[peaks], c='red', marker='x')

rr = np.diff(peaks) / fs
heart_rate = 60 / rr.mean()  # 63.9 BPM
```

![Cell output](media/09%20ECG%2002%20peaks.png)

This is a cyclic signal, so lets cut it up and overlay the pulses. Real-world measurements are rarely perfectly reproducible. By identifying repeated events, aligning them, and averaging them, we can reduce noise and reveal their common structure.

Notice how NumPy's vectorisation keeps that very simple.

```python
before = int(0.25 * fs)
after = int(0.4 * fs)

beats = np.array(
    [ecg[p - before : p + after]
     for p in peaks
     if p - before >= 0 and p + after <= len(ecg)]
)
beats -= beats.mean(axis=1)[..., np.newaxis]

t_beat = np.arange(-before, after) / fs

for beat in beats:
    plt.plot(t_beat, beat, alpha=0.3, lw=1)

mean_beat = beats.mean(axis=0)
plt.plot(t_beat, mean_beat, c='C1')
```

![Cell output](media/09%20ECG%2003%20sequenced.png)

A common goal in science is to describe observations using a mathematical model. Below, we define a function and let a numerical optimiser find the parameters that best explain the measured data.

```python
def gaussian(t, A, mu, sigma):
    return A * np.exp(-0.5 * ((t - mu) / sigma) ** 2)


def ecg_model(t, c, Ap, mp, sp, Ar, mr, sr, At, mt, st):
    return c + gaussian(t, Ap, mp, sp) + gaussian(t, Ar, mr, sr) + gaussian(t, At, mt, st)


p0 = [0, 0.1, -0.1, 0.02, 1, 0, 0.02, 0.1, 0.3, 0.02]  # initial guess
params, covariance = scipy.optimize.curve_fit(ecg_model, t_beat, mean_beat, p0=p0)

fig, ax = plt.subplots()
ax.plot(t_beat, mean_beat, '*', ms=2, alpha=0.5, label='Measured')
ax.plot(t_beat, ecg_model(t_beat, *params), label='Fitted')
ax.legend()
```

![Cell output](media/09%20ECG%2004%20fitted.png)

## Medical Images

### Hip CT

As a second example, we'll process a hip CT (from https://doi.org/10.5281/zenodo.20473746). This comes as a compressed NifTI image, and again, a parser for that data already exists. Lets first again plot the data.

```python
import SimpleITK as sitk


image = sitk.ReadImage('600001/600001.nii.gz')
image = sitk.Shrink(image, [2, 2, 2])
ct = sitk.GetArrayFromImage(image)


fig, axes = plt.subplots(6, 8)

for ax, i in zip(axes.ravel(), np.linspace(0, ct.shape[0] - 1, 8 * 6).astype(int)):
    im = ax.imshow(ct[i], vmin=-500, vmax=1000, cmap='gray')
    ax.axis('off')
```

![Cell output](media/09%20CT%2001%20sections.png)

We can exctract bony regions with thresholding, and clean up the resulting mask with morphological image processing.

```python
import scipy.ndimage


bone = ct > 100
bone = scipy.ndimage.median_filter(bone, size=3)
bone = scipy.ndimage.binary_closing(bone)

labels, n = scipy.ndimage.label(bone)
sizes = np.bincount(labels.ravel())
sizes[0] = 0  # Ignore background

bone = labels == sizes.argmax()
```

Once we have identified a structure in the image, we can convert it into a three-dimensional surface. See how different Python libraries work together: *SimpleITK* handles medical image formats, *scikit-image* and *scipy* processe the arrays, and *Trimesh* constructs and visualises geometric objects.

```python
import trimesh
from skimage.measure import marching_cubes


spacing = np.array(image.GetSpacing())[::-1]

verts, faces, _, _ = marching_cubes(bone, level=0.25, spacing=spacing)

verts = verts[:, ::-1]
mesh = trimesh.Trimesh(vertices=verts, faces=faces)


trimesh.smoothing.filter_laplacian(mesh, lamb=0.25, iterations=15)

mesh.show()
```

![CT segmentation](media/09%20CT%2002%20segmentation.png "Trimesh provides a built in simple way to visualise a 3D mesh.")

```python
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_trisurf(*mesh.vertices.T, triangles=mesh.faces, cmap='magma', linewidth=0)

ax.set_aspect('equal')
ax.zaxis.set_inverted(True)
fig.colorbar(surf, ax=ax, label='Z position', shrink=0.6)
```

![Cell output](media/09%20CT%2003%20colormap.png)

## Workflow

These examples should illustrate a common pattern in scientific programming: load data, explore it, transform it, extract information, and visualise the (intermediate) results.

Once you're comfortable working with arrays, functions, and libraries, the same basic Python skills transfer to an enormous range of scientific problems.

The key takeaway:

- _You rarely start from scratch._ wfdb, SimpleITK, and SciPy already implement much of the difficult functionality.
- _Arrays are the common language._ ECG recordings, CT volumes, detected peaks, and segmented structures are all represented as NumPy arrays.
- _Visualisation is part of the workflow._ Plotting intermediate results is essential to understand whether our calculations make sense.
