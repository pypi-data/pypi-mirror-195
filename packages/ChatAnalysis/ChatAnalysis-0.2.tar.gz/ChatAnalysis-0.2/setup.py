from setuptools import setup, find_packages

setup(
    name="ChatAnalysis",
    version="0.2",
    author="Parth Dilip Kambli",
    author_email="gulches.laptops_0m@icloud.com",  # using icloud email forwarding
    description="A package for analyzing chat messages.",
    packages=find_packages(),
    install_requires=[
        'nltk',
        'matplotlib',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
