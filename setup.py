import setuptools

#-----------------------------------------------------------------------------
#  Copyright (c) 2020-2021, pyminer development team.

#  The full license is in the file LICENSE, distributed with this software.
#-----------------------------------------------------------------------------


NAME = 'pyminer'
VERSION = '2.1.2'
DESCRIPTION = 'pyminer, a component-based data mining framework.'
AUTHOR = 'pyminer development team'
AUTHOR_EMAIL = 'team@pyminer.com'
HOMEPAGE = 'www.pyminer.com'
URL = 'https://gitee.com/py2cn/pyminer'
BUG_TRACKER = 'https://gitee.com/py2cn/pyminer/issues'


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    project_urls={
        "Bug Tracker": BUG_TRACKER,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Visualization",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
    ],
    packages=['pyminer'],
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'scikit-learn',
        'seaborn',
        'matplotlib',
        'pyside2',
        'openpyxl',
        'xlrd',
        'sqlalchemy',
        'jedi',
        'json-rpc',
        'qtconsole',
        'certifi',
        'cycler',
        'et-xmlfile',
        'helpdev',
        'jdcal',
        'joblib',
        'kiwisolver',
        'Pillow',
        'pymysql',
        'pyparsing',
        'pyreadstat',
        'python-dateutil',
        'pytz',
        'six',
        'threadpoolctl',
        'pywin32',
        'Werkzeug',
        'requests',
        'tornado',
        'matgen',
        'yapf',
        'configparser',
        'send2trash',
        'sympy',
        'lxml',
        'cloudpickle',
        'ghp-import',
        'pyqtgraph',
        'watchdog',
        'python-docs-theme',
        'waitress',
        'sshtunnel',
        'flask',
        'markdown',
        'flake8',
        'psycopg2',
        'networkx',
        'flask-cors',
        'notebook',
        'sliceable-generator',
        'fsspec',
        'cx_Oracle',
        'pyminer_comm',
        'ipyparams',
        'pathspec',
        'codegen',
        'chardet',
        'parso',
        'QDarkStyle',
        'build',
        'twine',
    ],
    
)