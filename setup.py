from setuptools import setup, find_packages

setup(
    name="flask_service_tools",
    version="0.1.0",
    package_dir={"": "flask_service_tools"},
    packages=find_packages(where="flask_service_tools"),
    install_requires=[
        "Flask",
        "SQLAlchemy",
        "PyMySQL",
    ],
    description="Common utilities for Flask API services",
    url="https://github.com/ATM-Consulting/flask_service_tools.git",
    author="Sami Filali",
    author_email="sami.filali@atm-consulting.fr",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
