# 09 Exercises: Scientific Tools Solution

## Task 01

```python
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA


data = np.loadtxt('src/observations.csv', delimiter=',', skiprows=1)

idx = data[:, 0]
xyz = data[:, 1:]

pca = PCA(n_components=3)
pca.fit(xyz)
```

```python
fig = plt.figure(layout='tight')
ax_3d = fig.add_subplot(121, projection='3d')
ax_2d = fig.add_subplot(122)

for i, color in enumerate(('red', 'blue')):
    selection = idx == i
    ax_3d.scatter(*xyz[selection].T, s=2, alpha=0.15, color=color)

    projected = pca.transform(xyz)
    ax_2d.scatter(
        *projected[selection, :2].T, s=2,
        alpha=0.15, color=color, label=f'index = {i}'
    )

for i, direction in enumerate(pca.components_, start=1):
    line = np.array([
        pca.mean_ - 10 * direction,
        pca.mean_ + 10 * direction
    ])
    
    ax_3d.plot(*line.T, lw=2, label=f'PC {i}')

ax_3d.set(xlabel='x', ylabel='y', zlabel='z')
ax_3d.set_aspect('equal')
ax_3d.legend()

ax_2d.set(xlabel='PC 1', ylabel='PC 2')
ax_2d.legend(markerscale=4)
```

## Task 02

```python
from scipy.io import wavfile


pressure = np.load('src/pressure.npy')

audio = (pressure - pressure.mean()).astype(int)
wavfile.write('audio.wav', 44_100, audio)
```

```python
import scipy.fft

fig, ax = plt.subplots()

fs, audio = wavfile.read('audio.wav')
segments = audio[:(len(audio) // fs) * fs].reshape((-1, fs))

for second, segment in enumerate(segments):
    fft = scipy.fft.rfft(segment * np.hanning(fs))
    freq = scipy.fft.rfftfreq(n=fs, d=1/fs)
    spectrum = np.abs(fft)
    peak_idx, *_ = scipy.signal.find_peaks(spectrum, prominence=spectrum.max() / 10)

    sizes = 50 * (spectrum[peak_idx] / spectrum.max()) ** 2
    plt.scatter([second]*len(peak_idx), freq[peak_idx], s=sizes, c='C0')

ax.set_xlabel('Time (s)')
ax.set_ylabel('Frequency (Hz)')
ax.set_yscale('log')
```

```python
fig, ax = plt.subplots()
*_, im = ax.specgram(audio, Fs=fs, NFFT=8_192, cmap='magma', vmin=-60, vmax=40)

ax.set(xlabel='Time (s)', ylabel='Frequency (Hz)')
ax.set_yscale('log')
ax.set_ylim(20, 16_000)
```

FYI: This is a Shepard–Risset tone: several components, spaced an octave apart, rise together. High-frequency components fade out while low-frequency components fade in. The pattern repeats after about 10 seconds, creating the illusion of an endlessly rising pitch.

## Task 03

```python
import SimpleITK as sitk
import scipy.ndimage


image = sitk.ReadImage('src/600001.nii.gz')
image = sitk.Shrink(image, [2, 2, 2])
ct = sitk.GetArrayFromImage(image)

bone = ct > 100
bone = scipy.ndimage.median_filter(bone, size=3)
bone = scipy.ndimage.binary_closing(bone)

labels, n = scipy.ndimage.label(bone)
sizes = np.bincount(labels.ravel())
sizes[0] = 0  # Ignore background

bone = labels == sizes.argmax()
```

```python
import trimesh
from skimage.measure import marching_cubes


# note: [::-1] because SITK indexes as z, y, x, while
#       scikit-image uses x, y, z
spacing = np.array(image.GetSpacing())[::-1]
verts, faces, _, _ = marching_cubes(bone, level=0.25, spacing=spacing)

verts = verts[:, ::-1]
mesh = trimesh.Trimesh(vertices=verts, faces=faces)


trimesh.smoothing.filter_laplacian(mesh, lamb=0.25, iterations=15)

mesh.show()
```

```python
from tqdm.auto import tqdm


radius = 10

# note: We use ct.T to create a grid in x, y, z order.
coords = np.indices(ct.T.shape).T * image.GetSpacing()

# note: This is the straightforward approach. It works, but takes
#       hours. Other approaches can do the same in a few seconds.
density = np.zeros(len(mesh.vertices))
for i, vertex in enumerate(tqdm(mesh.vertices)):
    distance = np.linalg.norm(coords - vertex, axis=-1)
    selection = bone & (distance <= radius)
    density[i] = ct[selection].mean() if selection.any() else np.nan
```

```python
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

surf = ax.plot_trisurf(*mesh.vertices.T, triangles=mesh.faces, cmap='magma', linewidth=0)

surf.set_array(density[mesh.faces].mean(axis=1))
surf.set_clim(density.min(), density.max())

ax.set_aspect('equal')
ax.zaxis.set_inverted(True)
ax.set_title('Local bone density')
fig.colorbar(surf, ax=ax, label='Density (HU)', shrink=0.6)
```
