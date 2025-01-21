from setuptools import setup, find_packages

setup(
    name="garmin_planner",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'ply',
        'garth'
    ],
)