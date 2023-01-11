from enum import unique, auto, Flag


@unique
class Feature(Flag):
    NONE = 0
    UUID = auto()
    TREC_ID = auto()
    WARC_ID = auto()
    IDS = UUID | TREC_ID | WARC_ID
    INDEX = auto()
    CRAWL_DATE = auto()
    TARGET_HOSTNAME = auto()
    TARGET_URI = auto()
    TARGET = TARGET_HOSTNAME | TARGET_URI
    CACHE_URI = auto()
    PAGE_RANK = auto()
    SPAM_RANK = auto()
    RANKS = PAGE_RANK | SPAM_RANK
    TITLE_HIGHLIGHTED = auto()
    TITLE_TEXT = auto()
    TITLE = TITLE_HIGHLIGHTED | TITLE_TEXT
    SNIPPET_HIGHLIGHTED = auto()
    SNIPPET_TEXT = auto()
    SNIPPET = SNIPPET_HIGHLIGHTED | SNIPPET_TEXT
    EXPLANATION = auto()
    CONTENT = auto()
    CONTENT_PLAIN = auto()
    CONTENT_TYPE = auto()
    LANGUAGE = auto
    ALL = (
            UUID | TREC_ID | INDEX | TARGET | RANKS | TITLE | SNIPPET |
            EXPLANATION | CONTENT | CONTENT_PLAIN
    )
    ALL_STAGING = ALL | IDS | CRAWL_DATE | CACHE_URI | CONTENT_TYPE | LANGUAGE
