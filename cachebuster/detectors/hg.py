from mercurial import ui, hg
from mercurial.mode import hex

def unique_string(_file):
    base_dir = original_dir = os.path.dirname(os.path.abspath(file))
    while True:
        hg_dir = os.path.normpath(os.path.join(base_dir, '.hg'))
        if os.path.isdir(hg_dir):
            break

        new_base_dir = os.path.dirname(base_dir)

        # if they are the same, then we've reached the root directory and
        # can't move up anymore - there is no .git directory.
        if new_base_dir == base_dir:
            raise EnvironmentError, "django-cachebuster could not find a '.hg' directory in your project path. (Moving up from %s)" % original_dir

        base_dir = new_base_dir
    repo = hg.repository(ui.ui(), repo_path)
    ctx = repo[None]
    changeset = ctx.parents()[0]
    return hex(changeset.node())
