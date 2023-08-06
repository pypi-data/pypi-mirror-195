from distutils.core import setup

from setuptools import find_packages

from rosreestr2coord.version import VERSION

setup(
    name="rosreestr2coord",
    version=VERSION,
    packages=find_packages(exclude=["tests*"]),
    zip_safe=False,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    description="Get geometry from rosreestr",
    long_description="Get area coordinates by its cadastral number",
    install_requires=[
        "numpy",
        "Pillow==9.2.*",
        "opencv-contrib-python==4.5.3.56",
    ],
    url="https://github.com/rendrom/rosreestr2coord",
    author="Artemiy Doroshkov",
    author_email="rendrom@gmail.com",
    entry_points={
        "console_scripts": [
            "rosreestr2coord=rosreestr2coord.console:console",
        ],
    },
)

# https://pypi.python.org/pypi/twine

# pip install twine
# python setup.py sdist bdist_wheel
# twine upload dist/*
# twine upload -u 'rendrom' --repository-url https://upload.pypi.org/legacy/ dist/*
# twine upload --repository r2c dist/*
