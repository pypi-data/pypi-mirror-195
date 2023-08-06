
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lancium-compute-api",
    version="1.0.2",
    author="Rumit Patel",
    author_email="rumit.patel@lancium.com",
    description="Client Library for Lancium API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=["pyjwt", "requests", "six", "urllib3"],
    classifiers=[],
    python_requires='>=3.6',
)