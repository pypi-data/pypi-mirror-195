from setuptools import setup

setup(
    name="falcon-easy-crud",
    version="0.0.1",
    description="Make it easier to write web api",
    url="https://github.com/iiicebearrr/eazy-crud",
    author="iiicebearrr",
    author_email="969549808@qq.com",
    license="",
    packages=["falcon_easy_crud"],
    install_requires=[
        "click==8.1.3",
        "falcon==3.1.1",
        "openpyxl==3.1.1",
        "peewee==3.16.0",
        "psycopg2==2.9.5",
        "pyaml==21.10.1",
        "pydantic==1.10.5",
        "XlsxWriter==3.0.8",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
