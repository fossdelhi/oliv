from setuptools import setup

setup(name="oliv", version='0.1', py_modules=['oliv'],
      install_requires=['Click', ],
      entry_points='''[console_scripts]
                   oliv=oliv:oliv
                   ''',)
