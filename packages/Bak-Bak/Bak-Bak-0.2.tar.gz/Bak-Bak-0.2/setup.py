from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Bak-Bak",
    version="0.2",
    description="A Python library for speech synthesis using SAPI.SpVoice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["bakbak"],
    install_requires=["pypiwin32"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
