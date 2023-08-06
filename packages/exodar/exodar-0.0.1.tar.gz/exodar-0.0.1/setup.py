from setuptools import find_packages, setup

with open("./exodar/README.md", "r") as f:
    long_description = f.read()

setup(
    name="exodar",
    version="0.0.1",
    description="A test package",
    package_dir={"": "exodar"},
    packages=find_packages(where="exodar"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="vincent2303",
    author_email="vincent.martin23@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    extras_require={},
    python_requires=">=3.10",
)
