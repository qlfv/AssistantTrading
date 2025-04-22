from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="FinTechForesight",
    version="1.0.0",
    author="Quentin Lefèvre",
    author_email="votre.email@example.com",
    description="Assistant IA pour le Trading et les Cryptomonnaies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wiminds/FinTechForesight",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "yfinance>=0.2.0",
        "scikit-learn>=1.3.0",
        "tensorflow>=2.15.0",
        "seaborn>=0.13.0",
        "plotly>=5.18.0",
        "ta>=0.10.0",
        "python-binance>=1.0.19",
        "ccxt>=4.1.13",
    ],
    entry_points={
        "console_scripts": [
            "fintechforesight=main:main",
        ],
    },
) 