from setuptools import setup, find_packages

setup(
    name="fastpix-python",
    version="0.1.0",
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
