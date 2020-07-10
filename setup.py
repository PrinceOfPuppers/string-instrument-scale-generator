import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="string-theory", # Replace with your own username
    version="0.0.1",
    author="Joshua McPherson",
    author_email="joshuamcpherson5@gmail.com",
    description="A tool for generating maps of scales on any non-microtonal string instrument",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PrinceOfPuppers/string-theory",
    packages=setuptools.find_packages(),
    install_requires=[
          'numpy',
          'matplotlib'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
        "Framework :: Matplotlib"
    ],
    python_requires='>=3.6',
    scripts=["string_theory/string-theory.py"]
)