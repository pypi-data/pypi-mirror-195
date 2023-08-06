from setuptools import setup, find_packages

setup(
    name            = 'rk_extractor',
    version         = '0.0.2',
    description     = 'Used to extract RK from simultaneous fits',
    long_description= '',
    pymodules       = ['extractor'],
    package_dir     = {'' : 'src'},
    install_requires= [
        'numpy',
        'matplotlib',
        'logzero',
        'zfit',
        'generic-analysis-scripts'
    ],
)


