# By Mark Dgz 2023-06-20 
# run sample: python3 chkpyver.py 3.6.0
import sys

def check_python_version(required_version):
    if sys.version.startswith(required_version):
        print(f"Python {required_version} is installed.")
    else:
        print(f"Python {required_version} is not installed.")

    print(f"Current Python version: {sys.version}")
    print(f"Python installation path: {sys.executable}")

# Check if a command-line argument is provided
if len(sys.argv) > 1:
    version = sys.argv[1]
    check_python_version(version)
else:
    print("Please provide a Python version as a command-line argument.")
    print("As follows: python chkpyver.py 3.6.0")

