from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='epic-by-tom-tkacz',
    version='0.0.2',
    descript='Say epic!',
    py_modules=["epic"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={
        "dev": [
            "pytest>=3.7",
        ]
    },
    url="https://github.com/TomTkacz/epic",
    author="Tom Tkacz",
    author_email="thomasatkacz@gmail.com",
)