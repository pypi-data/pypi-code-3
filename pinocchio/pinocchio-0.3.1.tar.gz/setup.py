from setuptools import setup

setup(
    name='pinocchio',
    version="0.3.1",
    description = 'pinocchio plugins for the nose testing framework',
    author = 'C. Titus Brown and Michal Kwiatkowski',
    author_email = 'titus@idyll.org,michal@trivas.pl',
    license = 'MIT',

    url = 'https://github.com/mkwiatkowski/pinocchio',

    long_description = """\
Extra plugins for the nose testing framework.  Provides tools for flexibly
assigning decorator tags to tests, choosing tests based on their
runtime, doing moderately sophisticated code coverage analysis
of your unit tests, and making your test descriptions look like
specifications.
""",

    packages = ['pinocchio'],
    entry_points = {
        'nose.plugins': [
            'figleaf-sections = pinocchio.figleaf_sections:FigleafSections',
            ],
        'nose.plugins.0.10': [
            'decorator = pinocchio.decorator:Decorator',
            'output-save = pinocchio.output_save:OutputSave',
            'spec = pinocchio.spec:Spec',
            'stopwatch = pinocchio.stopwatch:Stopwatch',
        ]},
)
