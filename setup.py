import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iwan",
    version="0.1.0",
    author="vSir",
    author_email="weiguo341@gmail.com",
    description="iWAN client for Wanchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nevquit/iWAN",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "websocket-client>=0.58.0"
    ],
)
