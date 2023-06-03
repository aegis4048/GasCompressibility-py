import os
import sys
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"src"
)
sys.path.append(SOURCE_PATH)

# python -m unittest discover .

# python -m unittest tests.test_gascomp2