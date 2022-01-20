[![PyPi](https://img.shields.io/pypi/v/chatnoir-pyserini?style=flat-square)](https://pypi.org/project/chatnoir-pyserini/)
[![CI](https://img.shields.io/github/workflow/status/heinrichreimer/chatnoir-pyserini/CI?style=flat-square)](https://github.com/heinrichreimer/chatnoir-pyserini/actions?query=workflow%3A"CI")
[![Code coverage](https://img.shields.io/codecov/c/github/heinrichreimer/chatnoir-pyserini?style=flat-square)](https://codecov.io/github/heinrichreimer/chatnoir-pyserini/)
[![Python](https://img.shields.io/pypi/pyversions/chatnoir-pyserini?style=flat-square)](https://pypi.org/project/chatnoir-pyserini/)
[![Issues](https://img.shields.io/github/issues/heinrichreimer/chatnoir-pyserini?style=flat-square)](https://github.com/heinrichreimer/chatnoir-pyserini/issues)
[![Commit activity](https://img.shields.io/github/commit-activity/m/heinrichreimer/chatnoir-pyserini?style=flat-square)](https://github.com/heinrichreimer/chatnoir-pyserini/commits)
[![Downloads](https://img.shields.io/pypi/dm/chatnoir-pyserini?style=flat-square)](https://pypi.org/project/chatnoir-pyserini/)
[![License](https://img.shields.io/github/license/heinrichreimer/chatnoir-pyserini?style=flat-square)](LICENSE)

# 🔍 chatnoir-pyserini

Use the ChatNoir search engine in PyTerrier. 

## Installation

```shell
pip install chatnoir-pyserini
```

## Usage

```python
from chatnoir.pyserini import TODO

api_key: str = "<API_KEY>"

TODO
```

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
flake8 chatnoir examples
pylint -E chatnoir examples
pytest chatnoir examples
```

Please also add tests for the axioms or integrations you've added.

### Build wheel

A wheel for this package can be built by:

```shell
python -m build
```

## License

This repository is released under the [MIT license](LICENSE).
