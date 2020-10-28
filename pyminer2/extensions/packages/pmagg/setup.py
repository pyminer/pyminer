import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="jcl_pypi",
    version="0.0.1",
    author="jcl",
    author_email="2195932461@qq.com",
    description="A matplotlib GUI backend with interactive capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cl-jiang/pmagg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
