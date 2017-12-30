import cx_Freeze

#executables = [cx_Freeze.Executable("main_v2.py")]
import os 
os.environ['TCL_LIBRARY'] = "C:\\Users\\Nohan\\AppData\\Local\\Programs\\Python\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Nohan\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tk8.6"


cx_Freeze.setup(
	name="Loumo",
	options={"build_exe":{"packages":["tkinter","threading","socket","os","struct","menu","client","time"],"include_files":[r"C:\Users\Nohan\AppData\Local\Programs\Python\Python35-32\DLLs\tcl86t.dll",r"C:\Users\Nohan\AppData\Local\Programs\Python\Python35-32\DLLs\tk86t.dll"]}},
	description="AHAHAHAHAHAHA",
	version="1.0",
	executables=[cx_Freeze.Executable("Loumo.py")]

	)
