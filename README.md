[![PyPi](https://img.shields.io/pypi/v/chatnoir-pyterrier?style=flat-square)](https://pypi.org/project/chatnoir-pyterrier/)
[![CI](https://img.shields.io/github/workflow/status/chatnoir-eu/chatnoir-pyterrier/CI?style=flat-square)](https://github.com/chatnoir-eu/chatnoir-pyterrier/actions?query=workflow%3A"CI")
[![Code coverage](https://img.shields.io/codecov/c/github/chatnoir-eu/chatnoir-pyterrier?style=flat-square)](https://codecov.io/github/chatnoir-eu/chatnoir-pyterrier/)
[![Python](https://img.shields.io/pypi/pyversions/chatnoir-pyterrier?style=flat-square)](https://pypi.org/project/chatnoir-pyterrier/)
[![Google Colab](https://img.shields.io/badge/example-open%20in%20colab-informational?style=flat-square)](https://colab.research.google.com/github/chatnoir-eu/chatnoir-pyterrier/blob/main/examples/search.ipynb)
[![Issues](https://img.shields.io/github/issues/chatnoir-eu/chatnoir-pyterrier?style=flat-square)](https://github.com/chatnoir-eu/chatnoir-pyterrier/issues)
[![Commit activity](https://img.shields.io/github/commit-activity/m/chatnoir-eu/chatnoir-pyterrier?style=flat-square)](https://github.com/chatnoir-eu/chatnoir-pyterrier/commits)
[![Downloads](https://img.shields.io/pypi/dm/chatnoir-pyterrier?style=flat-square)](https://pypi.org/project/chatnoir-pyterrier/)
[![License](https://img.shields.io/github/license/chatnoir-eu/chatnoir-pyterrier?style=flat-square)](LICENSE)

# 🔍 chatnoir-pyterrier

Use the ChatNoir search engine in PyTerrier. Powered by the [`chatnoir-api`](https://pypi.org/project/chatnoir-api/) package.

## Installation

```shell
pip install chatnoir-pyterrier
```

## Usage

```python
from chatnoir_pyterrier import ChatNoirRetrieve

api_key: str = "<API_KEY>"
chatnoir = ChatNoirRetrieve(api_key)

# Use PyTerrier functions like with BatchRetrieve.
chatnoir.search("python library")
```

Also, check out the [sample notebook](examples/search.ipynb) or [open it in Google Colab](https://colab.research.google.com/github/chatnoir-eu/chatnoir-pyterrier/blob/main/examples/search.ipynb).

## Citation

If you use this package, please cite the [paper](https://webis.de/publications.html#bevendorff_2018)
from the [ChatNoir](https://github.com/chatnoir-eu) authors. 
You can use the following BibTeX information for citation:

```bibtex
@InProceedings{bevendorff:2018,
  address =               {Berlin Heidelberg New York},
  author =                {Janek Bevendorff and Benno Stein and Matthias Hagen and Martin Potthast},
  booktitle =             {Advances in Information Retrieval. 40th European Conference on IR Research (ECIR 2018)},
  editor =                {Leif Azzopardi and Allan Hanbury and Gabriella Pasi and Benjamin Piwowarski},
  ids =                   {potthast:2018c,stein:2018c},
  month =                 mar,
  publisher =             {Springer},
  series =                {Lecture Notes in Computer Science},
  site =                  {Grenoble, France},
  title =                 {{Elastic ChatNoir: Search Engine for the ClueWeb and the Common Crawl}},
  year =                  2018
}
```

## Development

To build and develop this package you need to install the `build` package:

```shell
pip install build
```

### Installation

Install package dependencies:

```shell
pip install -e .
```

### Testing

Install test dependencies:

```shell
pip install -e .[test]
```

Verify your changes against the test suite to verify.

```shell
flake8 chatnoir_pyterrier examples tests
pylint -E chatnoir_pyterrier examples tests
CHATNOIR_API_KEY="<API_KEY>" pytest chatnoir_pyterrier examples tests
```

Please also add tests for your newly developed code.

### Build wheels

Wheels for this package can be built by:

```shell
python -m build
```

## License

This repository is released under the [MIT license](LICENSE).
