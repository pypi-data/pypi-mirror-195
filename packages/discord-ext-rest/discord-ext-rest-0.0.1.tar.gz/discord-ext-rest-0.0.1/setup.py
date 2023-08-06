from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()
setup(
    name='discord-ext-rest',
    version='0.0.1',
    author="Pranoy Majumdar",
    author_email="officialpranoy2@gmail.com",
    description="🚀 A discord.py extension for Discord HTTP Interactions support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PranoyMajumdar/discord-ext-rest",
    project_urls={
        "Homepage": "https://github.com/PranoyMajumdar/discord-ext-rest"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.10",
    license="MIT",
    # extra_requires={
    #     "music": [
    #         "pomice"
    #     ]
    # }
)
