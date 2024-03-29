import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="documents-analysis-engine",
    version="0.0.1",
    author="seong-min-a",
    author_email="seong.min.ahn.x@gmail.com",
    description="documents analysis engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seong-min-a/documents-analysis-engine",
    project_urls={
        "Bug Tracker": "https://github.com/seong-min-a/documents-analysis-engine/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "documents_analysis_engine"},
    packages=setuptools.find_packages(where="documents_analysis_engine"),
    python_requires=">=3.8",
)