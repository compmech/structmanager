"""
Documentation Utilities
=======================

There are some documentation utilities designed to automatically search for
Python scripts and automatically generate documentation based on Unix scripts,
not implemented in Sphinx yet.

They can be imported from inside the ``conf.py`` file, and are contained in the
``utils.py`` module, as detailed below.

"""
import os
import shutil
from subprocess import Popen, PIPE
from glob import glob


def process_docstring(app, what, name, obj, options, lines):
    """Process docstring before it is printed

    Parameters
    ----------
    app : object
        The Sphinx application object.
    what : str
        The type of the object which the docstring belongs to (noe of "module",
        "class", "exception", "function", "method", "attribute").
    name : str
        The fully qualified name of the object.
    obj : object
        The object itself.
    options : sphinx.ext.autodoc.Options
        The options given to the directive
    lines : list
        The lines of the docstring

    """
    text = '\n'.join(lines)

    check = False

    # ADD EXTRA CHECKS HERE, using %help% or any identifier along the
    # documentation

    if not check:
        return

    newlines = text.split('\n')

    if len(lines) > len(newlines):
        for _ in range(len(lines) - len(newlines)):
            lines.pop(-1)
        for i in range(len(lines)):
            lines[i] = newlines[i]

    if len(lines) < len(newlines):
        for _ in range(len(newlines) - len(lines)):
            lines.append('')
        for i in range(len(lines)):
            lines[i] = newlines[i]


def create_task_list(to_do_fname, keyword='TODO'):
    """Creates a task list based on keywords in the source code

    Parameters
    ----------
    to_do_fname : str
        The file name for the TODO list.
    keyword : str, optional
        The string indicating a "to do" task.

    Examples
    --------
    Creating a ``TODO`` list::

        create_task_list("_TODO_list.rst", keyword="TODO")

    Creating a ``FIXME`` list::

        create_task_list("_FIXME_list.rst", keyword="FIXME")

    """
    print 'utils.py HERE'
    with open(to_do_fname, 'w') as f:
        f.write(keyword + ' list\n')
        f.write('='*len(keyword) + '=====\n')
        f.write('\n')
        for root, dirs, files in os.walk(r'../../feopt'):
            last = root.split(os.sep)[-1]
            for fname in files:
                if '.pyc' in fname:
                    continue
                path = os.path.join(root, fname)
                with open(path) as p:
                    count = 0
                    for line in p:
                        if keyword in line:
                            count += 1
                    if count > 0:
                        name = os.path.join(last, fname).replace('\\', '/')
                        f.write('\n')
                        f.write('- **feopt/%s**: %d entries\n' % (name, count))
                        f.write('\n')

if __name__ == '__main__':
    create_task_list('tmp_test_tmp.rst', keyword='TODO')




