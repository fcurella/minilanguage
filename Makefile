test:
    coverage run setup.py test

release:
    rm -rf dist
    python setup.py sdist bdist_wheel
    twine upload dist/*
