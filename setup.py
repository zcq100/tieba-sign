import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tieba-sign",
    version="0.8.0",
    author="zcq100",
    author_email="zcq100@gmail.com",
    description="贴吧自动签到",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zcq100/tieba-sign",
    packages=setuptools.find_packages(),
    exclude_package_data={
        '': ['tests']
    },
    install_requires=[
        "requests"],
    entry_points={
        'console_scripts': [
            'tieba-sign=tieba:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Internet",
    ],
    python_requires='>=3.6',
)
