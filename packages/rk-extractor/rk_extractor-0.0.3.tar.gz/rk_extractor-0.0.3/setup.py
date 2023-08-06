from setuptools import setup, find_packages

setup(
    name            = 'rk_extractor',
    version         = '0.0.3',
    description     = 'Used to extract RK from simultaneous fits',
    long_description= '',
    pymodules       = ['extractor', 'rkex_model'],
    package_dir     = {'' : 'src'},
    install_requires= [
        'numpy',
        'matplotlib',
        'logzero',
        'zfit',
        'generic-analysis-scripts >= 0.0.4'
    ],
)


