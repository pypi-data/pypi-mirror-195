from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lfmaptools",
    version="0.0.90",
    description="Mapping tools for LaharFlow data",
    author="Mark Woodhouse",
    author_email="mark.woodhouse@bristol.ac.uk",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "click",
        "ipython>7",
        "numpy>=1.19",
        "gdal",
        "contextily>=1.1",
        "matplotlib>=3.6",
        "shapely",
        "pandas",
        "geopandas",
        "netCDF4",
        "xarray",
        "rasterio",
        "rioxarray",
        "pyproj>=2.6",
        "scikit-image",
        "scipy",
        "jenkspy",
        "utm",
        "decorator<5,>=4.3",
        "networkx",
        "osmnx",
        "folium",
    ],
    entry_points={
        "console_scripts": [
            "lf_to_gtif = lfmaptools.scripts.lf_to_gtif:lf_to_gtif",
            "lf_to_kml = lfmaptools.scripts.lf_to_kml:lf_to_kml",
            "lf_inundation = lfmaptools.scripts.lf_inundation:lf_inundation",
            "lf_elev_change = lfmaptools.scripts.lf_elev_change:lf_elev_change",
        ]
    },
    #   extras_require={
    #       'interactive': ['ipython>7'],
    #   },
    zip_safe=False,
)
