# This file is placed in the Public Domain.


"OPB is a object programming bot."


import os


from setuptools import setup


def read():
    return open("README.rst", "r").read()


def uploadlist(dir):
    upl = []
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl


setup(
    name="cide",
    version="1",
    author="B.H.J. Thate",
    author_email="operbot100@gmail.com",
    url="http://github.com/operbot/operbot",
    description="object programming bot",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=["cide", "cide.modules"],
    scripts=[
             "bin/cide",
             "bin/cidec",
             "bin/cided"
            ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: System Administrators",
        "Topic :: Communications :: Chat :: Internet Relay Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)
