# 08 Exercises: Data Visualisation Solution

## Task 01

```python
import matplotlib.pyplot as plt
import numpy as np
```

```python
def lissajous(a, b, d):
    t = np.linspace(0, 2 * np.pi, 1_000)
    x = np.sin(a * t + d)
    y = np.cos(b * t)

    return x, y


fig, axes = plt.subplots(6, 4, figsize=(4, 6), layout='constrained')

fig.suptitle('Lissajous curves')


ratios = [(1, 1), (1, 2), (1, 3), (2, 3), (3, 4), (3, 5), (3, 6)]
deltas = np.arange(4) * np.pi / 4

for row, (a, b) in zip(axes, ratios):
    row[0].set_ylabel(f'{a}:{b}', fontsize=10)

    for ax, delta in zip(row, deltas):
        ax.plot(*lissajous(a, b, delta), lw=1)
        ax.fill(*lissajous(a, b, delta), alpha=0.1)
        ax.set_xticks([])
        ax.set_yticks([])

for ax, delta in zip(axes[0], deltas):
    ax.set_title(f'{delta / np.pi:g} π', fontsize=10)
```

## Task 02

```python
idx, x, y = np.loadtxt('src/observations_a.csv', delimiter=',').T

fig, axes = plt.subplots(
    2,
    2,
    figsize=(6, 6),
    sharex='col',
    sharey='row',
    gridspec_kw=dict(width_ratios=[1, 4], height_ratios=[4, 1], wspace=0.05, hspace=0.05),
)

(ax_y, ax_2d), (empty, ax_x) = axes
empty.axis('off')

hist_style = dict(bins=50, density=True, alpha=0.4)

for i, color in enumerate(('C0', 'C1')):
    selection = idx == i
    ax_2d.scatter(
        x[selection], y[selection], s=2, alpha=0.125, color=color, label=f'index = {i}'
    )

    ax_x.hist(x[selection], color=color, **hist_style)
    ax_y.hist(y[selection], orientation='horizontal', color=color, **hist_style)

ax_y.invert_xaxis()
ax_2d.legend(markerscale=4)

ax_x.set_xlabel('x')
ax_y.set_ylabel('y')

plt.show()
```

## Task 03

```python
z = np.loadtxt('src/observations_b.csv')
```

```python
# interactive mode helps to get a quick overview

%matplotlib widget


fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(projection='3d')

ax.scatter(x, y, z, s=1, alpha=0.125, c=idx)

ax.set(xlabel='x', ylabel='y', zlabel='z')
```

```python
# lets try a simple threshold classification
z_split = z.mean()
prediction = (z <= z_split).astype(bool)

fig, (ax_z, ax_scatter) = plt.subplots(
    2,
    1,
    figsize=(6, 6),
    sharex=True,
    gridspec_kw=dict(height_ratios=[1, 4], hspace=0.05),
)


for i, color in enumerate(('C0', 'C1')):
    selection = idx == i

    ax_z.hist(z[selection], color=color, label=f'index = {i}', **hist_style)

    ax_scatter.scatter(
        z[selection],
        x[selection],
        color=color,
        s=2,
        alpha=0.2,
    )

wrong = prediction != idx
ax_scatter.scatter(
    z[wrong],
    x[wrong],
    s=20,
    facecolors='none',
    edgecolors='red',
    linewidths=0.75,
)

ax_z.axvline(z_split, color='black', ls=':', lw=1)
ax_scatter.axvline(z_split, color='black', ls=':', lw=1)

fig.legend()
ax_scatter.set_xlabel('z')
ax_scatter.set_ylabel('x')
```

## Task 04

```python
# if you want to download through python as well
# url = "https://www.nlm.nih.gov/exhibition/historicalanatomies/Images/1200_pixels/cheselden_t32.jpg"
# urllib.request.urlretrieve(url, "src/skeleton.jpg")

img = plt.imread('src/skeleton.jpg')
h, w = img.shape[:2]

fig, ax = plt.subplots(figsize=(6, 8), layout='constrained')
ax.imshow(img)
ax.set_axis_off()
ax.set_title('William Cheselden — Osteographia (1733)')

# Coordinates as fractions of image width and height
bones = [
    ('Skull', (0.52, 0.15), (0.68, 0.13)),
    ('Ribs', (0.53, 0.38), (0.69, 0.41)),
    ('Pelvis', (0.52, 0.51), (0.68, 0.54)),
    ('Femur', (0.34, 0.61), (0.13, 0.62)),
    ('Tibia', (0.44, 0.75), (0.65, 0.73)),
]

for name, xy, text in bones:
    ax.annotate(
        name,
        xy=(xy[0] * w, xy[1] * h),
        xytext=(text[0] * w, text[1] * h),
        arrowprops=dict(arrowstyle='->', color='black'),
        color='black',
        fontsize=10,
    )
```
