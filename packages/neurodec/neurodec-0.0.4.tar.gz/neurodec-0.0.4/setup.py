from setuptools import setup

setup(
    name='neurodec',
    version='0.0.4',
    packages=['neurodec', 'neurodec.cli', 'neurodec.mdt'],
    license='',
    author='neurodec',
    description='A Python package that provides access to all of the neurodec software tools.',
    scripts=['scripts/neurodec'],
    install_requires=[
        'appdirs',
        'werkzeug',
        'trimesh',
        'numpy',
        'requests',
        'scipy',
    ],
)
