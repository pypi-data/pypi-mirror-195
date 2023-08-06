from distutils.core import setup


setup(
    name='polyloader',
    packages=['polyloader'],
    version='0.1',
    license='MIT',
    description = 'Loads polyfiles events to an event_dataframe',
    description_file = "README.md",
    author="Julien Braine",
    author_email='julienbraine@yahoo.fr',
    url='https://github.com/JulienBrn/PolyLoader',
    download_url = 'https://github.com/JulienBrn/PolyLoader.git',
    package_dir={'': 'src'},
    keywords=['python',  'logging'],
    install_requires=['event_dataframe'],
)