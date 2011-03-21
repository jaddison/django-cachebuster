__author__ = 'James Addison'

import os

def unique_string(file):
    # TODO: consider using 'inspect' to get the calling module rather than
    # forcing the user to pass it in.  It's passed in because we need to find the .git dir
    # for the calling module, not that of django-cachebuster!
    base_dir = original_dir = os.path.dirname(os.path.abspath(file))
    while True:
        git_dir = os.path.normpath(os.path.join(base_dir, '.git'))
        if os.path.isdir(git_dir):
            break

        new_base_dir = os.path.dirname(base_dir)

        # if they are the same, then we've reached the root directory and
        # can't move up anymore - there is no .git directory.
        if new_base_dir == base_dir:
            raise EnvironmentError, "django-cachebuster could not find a '.git' directory in your project path. (Moving up from %s)" % original_dir

        base_dir = new_base_dir

    # Read the HEAD ref
    fhead = open(os.path.join(git_dir, 'HEAD'), 'r')
    if fhead:
        ref = None
        try:
            line = fhead.readline().strip()
            ref_name = line.split(" ")[1].strip()

            # Read the commit id
            fref = open(os.path.join(git_dir, ref_name), 'r')
            if fref:
                ref = fref.readline().strip()
                fref.close()
        except IndexError:
            # if we get here, it means the git project is in a 'detached HEAD' state - ie. on a tag.
            # just get the commit hash from HEAD instead!
            ref = line.strip()

        fhead.close()
        
        if ref:
            return unicode(ref)

    raise EnvironmentError, "django-cachebuster ran into a problem parsing a commit hash in your .git directory. (%s)" % git_dir

