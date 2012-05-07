"""

    Yo dawg

"""

from setuptools import setup, find_packages

LONG_DESCRIPTION = open("README.rst").read() + "\n" + open("CHANGELOG.rst").read()

setup(name = "vvv",
    version = "0.2.4",
    long_description = LONG_DESCRIPTION,
    description = "A convenience utility for software source code validation and linting",
    author = "Mikko Ohtamaa",
    author_email = "mikko@opensourcehacker.com",
    url = "https://github.com/miohtama/vvv",
    install_requires = ["setuptools", 
        "PyYAML==3.10",
        "plac==0.9.0",
        "requests==0.11.1"
    ],
    packages = find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python",
    ],     
    license="GPL3+",
    # Don't install as zipped as we want to poke non-py files inside dist archive
    zip_safe = False,
    include_package_data = True,
    entry_points="""
      # -*- Entry points: -*-
      [vvv]
      tabs=vvv.validators.tabs:TabsPlugin
      linelength = vvv.validators.linelength:LineLengthPlugin
      css = vvv.validators.css:CSSPlugin
      jshint = vvv.validators.jshint:JSHintPlugin
      pylint = vvv.validators.pylint:PylintPlugin
      pdb = vvv.validators.pdb:PdbPlugin
      rst = vvv.validators.rst:RestructuredTextPlugin

      [console_scripts]
      vvv = vvv.main:entry_point
      stn = vvv.main:entry_point
      prkl = vvv.main:entry_point
      vvv-install-git-pre-commit-hook = vvv.hooks.git:setup_hook
      vvv-validate-rst = vvv.scripts.validaterst:run
      vvv-expand-tabs = vvv.scripts.expandtabs:run
      ghetto-ci = ghettoci.main:entry_point
      """,        
) 