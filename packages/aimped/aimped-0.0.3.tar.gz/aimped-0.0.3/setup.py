import setuptools

setuptools.setup(
    name="aimped",
    version="0.0.3",
    author="Russell C.",
    author_email="russell@aimped.com", 
    description="A small NLP package with nlp classes and functions",
    long_description="Aimped is a unique library that provides both inference and training classes and functions for only exclusively business-tailored AI-based NLP models.",
    long_description_content_type="text/markdown",
    url="https://dev.ml-hub.nioyatechai.com/", 
    packages=setuptools.find_packages(),
    install_requires=[ 'nltk', 'numpy', 'pandas' ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
