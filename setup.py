import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    entry_points={
        'console_scripts': [
            'autotile_generator = autotile_generator.__main__:main'
        ]
    },
    name="autotile_generator",
    include_package_data=True,
    version="1.0.0",
    author="Hearto Lazor",
    author_email="hearto@kemonogames.com",
    description="Game tile expansion helper",
    keywords ="gamedev autotile tile generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HeartoLazor/autotile_generator",
    install_requires=['jstyleson', 'pillow'],
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ),
)