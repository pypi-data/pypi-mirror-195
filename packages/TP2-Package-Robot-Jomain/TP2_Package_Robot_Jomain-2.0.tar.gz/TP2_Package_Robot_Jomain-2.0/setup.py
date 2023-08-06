from setuptools import setup

setup(
    name="TP2_Package_Robot_Jomain",
    author="Jomain Benoît",
    version="2.0",
    description="Génération d'une grille avec des méthodes qui permettent de déplacer un robot sur cette grille ou des obstacles peuvent être généré",
    packages=["Package_Robot"],
    install_requires=[
        "numpy",
        "pytest",
    ],
)

