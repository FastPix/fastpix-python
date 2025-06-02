from setuptools import setup, find_packages
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setup(
    name="fastpix_python",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        'async': [
            'aiohttp>=3.8.0',
        ]
    },
    description="FastPix SDK with both sync and async support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="FastPix",
    author_email="dev@fastpix.io",
    url="https://github.com/fastpix-io/fastpix-python-server-sdk",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)
