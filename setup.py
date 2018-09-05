from cx_Freeze import setup,Executable
import sys
import os
 
base=None
if sys.platform=='win32':
    base='Win32GUI'

os.environ['TCL_LIBRARY'] = r'C:\Program Files (x86)\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files (x86)\Python36-32\tcl\tk8.6'
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))    

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Shoot Rocks 0.3 Stars Edition",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]sr_main.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}

options = {
    'build_exe': {
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
            'sp-0.2.1.gif',
            'asteroid40x40.gif',
            'asteroid-extra.gif',
            'cosm.gif',
         ],
    },
    "bdist_msi": bdist_msi_options
}

setup(options=options, name='ShootRocks',
      version='0.3',
      author='fluxoid <ifi@yandex.ru>, jazzard <deathwingstwinks@gmail.com>',
      executables=[Executable(
          script='sr_main.py',
          base=base,
          )])
