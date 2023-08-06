from setuptools import setup, find_packages


setup(
    name="scaffoldx",
    version="1.0.0",
    license="MIT",
    author="Dhia' Alhaq Shalabi",
    author_email="dhia.shalabi@gmail.com",
    packages=find_packages("scaffold"),
    package_dir={"": "scaffold"},
    url="https://github.com/dhiashalabi/scaffold",
    keywords="Scaffold",
    install_requires=[
        "django",
    ],
)
