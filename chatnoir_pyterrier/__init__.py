__version__ = "0.1.0"

from dataclasses import dataclass, field
from itertools import islice
from logging import getLogger
from typing import Set, Optional, Iterable, Union

from chatnoir_api import Index
from chatnoir_api.constants import DEFAULT_INDICES
from chatnoir_api.model import Slop
from chatnoir_api.model.result import SearchResult, PhraseSearchResult
from chatnoir_api.v1 import search, search_phrases
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy
from pyterrier.batchretrieve import BatchRetrieveBase
from pyterrier.model import add_ranks
from tqdm import tqdm

logger = getLogger("chatnoir-pyterrier")


@dataclass
class ChatNoirRetrieve(BatchRetrieveBase):
    name = "ChatNoirRetrieve"

    api_key: str
    index: Set[Index] = field(default_factory=lambda: DEFAULT_INDICES)
    phrases: bool = False
    slop: Slop = 0
    num_results: Optional[int] = 10
    page_size: int = 10
    verbose: bool = False

    def __post_init__(self):
        super().__init__(verbose=self.verbose)

    def _transform_query(self, topics: DataFrame) -> DataFrame:
        assert topics["qid"].nunique() <= 1
        assert topics["query"].nunique() <= 1

        query_id: int = topics.iloc[0]["qid"]
        query: str = topics.iloc[0]["query"]
        page_size: int
        if self.num_results is not None:
            page_size = min(self.page_size, self.num_results)
        else:
            page_size = self.page_size

        results: Union[Iterable[SearchResult], Iterable[PhraseSearchResult]]
        if not self.phrases:
            results = search(
                api_key=self.api_key,
                query=query,
                index=self.index,
                explain=False,
                page_size=page_size,
            )
        else:
            results = search_phrases(
                api_key=self.api_key,
                query=query,
                index=self.index,
                slop=self.slop,
                explain=False,
                page_size=page_size,
            )

        if self.num_results is not None:
            results = islice(results, self.num_results)

        return DataFrame([
            {
                "qid": query_id,
                "query": query,
                "docno": result.trec_id,
                "score": result.score,
            }
            for result in results
        ])

    def transform(self, topics: DataFrame) -> DataFrame:

        if not isinstance(topics, DataFrame):
            raise RuntimeError("Can only transform dataframes.")

        if not {'qid', 'query'}.issubset(topics.columns):
            raise RuntimeError("Needs qid and query columns.")

        if len(topics) == 0:
            return self._transform_query(topics)

        topics_by_query: DataFrameGroupBy = topics.groupby(
            by=["qid"],
            as_index=False,
            sort=False,
        )
        if self.verbose:
            # Show progress during reranking queries.
            tqdm.pandas(
                desc="Searching with ChatNoir",
                unit="query",
            )
            topics_by_query = topics_by_query.progress_apply(
                self._transform_query
            )
        else:
            topics_by_query = topics_by_query.apply(self._transform_query)

        retrieved = topics_by_query.reset_index(drop=True)
        retrieved = add_ranks(retrieved)

        return retrieved
