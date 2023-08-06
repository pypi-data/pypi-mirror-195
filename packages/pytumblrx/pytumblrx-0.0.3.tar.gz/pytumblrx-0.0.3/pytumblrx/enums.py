from strenum import LowercaseStrEnum
from typing import Literal


class PostType(LowercaseStrEnum):
    TEXT = "text"
    PHOTO = "photo"
    QUOTE = "quote"
    LINK = "link"
    CHAT = "chat"
    AUDIO = "audio"
    VIDEO = "video"


PostTypeTyping = Literal["text", "photo", "quote", "link", "chat", "audio", "video"]


class PostFilter(LowercaseStrEnum):
    HTML = "html"
    TEXT = "text"
    RAW = "raw"


PostFilterTyping = Literal["html", "text", "raw"]


class PostState(LowercaseStrEnum):
    PUBLISHED = "published"
    DRAFT = "draft"
    QUEUE = "queue"
    PRIVATE = "private"


PostStateTyping = Literal['published', 'draft', 'queue', 'private']


class PostFormat(LowercaseStrEnum):
    HTML = "html"
    MARKDOWN = "markdown"


PostFormatTyping = Literal['html', 'markdown']
