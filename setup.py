from setuptools import setup
import py2exe
setup(
    console=["glcube.py"],
    app=["glcube.py"],
    setup_requires=["py2app"],
)
