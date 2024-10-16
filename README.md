[![PyPi](https://img.shields.io/pypi/v/chatnoir-pyterrier?style=flat-square)](https://pypi.org/project/chatnoir-pyterrier/)
[![CI](https://img.shields.io/github/actions/workflow/status/chatnoir-eu/chatnoir-pyterrier/ci.yml?branch=main&style=flat-square)](https://github.com/chatnoir-eu/chatnoir-pyterrier/actions/workflows/ci.yml)
[![Code coverage](https://img.shields.io/codecov/c/github/chatnoir-eu/chatnoir-pyterrier?style=flat-square)](https://codecov.io/github/chatnoir-eu/chatnoir-pyterrier/)
[![Python](https://img.shields.io/pypi/pyversions/chatnoir-pyterrier?style=flat-square)](https://pypi.org/project/chatnoir-pyterrier/)
[![Google Colab](https://img.shields.io/badge/example-open%20in%20colab-informational?style=flat-square)](https://colab.research.google.com/github/chatnoir-eu/chatnoir-pyterrier/blob/main/examples/search.ipynb)
[![Issues](https://img.shields.io/github/issues/chatnoir-eu/chatnoir-pyterrier?style=flat-square)](https://github.com/chatnoir-eu/chatnoir-pyterrier/issues)
[![Commit activity](https://img.shields.io/github/commit-activity/m/chatnoir-eu/chatnoir-pyterrier?style=flat-square)](https://github.com/chatnoir-eu/chatnoir-pyterrier/commits)
[![Downloads](https://img.shields.io/pypi/dm/chatnoir-pyterrier?style=flat-square)](https://pypi.org/project/chatnoir-pyterrier/)
[![License](https://img.shields.io/github/license/chatnoir-eu/chatnoir-pyterrier?style=flat-square)](LICENSE)

# 🔍 chatnoir-pyterrier

Use the ChatNoir REST-API in PyTerrier for retrieval/re-ranking against large corpora such as ClueWeb09, ClueWeb12, ClueWeb22, or MS MARCO.

Powered by the [`chatnoir-api`](https://pypi.org/project/chatnoir-api/) package.

## Installation
Install the package from PyPI:

```shell
pip install chatnoir-pyterrier
```

## Usage
You can use the `ChatNoirRetrieve` PyTerrier module in any PyTerrier pipeline, like you would do with `BatchRetrieve`.

```python
from chatnoir_pyterrier import ChatNoirRetrieve, Feature
from chatnoir_api import Index

chatnoir = ChatNoirRetrieve(staging=True, num_results=5, index=Index.MSMarcoV21, features=Feature.SNIPPET_TEXT)
chatnoir.search("python library")
```

Please check out our [sample notebook](examples/search.ipynb) or [open it in Google Colab](https://colab.research.google.com/github/chatnoir-eu/chatnoir-pyterrier/blob/main/examples/search.ipynb).

### Touché 2023
Are you participating in Touché 2023 [task 1](https://touche.webis.de/clef23/touche23-web/argument-retrieval-for-controversial-questions.html) or [task 2](https://touche.webis.de/clef23/touche23-web/evidence-retrieval-for-causal-questions.html)?
We've prepared a [sample notebook](examples/search_touche_2023.ipynb) to show you how to retrieve from the ClueWeb22.
Get started by [opening it in Google Colab](https://colab.research.google.com/github/chatnoir-eu/chatnoir-pyterrier/blob/main/examples/search_touche_2023.ipynb).

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
  month =                 mar,
  publisher =             {Springer},
  series =                {Lecture Notes in Computer Science},
  site =                  {Grenoble, France},
  title =                 {{Elastic ChatNoir: Search Engine for the ClueWeb and the Common Crawl}},
  year =                  2018
}
```

## Development

To build this package and contribute to its development you need to install the `build`, and `setuptools` and `wheel` packages:

```shell
pip install build setuptools wheel
```

(On most systems, these packages are already pre-installed.)

### Installation

Install package and test dependencies:

```shell
pip install -e .[test]
```

### Testing

Configure the API keys for testing:

```shell
export CHATNOIR_API_KEY="<API_KEY>"
export CHATNOIR_API_KEY_STAGING="<API_KEY>"
```

Verify your changes against the test suite to verify.

```shell
flake8 chatnoir_pyterrier tests examples
pylint -E chatnoir_pyterrier tests examples
pytest chatnoir_pyterrier tests examples
```

Please also add tests for your newly developed code.

### Build wheels

Wheels for this package can be built with:

```shell
python -m build
```

## Support

If you hit any problems using this package, please file an [issue](https://github.com/chatnoir-eu/chatnoir-pyterrier/issues/new).
We're happy to help!

## License

This repository is released under the [MIT license](LICENSE).
