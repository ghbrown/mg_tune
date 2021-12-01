
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mgtune',  
    version='0.0.0',
    scripts=['bin/mgtune'] ,
    author="Gabriel H. Brown",
    author_email="gabriel.h.brown@gmail.com",
    description="Automatic tuning of multigrid parameters using black box optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghbrown/sheetSparse",
    packages=setuptools.find_packages(),
    #include_package_data = True, #include non-Python files specified in MANIFEST.in
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    keywords=[
        "multigrid",
        "autotuning"
        "engineering",
    ],
    install_requires=[
        "numpy",
        "pyamg",
        "matplotlib",
    ],
 )
