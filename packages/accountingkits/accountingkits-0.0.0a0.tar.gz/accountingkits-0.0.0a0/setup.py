import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='accountingkits',
    version='0.0.0.alpha',
    description='The kit-package which made for accounting science research',
    author='zhang qihang',
    author_email='694499657@qq.com',
    url='https://github.com/qihangZH/accountingkits',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
