from setuptools import setup


setup(
    name="pychatgpt-cli",
    version="0.0.2",
    install_requires=[
        "click",
        "openai>=0.27.0",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "gcli = cli:main",
        ],
    },
)
