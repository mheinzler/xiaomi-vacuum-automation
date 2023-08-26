import importlib.util
import os
import sys

# we need to construct the module path relative to the project directory
project_dir = os.path.dirname(__file__)
dreame_path = (
    'dreame_vacuum/custom_components/dreame_vacuum/dreame/__init__.py')

# manually import the dreame subdirectory to avoid all references to Home
# Assistant
dreame_spec = importlib.util.spec_from_file_location(
    'dreame',
    os.path.join(project_dir, dreame_path))
dreame = importlib.util.module_from_spec(dreame_spec)

sys.modules['dreame'] = dreame
dreame_spec.loader.exec_module(dreame)
