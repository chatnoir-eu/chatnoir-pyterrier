from dataclasses import dataclass
from os import environ
from pathlib import Path
from shutil import rmtree
from typing import List, Optional
from dotenv import find_dotenv, load_dotenv
from ray import get, init, remote
from chatnoir_pyterrier import Index
from chatnoir_pyterrier import ChatNoirRetrieve, Feature
from ir_measures import nDCG
from pandas import DataFrame
from pyterrier import Experiment
from pyterrier.apply import generic
from pyterrier.datasets import get_dataset
from pyterrier_caching import RetrieverCache, Lazy, ScorerCache
from pyterrier_t5 import MonoT5ReRanker, DuoT5ReRanker
from torch import device
from torch.cuda import is_available as cuda_is_available

# Load .env file.
if find_dotenv():
    load_dotenv()

# Initialize Ray (and connect to cluster).
init()

EXPERIMENT_DIR = Path(
    "/mnt/ceph/storage/data-in-progress/data-research/web-search/chatnoir/chatnoir-pyterrier"
)


@dataclass(frozen=True)
class Config:
    dataset: str
    index: Index
    topics_variant: str
    campaign: str
    track: str
    year: int
    task: Optional[str] = None


configs: List[Config] = [
    Config(
        dataset="clueweb09/en/trec-web-2009",
        index="clueweb09",
        topics_variant="query",
        campaign="TREC",
        track="Web",
        year=2009,
    ),
    Config(
        dataset="clueweb09/en/trec-web-2009",
        index="clueweb09",
        topics_variant="description",
        campaign="TREC",
        track="Web",
        year=2009,
    ),
    Config(
        dataset="clueweb09/en/trec-web-2010",
        index="clueweb09",
        topics_variant="query",
        campaign="TREC",
        track="Web",
        year=2010,
    ),
    Config(
        dataset="clueweb09/en/trec-web-2010",
        index="clueweb09",
        topics_variant="description",
        campaign="TREC",
        track="Web",
        year=2010,
    ),
    Config(
        dataset="clueweb09/en/trec-web-2011",
        index="clueweb09",
        topics_variant="query",
        campaign="TREC",
        track="Web",
        year=2011,
    ),
    Config(
        dataset="clueweb09/en/trec-web-2011",
        index="clueweb09",
        topics_variant="description",
        campaign="TREC",
        track="Web",
        year=2011,
    ),
    Config(
        dataset="clueweb09/en/trec-web-2012",
        index="clueweb09",
        topics_variant="description",
        campaign="TREC",
        track="Web",
        year=2012,
    ),
    Config(
        dataset="clueweb09/en/trec-web-2012",
        index="clueweb09",
        topics_variant="description",
        campaign="TREC",
        track="Web",
        year=2012,
    ),
    Config(
        dataset="clueweb09/en/trec-web-2012",
        index="clueweb09",
        topics_variant="query",
        campaign="TREC",
        track="Web",
        year=2012,
    ),
    Config(
        dataset="clueweb09/en/trec-web-2012",
        index="clueweb09",
        topics_variant="description",
        campaign="TREC",
        track="Web",
        year=2012,
    ),
    Config(
        dataset="clueweb12/b13/clef-ehealth",
        index="clueweb12",
        topics_variant="text",
        campaign="CLEF",
        track="eHealth",
        year=2016,
    ),
    # No description available.
    Config(
        dataset="clueweb12/b13/ntcir-www-1",
        index="clueweb12",
        topics_variant="text",
        campaign="NTCIR",
        track="WWW",
        year=2017,
    ),
    # No description available.
    Config(
        dataset="clueweb12/b13/ntcir-www-2",
        index="clueweb12",
        topics_variant="title",
        campaign="NTCIR",
        track="WWW",
        year=2018,
    ),
    Config(
        dataset="clueweb12/b13/ntcir-www-2",
        index="clueweb12",
        topics_variant="description",
        campaign="NTCIR",
        track="WWW",
        year=2018,
    ),
    Config(
        dataset="clueweb12/b13/trec-misinfo-2019",
        index="clueweb12",
        topics_variant="title",
        campaign="TREC",
        track="Health Misinfo",
        year=2019,
    ),
    Config(
        dataset="clueweb12/b13/trec-misinfo-2019",
        index="clueweb12",
        topics_variant="description",
        campaign="TREC",
        track="Health Misinfo",
        year=2019,
    ),
    Config(
        dataset="clueweb12/touche-2020-task-2",
        index="clueweb12",
        topics_variant="title",
        campaign="CLEF",
        track="Touché",
        year=2020,
        task="2",
    ),
    Config(
        dataset="clueweb12/touche-2020-task-2",
        index="clueweb12",
        topics_variant="description",
        campaign="CLEF",
        track="Touché",
        year=2020,
        task="2",
    ),
    Config(
        dataset="clueweb12/touche-2021-task-2",
        index="clueweb12",
        topics_variant="title",
        campaign="CLEF",
        track="Touché",
        year=2021,
        task="2",
    ),
    Config(
        dataset="clueweb12/touche-2021-task-2",
        index="clueweb12",
        topics_variant="description",
        campaign="CLEF",
        track="Touché",
        year=2021,
        task="2",
    ),
    Config(
        dataset="clueweb12/touche-2022-task-2",
        index="clueweb12",
        topics_variant="title",
        campaign="CLEF",
        track="Touché",
        year=2022,
        task="2",
    ),
    Config(
        dataset="clueweb12/touche-2022-task-2",
        index="clueweb12",
        topics_variant="description",
        campaign="CLEF",
        track="Touché",
        year=2022,
        task="2",
    ),
    Config(
        dataset="clueweb12/trec-web-2013",
        index="clueweb12",
        topics_variant="query",
        campaign="TREC",
        track="Web",
        year=2013,
    ),
    Config(
        dataset="clueweb12/trec-web-2013",
        index="clueweb12",
        topics_variant="description",
        campaign="TREC",
        track="Web",
        year=2013,
    ),
    Config(
        dataset="clueweb12/trec-web-2014",
        index="clueweb12",
        topics_variant="query",
        campaign="TREC",
        track="Web",
        year=2014,
    ),
    Config(
        dataset="clueweb12/trec-web-2014",
        index="clueweb12",
        topics_variant="description",
        campaign="TREC",
        track="Web",
        year=2014,
    ),
    # Config(
    #     dataset="gov/trec-web-2002",
    #     index="gov",
    #     topics_variant="title",
    #     campaign="TREC",
    #     track="Web",
    #     year=2002,
    # ),
    # Config(
    #     dataset="gov/trec-web-2002",
    #     index="gov",
    #     topics_variant="description",
    #     campaign="TREC",
    #     track="Web",
    #     year=2002,
    # ),
    # Config(
    #     dataset="gov/trec-web-2003",
    #     index="gov",
    #     topics_variant="title",
    #     campaign="TREC",
    #     track="Web",
    #     year=2003,
    # ),
    # Config(
    #     dataset="gov/trec-web-2003",
    #     index="gov",
    #     topics_variant="description",
    #     campaign="TREC",
    #     track="Web",
    #     year=2003,
    # ),
    # Config(
    #     dataset="gov/trec-web-2004",
    #     index="gov",
    #     topics_variant="text",
    #     campaign="TREC",
    #     track="Web",
    #     year=2004,
    # ),
    # # No description available.
    # Config(
    #     dataset="gov2/trec-tb-2004",
    #     index="gov2",
    #     topics_variant="title",
    #     campaign="TREC",
    #     track="Terabyte",
    #     year=2004,
    # ),
    # Config(
    #     dataset="gov2/trec-tb-2004",
    #     index="gov2",
    #     topics_variant="description",
    #     campaign="TREC",
    #     track="Terabyte",
    #     year=2004,
    # ),
    # Config(
    #     dataset="gov2/trec-tb-2005",
    #     index="gov2",
    #     topics_variant="title",
    #     campaign="TREC",
    #     track="Terabyte",
    #     year=2005,
    # ),
    # Config(
    #     dataset="gov2/trec-tb-2005",
    #     index="gov2",
    #     topics_variant="description",
    #     campaign="TREC",
    #     track="Terabyte",
    #     year=2005,
    # ),
    # Config(
    #     dataset="gov2/trec-tb-2006",
    #     index="gov2",
    #     topics_variant="title",
    #     campaign="TREC",
    #     track="Terabyte",
    #     year=2006,
    # ),
    # Config(
    #     dataset="gov2/trec-tb-2006",
    #     index="gov2",
    #     topics_variant="description",
    #     campaign="TREC",
    #     track="Terabyte",
    #     year=2006,
    # ),
    Config(
        dataset="msmarco-passage/trec-dl-2019",
        index="msmarco-passage",
        topics_variant="text",
        campaign="TREC",
        track="Deep Learning",
        year=2019,
    ),
    # No description available.
    Config(
        dataset="msmarco-passage/trec-dl-2020",
        index="msmarco-passage",
        topics_variant="text",
        campaign="TREC",
        track="Deep Learning",
        year=2020,
    ),
    # No description available.
    Config(
        dataset="msmarco-passage-v2/trec-dl-2021",
        index="msmarco-passage-v2",
        topics_variant="text",
        campaign="TREC",
        track="Deep Learning",
        year=2021,
    ),
    # # No description available.
    Config(
        dataset="msmarco-passage-v2/trec-dl-2022",
        index="msmarco-passage-v2",
        topics_variant="text",
        campaign="TREC",
        track="Deep Learning",
        year=2022,
    ),
    # # No description available.
]

CACHE_DIR = EXPERIMENT_DIR / "cache"


def _add_missing_cols(df: DataFrame) -> DataFrame:
    for col in (
        "rank", "query", "text",
    ):
        if col not in df.columns:
            df = df.assign(**{col: None})
    return df


@remote(num_cpus=1, memory=10*1000*1000*1000, num_gpus=1, accelerator_type="GeForce-GTX-1080", max_retries=10, retry_exceptions=True)
# @remote(num_cpus=4, memory=10*1000*1000*1000, max_retries=10, retry_exceptions=True)
def run_experiment(config: Config) -> DataFrame:
    print(f"Config: {config}")
    print(f"Device: {device('cuda' if cuda_is_available() else 'cpu')}")

    retrieve_cache_dir = CACHE_DIR / "retrieve" / config.dataset
    retrieve_cache_dir.mkdir(parents=True, exist_ok=True)
    if not (retrieve_cache_dir / "pt_meta.json").exists():
        rmtree(retrieve_cache_dir)

    rerank_mono_t5_cache_dir = CACHE_DIR / "rerank" / "mono-t5" / config.dataset / config.topics_variant
    rerank_mono_t5_cache_dir.mkdir(parents=True, exist_ok=True)
    if not (rerank_mono_t5_cache_dir / "pt_meta.json").exists():
        rmtree(rerank_mono_t5_cache_dir)

    retrieve_duo_t5_cache_dir = CACHE_DIR / "retrieve" / "duo-t5" / config.dataset
    retrieve_duo_t5_cache_dir.mkdir(parents=True, exist_ok=True)
    if not (retrieve_duo_t5_cache_dir / "pt_meta.json").exists():
        rmtree(retrieve_duo_t5_cache_dir)

    experiment_cache_dir = CACHE_DIR / "experiment5" / config.dataset / config.topics_variant
    experiment_cache_dir.mkdir(parents=True, exist_ok=True)

    # Create ChatNoir retriever.
    retriever = ChatNoirRetrieve(
        api_key=environ["CHATNOIR_API_KEY"],
        index=config.index,
        features=Feature.CONTENTS_PLAIN,
        num_results=100,
        verbose=True,
        retries=20,
    )

    # Cache retriever.
    retriever = RetrieverCache(
        str(retrieve_cache_dir),
        retriever,
        verbose=True,
    ) >> generic(_add_missing_cols)

    # Re-rankers.
    mono_t5 = Lazy(
        lambda: MonoT5ReRanker(
            model="castorini/monot5-base-msmarco",
            verbose=True,
            batch_size=128,
        )
    )
    mono_t5 = ScorerCache(
        str(rerank_mono_t5_cache_dir),
        mono_t5,
        verbose=True,
    )
    duo_t5 = Lazy(
        lambda: DuoT5ReRanker(
            model="castorini/duot5-base-msmarco",
            verbose=True,
            batch_size=128,
        )
    )

    # Data
    dataset = get_dataset(f"irds:{config.dataset}")
    topics = dataset.get_topics(variant=config.topics_variant)
    topics = topics[topics["query"] != ""]  # Catch empty queries that cause troubles with ChatNoir.
    qrels = dataset.get_qrels()

    # Warm up cache.
    if not mono_t5.built():
        mono_t5.build(row for _, row in retriever.transform(topics).iterrows())

    # Run experiment
    return Experiment(
        retr_systems=[
            retriever,
            (retriever % 100) >> mono_t5,
            RetrieverCache(
                str(retrieve_duo_t5_cache_dir),
                (((retriever % 100) >> mono_t5) % 5) >> duo_t5,
                verbose=True,
            ) ^ ((retriever % 100) >> mono_t5),
        ],
        names=[
            "ChatNoir",
            "ChatNoir+monoT5",
            "ChatNoir+monoT5+duoT5",
        ],
        topics=topics,
        qrels=qrels,
        eval_metrics=[nDCG @ 5],
        verbose=True,
        save_dir=str(experiment_cache_dir),
        save_mode="reuse",
    )


experiments = get([run_experiment.remote(config) for config in configs])
print(experiments)
