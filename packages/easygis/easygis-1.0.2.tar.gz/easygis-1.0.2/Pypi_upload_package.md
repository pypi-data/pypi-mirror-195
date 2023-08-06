### Installation
pip install twine
python -m pip install --upgrade build

### Build package
Step 1: 
    $ python setup.py sdist
Step 2:
    $ python setup.py bdist_wheel --universal

### Upload to Pypi
    $ twine upload .\dist\easygis-1.0.1.tar.gz