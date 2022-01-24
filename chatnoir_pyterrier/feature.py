from enum import unique, auto, Flag


@unique
class Feature(Flag):
    NONE = 0
    UUID = auto()
    INDEX = auto()
    TARGET_HOSTNAME = auto()
    TARGET_URI = auto()
    TARGET = TARGET_HOSTNAME | TARGET_URI
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
    HTML = auto()
    HTML_PLAIN = auto()
    ALL = (
            UUID | INDEX | TARGET | RANKS | TITLE | SNIPPET | EXPLANATION |
            HTML | HTML_PLAIN
    )
