import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\Boris\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Boris\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

include_files = [r"C:\Users\Boris\AppData\Local\Programs\Python\Python36-32\DLLs\tcl86t.dll",
                 r"C:\Users\Boris\AppData\Local\Programs\Python\Python36-32\DLLs\tk86t.dll"]


cx_Freeze.setup(
    name="Train",
    version="0.1",
    options={'build_exe': {'includes': ['numpy.core._methods',
                                        'numpy.lib.format',
                                        "matplotlib.backends.backend_tkagg",
                                        "tkinter"],
                           'include_files': include_files}},
    description="Train",
    executables=[cx_Freeze.Executable("Gist.py")]
)
