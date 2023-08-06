# python setup.py sdist
# tar --list -f dist/micropeutist-1.0.tar.gz

import setuptools

def parse(filename) -> list:
    ''' read file and put lines to list'''
    result =[]
    with open(filename) as file:
        for line in file:
            result.append(line[:-1:])
    return result

setuptools.setup(
    name='micropeutist',
    version='1.0',
    long_description=__doc__,
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=parse('requirements.txt'),
    tests_require=['pytest'],
    )
