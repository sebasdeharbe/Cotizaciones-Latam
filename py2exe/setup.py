from distutils.core import setup
import py2exe
includes = ['requests', 'urllib3', 'bs4', 'xml','datetime','json','decimal','chardet','os','errno','pathlib']
excludes = []
packages = []
dll_excludes = []

setup(
    options ={"py2exe": {"compressed": 0,
                          "optimize": 0,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 1,
                          "dist_dir": ".",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
    },
    windows=[{
            'script': 'C:/Users/sebastian/Documents/Desarrollo-Pruebas/Cotizaciones/Proyecto Python/cotizaciones.py',
             'icon_resources': [(1, 'icon.ico')]     
    }]
)
