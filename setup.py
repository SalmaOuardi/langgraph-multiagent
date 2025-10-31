from setuptools import setup, find_packages

setup(
    name="langgraph-multiagent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
