from chatnoir_api import Index
from pandas import DataFrame

from chatnoir_pyterrier.retrieve import ChatNoirRetrieve, Feature


def test_retrieve_hash(api_key: str):
    retrieve = ChatNoirRetrieve(
        api_key=api_key,
    )
    retrieve_hash = hash(retrieve)
    assert isinstance(retrieve_hash, int)


def test_retrieve_query(api_key: str, query: str, index: Index):
    retrieve = ChatNoirRetrieve(
        api_key=api_key,
        index=index,
        num_results=1,
    )
    result = retrieve.search(query)
    assert result is not None
    assert isinstance(result, DataFrame)
    assert "qid" in result.columns
    assert "query" in result.columns
    assert "docno" in result.columns
    assert "score" in result.columns


def test_retrieve_feature(
    api_key: str,
    query: str,
    feature: Feature,
):
    retrieve = ChatNoirRetrieve(
        api_key=api_key,
        features=feature,
        num_results=1,
    )
    result = retrieve.search(query)
    assert result is not None
    assert isinstance(result, DataFrame)

    if Feature.UUID in feature:
        assert "uuid" in result.columns
    if Feature.TREC_ID in feature:
        assert "trec_id" in result.columns
    if Feature.WARC_ID in feature:
        assert "warc_id" in result.columns
    if Feature.INDEX in feature:
        assert "index" in result.columns
    if Feature.CRAWL_DATE in feature:
        assert "crawl_date" in result.columns
    if Feature.TARGET_HOSTNAME in feature:
        assert "target_hostname" in result.columns
    if Feature.TARGET_URI in feature:
        assert "target_uri" in result.columns
    if Feature.CACHE_URI in feature:
        assert "cache_uri" in result.columns
    if Feature.PAGE_RANK in feature:
        assert "page_rank" in result.columns
    if Feature.SPAM_RANK in feature:
        assert "spam_rank" in result.columns
    if Feature.TITLE_HIGHLIGHTED in feature:
        assert "title_highlighted" in result.columns
    if Feature.TITLE_TEXT in feature:
        assert "title_text" in result.columns
    if Feature.SNIPPET_HIGHLIGHTED in feature:
        assert "snippet_highlighted" in result.columns
    if Feature.SNIPPET_TEXT in feature:
        assert "snippet_text" in result.columns
    if Feature.EXPLANATION in feature:
        assert "explanation" in result.columns
    if Feature.CONTENTS in feature:
        assert "contents" in result.columns
    if Feature.CONTENTS_PLAIN in feature:
        assert "contents_plain" in result.columns
        assert "text" in result.columns
    if Feature.CONTENT_TYPE in feature:
        assert "content_type" in result.columns
    if Feature.LANGUAGE in feature:
        assert "language" in result.columns
