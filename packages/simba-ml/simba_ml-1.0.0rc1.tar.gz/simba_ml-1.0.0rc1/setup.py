from setuptools import setup, find_packages
import versioneer
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

VERSION = versioneer.get_version()
DESCRIPTION = "Simulation-Based Machine Learning"
print(VERSION)

# Setting up
setup(
    name="simba_ml",
    version=VERSION,
    cmdclass=versioneer.get_cmdclass(),
    author="Maximilian Kleissl, Björn Heyder, Julian Zabbarov, Lukas Drews",
    author_email="maximilian.kleissl@student.hpi.de,bjoern.heyder@student.hpi.de,julian.zabbarov@student.hpi.de,lukas.drews@student.hpi.de",
    project_urls={
        "Bug Tracker": "https://gitlab.hpi.de/mpws2022br1/simba_ml/issues",
        "Source Code": "https://gitlab.hpi.de/mpws2022br1/simba_ml/",
    },
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "numpy",
        "scipy",
        "matplotlib",
        "scikit-learn",
        "dacite",
        "tomli",
        "wandb",
    ],
    keywords=[
        "python",
        "machine learning",
        "simulation",
        "ordinary differential equations",
        "ode",
        "simba",
        "simba-ml",
    ],
    classifiers=[],
    entry_points={
        "console_scripts": [
            "simba_ml = simba_ml.cli.__main__:main",
        ],
    },
    license_files=("LICENSE.txt",),
    data_files=[("man/man1", ["man/simba_ml.1"])],
)
