# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['clustree']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6,<4.0',
 'networkx>=3,<4',
 'pairing-functions==0.2.1',
 'pandas>=1.5,<2.0']

setup_kwargs = {
    'name': 'clustree',
    'version': '0.1.8',
    'description': 'Visualize relationship between clusterings at different resolutions',
    'long_description': "# clustree\n\n## Status\n\n**Functionality: Implemented**\n\n* Directed graph representing clustree. Nodes are parsed images and node information is encoded by a small circle in the corner of the image.\n* Data and images provided directly or through a path to parent directory.\n* If parsed directly, data should be a `pd.DataFrame` object.\n* If parsed directly, images should be a dictionary. See more information in Quickstart.\n* Edge and node color can correspond to one of: #samples that pass through edge/node, cluster resolution `K`, or a fixed color. In the case of node color, a column name in the data and aggregate function can be used too. Use of column name and #samples creates a continuous colormap, whilst the other options result in discrete colors.\n\n\n**Functionality: To Add**\n\n* Legend for continuous colormaps.\n* Reingold-Tilford algorithm to minimise crossing edges.\n* Allow PDF inputs.\n* Much more! Early testing will help prioritise future development.\n\n## Usage\n\n### Installation\n\nInstall the package with pip:\n\n```\npip install clustree\n```\n\n### Quickstart\n\nThe powerhouse function of the library is `clustree`. Use\n\n```\nfrom clustree import clustree\n```\n\nto import the function. Details on the parameters is provided below.\n\n```\ndef clustree(\n    data: Union[str, Path, pd.DataFrame],\n    prefix: str,\n    images: Union[str, Path, dict[int, np.ndarray]],\n    output_path: Optional[Union[str, Path]] = None,\n    draw: bool = True,\n    node_color: Any = None,\n    node_color_aggr: Optional[Union[Callable, str]] = None,\n    node_cmap: Optional[Union[mpl.colors.Colormap, str]] = None,\n    edge_color: Any = None,\n    edge_cmap: Optional[Union[mpl.colors.Colormap, str]] = None,\n    errors: bool = False,\n) -> DiGraph:\n```\n\n* `data`: Path of csv or DataFrame object.\n* `prefix`: String indicating columns containing clustering information.\n* `images`: String indicating directory containing images. See more information on files expected in directory in Notes.\n* `output_path`: Directory to output the final plot to. If None, then output not wrriten to file.\n* `draw`: Whether to draw the clustree. Defaults to True. If False and output_path supplied, will be overridden. Saving to file requires drawing.\n* `node_color`: For continuous colormap, use 'samples' or the name of a metadata column to color nodes by. For discrete colors, use 'prefix' to color by resolution or specify a fixed color (see Specifying colors in Matplotlib tutorial here: https://matplotlib.org/stable/tutorials/colors/colors.html).  If None, default set equal to value of prefix to color by resolution.\n* `node_color_aggr`: If node_color is a column name then a function or string giving the name of a function to aggregate that column for samples in each cluster.\n* `node_cmap`: If node_color is 'samples' or a column name then a colourmap to use (see Colormap Matplotlib tutorial here: https://matplotlib.org/stable/tutorials/colors/colormaps.html).\n* `edge_color`: For continuous colormap, use 'samples'. For discrete colors, use 'prefix' to color by resolution or specify a fixed color (see Specifying colors in Matplotlib tutorial here: https://matplotlib.org/stable/tutorials/colors/colors.html). If None, default set to 'samples'.\n* `edge_cmap`: If edge_color is 'samples' then a colourmap to use (see Colormap Matplotlib tutorial here: https://matplotlib.org/stable/tutorials/colors/colormaps.html).\n* `errors`: Whether to raise an error if an image is missing from directory supplied to images parameter. If False, a fake image will be created with text 'K_k' where K is cluster resolution and k is cluster number. Defaults to False.\n\n## Glossary\n\n* *cluster resolution*: Upper case `K`. For example, at cluster resolution `K=2` data is clustered into 2 distinct clusters.\n* *cluster number*: Lower case `k`. For example, at cluster resolution 2 data is clustered into 2 distinct clusters `k=1` and `k=2`.\n* *kk*: highest value of `K` (cluster resolution) shown in clustree.\n* *cluster membership*: The association between data points and cluster numbers for fixed cluster resolution. For example, `[1, 1, 2, 2, 2]` would mean the first 2 data points belong to cluster number `1` and the following 3 data points belong to cluster number `2`.",
    'author': 'Ben Barlow',
    'author_email': 'ben-j-barlow.1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ben-j-barlow/clustree',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
