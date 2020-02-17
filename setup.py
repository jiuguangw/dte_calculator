import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dte_calculator",  # Replace with your own username
    version="0.0.1",
    author="Jiuguang Wang",
    author_email="jw@robo.guru",
    description="Python based utility to compare electric service plans based on past consumption data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiuguangw/dte_calculator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
