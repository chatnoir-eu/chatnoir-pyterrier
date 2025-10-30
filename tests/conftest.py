from os import environ

from pytest import fixture
# from pytest import fixture, skip

from chatnoir_api import Index

from chatnoir_pyterrier.retrieve import Feature


@fixture(scope="module")
def api_key() -> str:
    key: str = "CHATNOIR_API_KEY"
    if key not in environ:
        raise RuntimeError(
            f"Must specify ChatNoir api key "
            f"in the {key} environment variable "
            f"to run this test."
        )
    return environ[key]


@fixture(scope="module", params=["python library", "search engine"])
def query(request) -> str:
    return request.param


@fixture(
    scope="module",
    params=[
        "clueweb09",
        "clueweb12",
        "clueweb22/b",
        "msmarco-document",
        "msmarco-passage",
        "msmarco-document-v2",
        "msmarco-passage-v2",
        "msmarco-document-v2.1",
        "msmarco-passage-v2.1",
        "trec-tot/2024",
        "longeval-sci/2024-11",
        "wows-owi/2025",
    ]
)
def index(request) -> Index:
    return request.param


@fixture(scope="module", params=[feature for feature in Feature])
def feature(request) -> Feature:
    return request.param
