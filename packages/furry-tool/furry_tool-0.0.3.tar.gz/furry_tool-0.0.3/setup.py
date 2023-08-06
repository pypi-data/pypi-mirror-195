import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="furry_tool",
    version="0.0.3",
    author="AaronDoge",
    author_email="pangyuyu@email.cn",
    description="个人工具集",
    license="Apache License 2.0",
    keywords=['python', 'furry_tool', 'toolkit'],
    install_requires=['docxtpl'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xsxz01/furry_tool.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
