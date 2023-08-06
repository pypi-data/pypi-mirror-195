## STAC Info package
#### This package provides a way to search for STAC items in a STAC catalog and view the metadata of the items in a CSV file.

### Installation
#### Install the package using pip:
```bash
pip install stac-info
```

### Usage
#### To search for STAC items in a STAC catalog, use the following command:
```python
from stac_info.search import EarthSearch

bbox = [-122.5, 37.5, -122.0, 37.8]
date = ["2020-01-01", "2020-01-31"].join("/")
limit = 10

data = EarthSearch("https://earth-search.aws.element84.com/v0/search")
data.filter(bbox, date, limit)
```

#### The search results will automatically be saved in a CSV file named `earth_search.csv` in the current working directory.

More information about STAC can be found [here](https://stacspec.org/).
More features will be added and announced in the future.

### DISCLAIMER
#### This package is not affiliated with the STAC project in any way. This package is not endorsed by the STAC project. This package is not supported by the STAC project.
#### This is a beta version of the package. The package is still under development and may not be stable. Use at your own risk.