import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auto_video_cut",
    version="0.0.1",
    author="Yasin Balcancı",
    author_email="ybalcanci@gmail.com",
    description="Cut unnecessary parts of a video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ybalcanci/auto_video_cut",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)