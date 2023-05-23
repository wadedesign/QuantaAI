# slash_commands/__init__.py
from os.path import dirname, basename, isfile
import glob

# Import all .py files inside the slash_commands folder
__all__ = [basename(f)[:-3] for f in glob.glob(dirname(__file__) + "/*.py") if isfile(f) and not f.endswith('__init__.py')]