from dataclasses import dataclass, field
from functools import reduce
from itertools import islice
from typing import Set, Optional, Iterable, Union, Any, Dict, Hashable

from chatnoir_api import Index, Result, Slop, ExplainedResult
from chatnoir_api.model import SearchMethod
from chatnoir_api.v1 import (
    search, search_phrases
)
from chatnoir_api.defaults import (
    DEFAULT_INDEX, DEFAULT_SLOP, DEFAULT_RETRIES, DEFAULT_BACKOFF_SECONDS, DEFAULT_API_KEY, DEFAULT_SEARCH_METHOD
)
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy
from pyterrier import Transformer
from pyterrier.model import add_ranks
from tqdm import tqdm

from chatnoir_pyterrier.feature import Feature

@dataclass
class ChatNoirRetrieve(Transformer):
    name = "ChatNoirRetrieve"

    index: Union[Index, Set[Index]] = field(
        default_factory=lambda: DEFAULT_INDEX,
    )
    phrases: bool = False
    slop: Slop = DEFAULT_SLOP
    features: Union[Feature, Set[Feature]] = Feature.NONE
    filter_unknown: bool = False
    num_results: Optional[int] = 10
    page_size: int = 100
    retries: int = DEFAULT_RETRIES
    backoff_seconds: float = DEFAULT_BACKOFF_SECONDS
    verbose: bool = False
    api_key: str = DEFAULT_API_KEY
    search_method: SearchMethod = DEFAULT_SEARCH_METHOD

    def _merge_result(
        self,
        row: Dict[Hashable, Any],
        result: Union[
            Result, ExplainedResult,
        ]
    ) -> Dict[Hashable, Any]:
        row = {
            **row,
            "docno": result.trec_id,
            "score": result.score,
        }
        if Feature.UUID in self.features:
            row["uuid"] = result.uuid
        if Feature.TREC_ID in self.features:
            row["trec_id"] = result.trec_id
        if Feature.WARC_ID in self.features:
            row["warc_id"] = result.warc_id
        if Feature.INDEX in self.features:
            row["index"] = result.index
        if Feature.CRAWL_DATE in self.features:
            row["crawl_date"] = result.crawl_date
        if Feature.TARGET_HOSTNAME in self.features:
            row["target_hostname"] = result.target_hostname
        if Feature.TARGET_URI in self.features:
            row["target_uri"] = result.target_uri
        if Feature.CACHE_URI in self.features:
            row["cache_uri"] = result.cache_uri
        if Feature.PAGE_RANK in self.features:
            row["page_rank"] = result.page_rank
        if Feature.SPAM_RANK in self.features:
            row["spam_rank"] = result.spam_rank
        if Feature.TITLE_HIGHLIGHTED in self.features:
            row["title_highlighted"] = result.title.html
        if Feature.TITLE_TEXT in self.features:
            row["title_text"] = result.title.text
        if Feature.SNIPPET_HIGHLIGHTED in self.features:
            row["snippet_highlighted"] = result.snippet.html
        if Feature.SNIPPET_TEXT in self.features:
            row["snippet_text"] = result.snippet.text
        if Feature.EXPLANATION in self.features:
            if not isinstance(result, ExplainedResult):
                raise RuntimeError(f"Unexpected response type: {type(result)}, expected: {type(ExplainedResult)}")
            row["explanation"] = result.explanation
        if Feature.CONTENTS in self.features:
            try:
                row["contents"] = result.cache_contents(plain=False)
            except Exception:
                row["contents"] = None
        if Feature.CONTENTS_PLAIN in self.features:
            try:
                row["text"] = row["contents_plain"] = result.cache_contents(plain=True)
            except Exception:
                row["text"] = row["contents_plain"] = None
        if Feature.CONTENT_TYPE in self.features:
            row["content_type"] = result.content_type
        if Feature.LANGUAGE in self.features:
            row["language"] = result.language
        return row

    def _transform_query(self, topic: DataFrame) -> DataFrame:
        if len(topic.index) != 1:
            raise RuntimeError("Can only transform one query at a time.")

        row: Dict[Hashable, Any] = topic.to_dict(orient="records")[0]
        query: str = row["query"]

        page_size: int
        if self.num_results is not None:
            page_size = min(self.page_size, self.num_results)
        else:
            page_size = self.page_size

        features: Feature
        if isinstance(self.features, Set):
            features = reduce(
                lambda feature_a, feature_b: feature_a | feature_b,
                self.features
            )
        else:
            features = self.features

        explain: bool = Feature.EXPLANATION in features

        results: Iterable[Union[
            Result, ExplainedResult,
        ]]
        if not self.phrases:
            if explain:
                results = search(
                    query=query,
                    index=self.index,
                    minimal=False,
                    explain=True,
                    page_size=page_size,
                    retries=self.retries,
                    backoff_seconds=self.backoff_seconds,
                    api_key=self.api_key,
                    search_method=self.search_method
                ).results
            else:
                results = search(
                    query=query,
                    index=self.index,
                    minimal=False,
                    explain=False,
                    page_size=page_size,
                    retries=self.retries,
                    backoff_seconds=self.backoff_seconds,
                    api_key=self.api_key,
                    search_method=self.search_method
                ).results
        else:
            if explain:
                results = search_phrases(
                    query=query,
                    index=self.index,
                    minimal=False,
                    slop=self.slop,
                    explain=True,
                    page_size=page_size,
                    retries=self.retries,
                    backoff_seconds=self.backoff_seconds,
                    api_key=self.api_key,
                    search_method=self.search_method
                ).results
            else:
                results = search_phrases(
                    query=query,
                    index=self.index,
                    minimal=False,
                    slop=self.slop,
                    explain=False,
                    page_size=page_size,
                    retries=self.retries,
                    backoff_seconds=self.backoff_seconds,
                    api_key=self.api_key,
                    search_method=self.search_method
                ).results

        if self.filter_unknown:
            # Filter unknown results, i.e., when the TREC ID is missing.
            results = (
                result
                for result in results
                if result.trec_id is not None
            )
            pass

        if self.num_results is not None:
            results = islice(results, self.num_results)

        return DataFrame([
            self._merge_result(row, result)
            for result in results
        ])

    def transform(self, inp: DataFrame) -> DataFrame:

        if not isinstance(inp, DataFrame):
            raise RuntimeError("Can only transform dataframes.")

        if not {'qid', 'query'}.issubset(inp.columns):
            raise RuntimeError("Needs qid and query columns.")

        if len(inp) == 0:
            return self._transform_query(inp)

        topics_by_query: DataFrameGroupBy = inp.groupby(
            by=["qid"],
            as_index=False,
            sort=False,
        )

        retrieved: DataFrame
        if self.verbose:
            # Show progress during reranking queries.
            tqdm.pandas(
                desc="Searching with ChatNoir",
                unit="query",
            )
            retrieved = topics_by_query.progress_apply(
                self._transform_query
            )
        else:
            retrieved = topics_by_query.apply(self._transform_query)

        if len(retrieved) == 0:
            return retrieved
        retrieved = retrieved.reset_index(drop=True)\
            .sort_values(by=["score"], ascending=False)
        retrieved = add_ranks(retrieved)

        return retrieved

    def __hash__(self):
        return hash((
            self.api_key,
            (
                tuple(sorted(self.index))
                if isinstance(self.index, Set)
                else self.index
            ),
            self.phrases,
            self.slop,
            (
                list(sorted(self.features))
                if isinstance(self.features, Set)
                else self.features
            ),
            self.filter_unknown,
            self.num_results,
            self.page_size,
            self.retries,
            self.backoff_seconds,
            self.verbose,
        ))
