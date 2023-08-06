import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="Ddnet",
    version="0.0.5",
    author="Zichuana",
    author_email="2092653757@qq.com",
    description="This is a test. This project is not very useful!!!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zichuana/Ddnet",
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'matplotlib', 'numpy', 'scipy', 'pandas_profiling', 'folium', 'seaborn', 'random', 'os'],
    # add any additional packages that needs to be installed along with SSAP package.

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
