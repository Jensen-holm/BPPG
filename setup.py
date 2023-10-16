from setuptools import setup

APP = ["app.py"]

DATA_FILES = [
    "data/iris.csv",
]

OPTIONS = {
    "iconfile": "assets/backprop_playground.png",
}

setup(
    name="BPPG",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
