import importlib.util
import sys

# manually import the dreame subdirectory to avoid all references to Home
# Assistant
dreame_spec = importlib.util.spec_from_file_location(
    'dreame',
    './dreame_vacuum/custom_components/dreame_vacuum/dreame/__init__.py')
dreame = importlib.util.module_from_spec(dreame_spec)

sys.modules['dreame'] = dreame
dreame_spec.loader.exec_module(dreame)
