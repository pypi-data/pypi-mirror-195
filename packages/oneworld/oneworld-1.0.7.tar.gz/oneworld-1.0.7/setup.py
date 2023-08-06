import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oneworld", 
    version="1.0.7",
    author="Antoni Aguilar Mogas",
    author_email="aguilar.mogas@gmail.com",
    description="Python mapping made easy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://taguilar@bitbucket.org/taguilar/oneworld",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: GIS"
    ],
    python_requires='>=3.7',
    install_requires=[ 
          "pandas>=1.5.2",
          "matplotlib>=3.6.2",
          "seaborn>=0.12.2",
          "jinja2>=3.1.2",
          "cartopy>=0.21.1",
      ],
    include_package_data=True,
)
