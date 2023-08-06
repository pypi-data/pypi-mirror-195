import pathlib, sys
import pytest

cwd = pathlib.Path.cwd()

# Add the project's root directory to the system path
sys.path.append(str( cwd.parent ))

# Add a lib directory 
# To the system path for tests to be able to use
sys.path.append(str( cwd / 'tests_data' ))

pytest.main()
