__author__ = 'James Addison'

import os

def unique_string():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    while True:
        git_dir = os.path.normpath(os.path.join(base_dir, '.git'))
        if os.path.isdir(git_dir):
            break

        new_base_dir = os.path.dirname(base_dir)

        # if they are the same, then we've reached the root directory and
        # can't move up anymore - there is no .git directory.
        if new_base_dir == base_dir:
            return None

        base_dir = new_base_dir

    # Read the HEAD ref
    fhead = open(os.path.join(git_dir, 'HEAD'), 'r')
    ref_name = fhead.readline().split(" ")[1].strip()
    fhead.close()

    # Read the commit id
    fref = open(os.path.join(git_dir, ref_name), 'r')
    ref = fref.readline().strip()
    fref.close()

    return unicode(ref)
