from setuptools import setup, find_packages

setup(
    name="flask_service_tools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "SQLAlchemy",
        "PyMySQL",
    ],
    description="Common utilities for Flask API services",
    url="https://gitlab.atm-consulting.fr/atm-consulting/ai-services-hub/flask_service_tools",
    author="Sami Filali",
    author_email="sami.filali@atm-consulting.fr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
