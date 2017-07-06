from cx_Freeze import setup,Executable
import sys
import os
 
base=None
if sys.platform=='win32':
    base='Win32GUI'

os.environ['TCL_LIBRARY'] = r'C:\Program Files (x86)\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files (x86)\Python36-32\tcl\tk8.6'
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))    

options = {
    'build_exe': {
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
            'sp.gif',
         ],
    },
}

setup(options=options,name='ShootRocks',
      version='0.1.2',
      author='fluxoid <ifi@yandex.ru>, jazzard <deathwingstwinks@gmail.com>',
      executables=[Executable(script='sr_main.py',base=base)])