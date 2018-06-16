import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    entry_points={
        'console_scripts': [
            'my_project = my_project.__main__:main'
        ]
    },
    name="autotile_generator",
    data_files=[('autotile_generator', ['autotile_generator/default_input_map.json'])],
    include_package_data=True,
    version="1.0.0",
    author="Hearto Lazor",
    author_email="hearto@kemonogames.com",
    description="Game tile expansion helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HeartoLazor/autotile_generator",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ),
)