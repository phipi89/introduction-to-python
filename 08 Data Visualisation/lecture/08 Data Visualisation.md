# 08 Data Visualisation

## TL;DR

```python
import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(0, 2*np.pi)
y = np.sin(x)

plt.plot(x, y)
plt.show()
```

## More than a thousand words

```python
import numpy as np

# Hours of practice
hours = np.array([4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

# Performance scores for three training methods
method_a = np.array([4.26, 5.68, 7.24, 4.82, 6.95, 8.81, 8.04, 8.33, 10.84, 7.58, 9.96])
method_b = np.array([3.10, 4.74, 6.13, 7.26, 8.14, 8.77, 9.14, 9.26, 9.13, 8.74, 8.10])
method_c = np.array([4.07, 4.68, 9.37, 5.91, 6.52, 7.13, 7.74, 8.35, 8.96, 9.58, 10.17])
```

```python
def print_stats(x, y):
    slope, intercept, r, *_ = scipy.stats.linregress(x, y)

    print(f"mean x/y:      {np.mean(x):.2f} / {np.mean(y):.2f}")
    print(f"variance x/y:  {np.var(x):.2f} / {np.var(y):.2f}")
    print(f"correlation:   {r:.3f}")
    print(f"linear fit:    y = {slope:.1f}x + {intercept:.1f}")
    print(f"R²:            {r**2:.3f}")


#                  method_a          method_b          method_c

# mean x/y:        9.00 / 7.50       9.00 / 7.50       9.00 / 7.50   
# variance x/y:    10.00 / 3.75      10.00 / 3.75      10.00 / 3.75  
# correlation:     0.816             0.816             0.816         
# linear fit:      y = 0.5x + 3.0    y = 0.5x + 3.0    y = 0.5x + 3.0
# R²:              0.667             0.667             0.667         
```

```python
import matplotlib.pyplot as plt


for score in methods:
    plt.plot(hours, score)
```

![Cell output](media/08%20matplotlib_a.png)

Visualising data is an indispensible tool to understand its shape. Note how by default, this looks incredibly ugly; we'll fix that later, but first lets understand how `matplotlib` is set up.

## Matplotlib

### Object-oriented setup

Matplotlib is the most widely used library for data visualisation in Python. As the name still suggests, Matplotlib was originally designed to give MATLAB-like plotting experience. This style is what we used above: There's an implicit creation of a figure, and all subsequent calls modify that figure.

This notation is helpful for quick looks at data, because its very minimal. However it quickly reaches limits. Therefore, its recommended to use an the modern object-oriented style, where we explicitly objects that represent elements of the figures, and manipulate those.

In the example below, we explicitly create a figure with three axes. In this object-oriented notation, we can reference all elements to attach for example scatter and line plots, labels, titles etc. This gives us very specific control over these objects.

Matplotlib is very capable, but also quite the mess for historic reasons. Note for example the inconsistency between the naming of `ax.set_title` and `fig.suptitle`… it is what it is!

```python
fig, axes = plt.subplots(1, 3, sharey=True, figsize=(6, 4), layout='tight')

for i, ax in enumerate(axes):
    performance = methods[i]
    ax.set_title('method ' + 'ABC'[i])

    ax.scatter(hours, performance)

    a, b, *_ = sp.stats.linregress(hours, performance)
    ax.plot(hours, a * hours + b, c='red', ls=':')

axes[0].set_ylabel('performance (%)')
axes[1].set_xlabel('training (h)')
fig.suptitle('Performance comparison')

fig.show()
```

![Cell output](media/08%20matplotlib_b.png)

Nevertheless its quirks, I really encourage you to familiarise with Matplotlib's most important concepts. For explorative data analysis as well as for quick "on the fly" checks (e.g., that the data you're working on / transforming is what you expect it), plotting is indispensible.

Once you internalised these concepts, You'll often be faster to just write visualisations in Python over requesting them through coding LLMs. Especially after a couple of iterations through a plot, gen-ai code will be \<unübersichtlich>ly verbose.

### Plot Anatomy

Conceptually, a Matplotlib *figure* is the entire canvas. A figure can contain one or more *axes* objects, each representing an individual plotting area. Each axes can hold multiple plots, such as lines, scatter points, or filled regions. Elements like axis labels, ticks, and grids belong to individual axes, while others, such as legends and colorbars, can also be associated with the entire figure.

Plots are created by calling the corresponding method on an axes object (e.g., `ax.plot`). These methods take the data to be plotted and accept optional keyword arguments (e.g., `lw=2`) to control its appearance.

Further customisation, such as setting axis labels or limits, is done through methods on the axes and figure objects. Many of these are *setter* methods, such as `ax.set_xlabel` or `ax.set_ylim`.

Overall, the typical workflow in Matplotlib is:

1. **Create** a figure and one or more axes using `plt.subplots`.
2. **Plot** data using methods such as `ax.plot`.
3. **Style** the plots using optional keyword arguments.
4. **Configure** labels, ticks, legends, and other elements through methods on the axes or figure.

```python
fig, ax = plt.subplots(figsize=(6, 4), layout='tight')

fig.suptitle('Figure title')
ax.set_title('Axes title')

x = np.linspace(0, 2 * np.pi)
ax.plot(x, np.sin(x), lw=2, ls=':', label='sine(x)')
ax.plot(x, np.cos(x) / x, label='cos(x) / x')

ax.set_ylim([-1.25, 1.25])

ax.set_xlabel('horizontal axes label')
ax.set_ylabel('vertical axes label')

ax.grid(alpha=0.25)
ax.legend(loc='upper right')

ticks = np.arange(0, 7, np.pi/2)
ax.set_xticks(ticks, [f'{x / np.pi:g} π' for x in ticks])

fig.show()
```

![Cell output](media/08%20plot%20anatomy.png)

### Themes and Style

One annoyance of Matplotlib is, that it does not looks a bit dated by default. The first figure in this example did use the default style; subsequent figures used a custom style that looks a bit more modern. Alternative styles are straightforward to setup trough a text file. Below is an example of such a file.

```text
# clean.mplstyle

font.size: 10
font.family: DejaVu Serif
axes.labelsize: 9
axes.titlesize: 10
axes.edgecolor: "#CCCCCC"
axes.linewidth: 0.5
axes.prop_cycle: cycler('color', ['636efa', 'ef553b', '00cc96', 'ab63fa', 'ffa15a', '19d3f3', 'ff6692', 'b6e880', 'ff97ff', 'fecb52'])
figure.labelsize: 9
grid.color: "#CCCCCC"
xtick.labelsize: 8
ytick.labelsize: 8
xtick.color: "#CCCCCC"
ytick.color: "#CCCCCC"
xtick.labelcolor: "#444444"
ytick.labelcolor: "#444444"
xtick.major.width: 0.5
ytick.major.width: 0.5
xtick.minor.width: 0.5
ytick.minor.width: 0.5
legend.fontsize: 8
legend.edgecolor: "#CCCCCC"
legend.borderpad: 0.5
legend.borderaxespad: 0.5
legend.framealpha: 0.8
legend.frameon: False
legend.fancybox: False
```

I recommend to define your own style to your liking. Styles can be loaded through `plt.style.use`, and then apply automatically to all subsequently created plots.

These style files help to apply a general style. For individual plots, you then typically want to customise specific details. As seen above, these are passed as keyword arguments, so a clean way to do that is to create a style `dict`, that is passed along the appropriate plot methods.

```python
plt.style.use('clean.mplstyle')


fig, ax = plt.subplots(figsize=(4.5, 4))

X, Y, Z = riemann_zeta(-3, 3)
zeta = ax.pcolormesh(X, Y, np.angle(Z), cmap='twilight')

style = dict(
    levels=1000,
    colors='white',
    linewidths=0.5,
    linestyles='dotted',
    alpha=0.5
)

ax.contour(X, Y, Z.real, **style)
ax.contour(X, Y, Z.imag, **style)

ax.set_xlabel('Re(s)')
ax.set_ylabel('Im(s)')
ax.set_title('Riemann zeta function ζ(s)')

fig.colorbar(zeta)
```

![Cell output](media/08%20Rieman.png)

### Types of Plots

Matplotlib supports a wide variety of plot types, from simple lines and scatter plots to statistical visualisations, vector fields, and 3D surfaces.

Below is an overview of the most common types. As we have seen, plots are drawn on an area called the axis, so we can stack arbitrary plots. This overview is not intended to be complete.

![Cell output](media/08%20plot%20types.png)

### Backends and Export Formats

Matplotlib uses different backends to render figures, depending on the environment. In Jupyter notebooks, figures can be embedded as static images or displayed as interactive plots. These options can be selected through the _magic_ command `%matplotlib`.

```python
x = np.linspace(0, 15, 10_000)
chirp = np.sin(x**2)

# static rasterised image
%matplotlib inline

fig, ax = plt.subplots()
ax.plot(x, chirp)
fig.show()


# interactive figure
%matplotlib widget

fig, ax = plt.subplots()
ax.plot(x, chirp)
fig.show()


# write to file
fig.savefig('figure.png')       # rasterised
fig.savefig('figure.pdf')       # vectorised
```

Finally, figures can be exported with `fig.savefig('filename.ext')`. Depending on the file extension, Matplotlib automatically selects between rasterised output (e.g., `.png`) or vector graphics (e.g., `.pdf`).
