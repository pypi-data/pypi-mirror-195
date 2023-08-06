from setuptools import setup, find_packages

setup(
    name='hyc-utils',
    version='0.5.29',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'statsmodels',
        'torch',
        'tomli',
        'h5py',
        'pandas',
        'tables', # optional dependency for pandas
        'tqdm',
        'mat73',
        'platformdirs',
    ],
    extras_require={
        'test': ['pytest', 'scipy'],
    },
    include_package_data=True,
)
