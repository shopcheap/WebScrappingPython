import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.


# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Adder",
        version = "0.1",
        
      
        executables = [Executable("build.py", base=base)])