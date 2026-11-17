import sys
import inspect
import linecache
from IPython.core.magics.code import extract_symbols


def _locate_source_path(class_name):
    """Return the file path where a class is defined."""

    for _, member in inspect.getmembers(class_name):
        if inspect.isfunction(member):
            expected = f'{class_name.__qualname__}.{member.__name__}'
            if member.__qualname__ == expected:
                return inspect.getfile(member)


def _extract_source_from_path(path, class_name):
    """Extract the source code for a class from a file."""

    src = ''.join(linecache.getlines(path))
    blocks = extract_symbols(src, class_name)
    return blocks[0][0]


def _sourcecode(obj):
    """Get the source code for a single class object."""

    path = _locate_source_path(obj)
    source =  _extract_source_from_path(path, obj.__name__)
    return source


def objects_to_sourcecode(*objects):
    """Return the concatenated source code for one or more class objects.
    
    Parameters
    ----------
    *objects : class or several classes
        All classes need to be defined within the same notebook.

    Returns
    -------
    sourcecode : str
        String containing the Python sourcecode of all objects, concatenated
        by newlines. 
    """

    for obj in objects:
        if not inspect.isclass(obj):
            raise ValueError('Only (one or more) classes can be provided.')
    try:
        sources = [_sourcecode(obj) for obj in objects]
        return '\n\n'.join(sources)
    except:
        raise RuntimeError(
            'Source extraction failed. Ensure you are in a Jupyter notebook and '
            'provide classes defined within that notebook. If issues persist, '
            'please let me know.'
        )
