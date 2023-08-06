from setuptools import setup, find_packages

VERSION = '0.0.3'
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
    install_requires=['httpx','pycryptodome','Pillow',"setuptools>=61.0","psutil","pyperclip","requests"],
    keywords=['python'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
    ]
)