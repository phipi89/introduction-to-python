import matplotlib.pyplot as plt



def show_image_arrays(*imgs):
    """
    Display one or more 2D image arrays side by side in grayscale.

    Each input must be a 2D NumPy array. The function creates a single
    figure with one subplot per image, arranged horizontally.

    Parameters
    ----------
    *imgs : array_like
        One or more 2D NumPy arrays representing grayscale images.

    Raises
    ------
    ValueError
        If any of the provided arrays are not 2D.
    """

    for i, img in enumerate(imgs, start=1):
        if img.ndim != 2:
            raise ValueError(f'array {i} is not 2D.')


    fig = plt.figure()
    for i, img in enumerate(imgs, start=1):
        ax = plt.subplot(1, len(imgs), i)
        ax.imshow(img, cmap='gray')

    plt.show()
