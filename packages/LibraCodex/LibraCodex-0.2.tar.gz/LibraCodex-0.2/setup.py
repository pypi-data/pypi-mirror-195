from setuptools import setup, find_packages



setup(
    name="LibraCodex",
    version="0.2",
    author="Norlize",
    author_email="norlizyber0@gmail.com",
    description="a simple library fot local files management by collect multiple paths in once times.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=["LibraCodex"],
    keywords=['local','Libra','Libracodex','LibraCodex','Codex','os','utility','codex'],
    package_data={
        "LibraCodex":[
            "license.txt",
            "Readme.md",
            "Example.py"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls = {
        "Source code":'https://github.com/Norlize/Libracodex'
    },
)
