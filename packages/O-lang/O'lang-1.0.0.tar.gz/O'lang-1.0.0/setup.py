import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="O'lang",                     # This is the name of the package
    version="1.0.0",                        # The initial release version
    author="Saurabh Satapathy",                     # Full name of the author
    author_email="saurabhsatapathy0@gmail.com",
    description="A fun programming language with odia keywords...",
    # Long description read from the the readme file
    long_description=long_description,
    long_description_content_type="text/markdown",
    # List of all python modules to be installed
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    # Minimum version requirement of the package
    python_requires='>=3.10.4',
    # Name of the python package
    py_modules=["olang", "olang_compiler", "strings_essentials"],
    # Directory of the source code of the package
    package_dir={'': 'olang/src'},
    install_requires=[],                    # Install other dependencies if any
    include_package_data=True
)
