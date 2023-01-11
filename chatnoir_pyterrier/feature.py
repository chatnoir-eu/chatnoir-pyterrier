from enum import unique, auto, Flag
from functools import reduce
from operator import or_


def _combine_flags(*flags):
    return reduce(or_, flags)


@unique
class Feature(Flag):
    NONE = 0
    UUID = auto()
    TREC_ID = auto()
    WARC_ID = auto()
    IDS = _combine_flags(UUID, TREC_ID, WARC_ID)
    INDEX = auto()
    CRAWL_DATE = auto()
    TARGET_HOSTNAME = auto()
    TARGET_URI = auto()
    TARGET = _combine_flags(TARGET_HOSTNAME, TARGET_URI)
    CACHE_URI = auto()
    PAGE_RANK = auto()
    SPAM_RANK = auto()
    RANKS = _combine_flags(PAGE_RANK, SPAM_RANK)
    TITLE_HIGHLIGHTED = auto()
    TITLE_TEXT = auto()
    TITLE = _combine_flags(TITLE_HIGHLIGHTED, TITLE_TEXT)
    SNIPPET_HIGHLIGHTED = auto()
    SNIPPET_TEXT = auto()
    SNIPPET = _combine_flags(SNIPPET_HIGHLIGHTED, SNIPPET_TEXT)
    EXPLANATION = auto()
    CONTENT = auto()
    CONTENT_PLAIN = auto()
    CONTENT_TYPE = auto()
    LANGUAGE = auto()
    ALL = _combine_flags(
        UUID, TREC_ID, INDEX, TARGET, RANKS, TITLE, SNIPPET, EXPLANATION,
        CONTENT, CONTENT_PLAIN
    )
    ALL_STAGING = _combine_flags(
        ALL, WARC_ID, CRAWL_DATE, CACHE_URI, CONTENT_TYPE, LANGUAGE
    )
