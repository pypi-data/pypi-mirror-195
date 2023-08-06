from setuptools import setup, find_packages

VERSION = '1.0.5'
DESCRIPTION = 'How about installing izda?'
LONG_DESCRIPTION = 'I created this simple library just because I was bored.'

# Setting up
setup(
    name="izda",
    version=VERSION,
    author="CollinIzDa",
    author_email="<info@collinizda.de>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pystyle'],
    keywords=['python', 'collinizda', 'CollinIzDa'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)