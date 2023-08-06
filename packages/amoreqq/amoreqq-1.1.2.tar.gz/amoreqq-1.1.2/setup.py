import re
from setuptools import setup

with open("README.md", "r") as f:
    readme_content = f.read()

base_packages = ["httpx", "pydantic"]

with open("amoreqq/version.py", "r", encoding="utf-8") as f:
            version = re.search(
                r"^__version__\s*=\s*'(.*)'.*$", f.read(), flags=re.MULTILINE
            )[1]
        
setup(
    name="amoreqq",
    license="MIT",
    author="Amore",
    author_email="me.thefarkhodov@gmail.com",
    url="https://github.com/AmoreForever/amoreqq",
    download_url="https://github.com/AmoreForever/amoreqq/archive/main.zip",
    keywords=["different dimension me", "anime", "ai"],
    classifiers=[
        "Programming Language :: Python :: 3.10"
    ],
    description_file="README.md",
    license_files=["LICENSE.md"],
    long_description_content_type="text/markdown",
    requires=base_packages,
    version=version,
    long_description=readme_content,
)
