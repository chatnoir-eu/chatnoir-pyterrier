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

chatnoir = ChatNoirRetrieve(index="msmarco-document-v2.1", features=Feature.SNIPPET_TEXT)
chatnoir.search("python library")
```

### Features

ChatNoir provides an extensive set of extra features, such as the full text or page rank / spam rank (for some indices).
These can easily be included in the response data frame for usage in subsequent PyTerrier re-ranking stages like so:

```python
from chatnoir_pyterrier import ChatNoirRetrieve, Feature

chatnoir_msmarco_snippet = ChatNoirRetrieve(index="msmarco-document-v2.1", features=Feature.SNIPPET_TEXT)
chatnoir_msmarco_snippet.search("python library")

chatnoir_cw09_page_spam_rank = ChatNoirRetrieve(index="clueweb09", features=Feature.PAGE_RANK | Feature.SPAM_RANK)
chatnoir_cw09_page_spam_rank.search("python library")
```

### Advanced usage

Please check out our [sample notebook](examples/search.ipynb) or [open it in Google Colab](https://colab.research.google.com/github/chatnoir-eu/chatnoir-pyterrier/blob/main/examples/search.ipynb).

We also provide a hands-on guide for the Touché 2023 shared tasks [here](examples/search_touche_2023.ipynb).

<!-- ## Citation

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
``` -->

### Experiments

With chatnoir-pyterrier, it is easy to run benchmarks on a number of shared tasks that run on larger document collections.
We demonstrate this by running ChatNoir retrieval on all suported TREC, CLEF, and NTCIR shared tasks available in ir_datasets.

First install the experiment dependencies:

```shell
pip install -e .[experiment]
```

To run the experiments, first create the runs by running:

```shell
ray job submit --runtime-env examples/ray-runtime-env.yml --no-wait -- python examples/experiment.py 
```

This will create runs for each shared task in parallel and save it to a cache.

After creating the runs, the [`experiment.ipynb`](examples/experiment.ipynb) notebook can be used to analyze the results.

## Indexing

Head over to the [ChatNoir `ir_datasets` indexer](https://github.com/chatnoir-eu/chatnoir-ir-datasets-indexer) to learn more on how new `ir_datasets`-compatible datasets are indexed into ChatNoir.

## Development

To build this package and contribute to its development you need to install the `build`, and `setuptools` and `wheel` packages:

```shell
pip install build setuptools wheel
```

(On most systems, these packages are already pre-installed.)

### Development installation

Install package and test dependencies:

```shell
pip install -e .[test]
```

### Testing

Configure the API keys for testing:

```shell
export CHATNOIR_API_KEY="<API_KEY>"
```

Verify your changes against the test suite to verify.

```shell
ruff check .                   # Code format and LINT
mypy .                         # Static typing
bandit -c pyproject.toml -r .  # Security
pytest .                       # Unit tests
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
