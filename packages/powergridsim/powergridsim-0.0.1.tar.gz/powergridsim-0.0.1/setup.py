from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Simulation of Unit Commitment and Economic Dispatch in Real Power Grids'

# Setting up
setup(
    name="powergridsim",
    version=VERSION,
    author="Junying (Alice) Fang",
    author_email="jf3187@columbia.edu",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['python'],
    keywords=['python', 'optimization', 'grid', 'electricity', 'energy', 'unit commitment', 'economic dispatch'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)