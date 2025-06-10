"""
Mountain Blog Generator
低山旅行記事自動生成システム
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mountain-blog-generator",
    version="1.0.0",
    author="Mountain Blog Team",
    author_email="admin@teizan.abg.ooo",
    description="低山旅行記事を自動生成してWordPressに投稿するシステム",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mountain-blog-generator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "anthropic>=0.25.0",
        "Pillow>=10.2.0",
        "python-dateutil>=2.8.2",
        "PyYAML>=6.0.1",
        "colorlog>=6.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "responses>=0.24.1",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "isort>=5.13.0",
        ],
        "scheduler": [
            "schedule>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mountain-blog=src.presentation.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.yaml", "*.yml"],
    },
)