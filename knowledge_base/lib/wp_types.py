from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class WPPost:
    """Represents a WordPress post/doc."""
    id: Optional[int] = None
    title: str = ""
    slug: str = ""
    content: str = ""
    status: str = "draft"  # draft, publish, pending, private
    categories: List[int] = field(default_factory=list)
    meta: Dict[str, str] = field(default_factory=dict)
    featured_image: Optional[int] = None
    link: str = ""
    excerpt: str = ""


@dataclass
class WPCategory:
    """Represents a WordPress category/taxonomy term."""
    id: Optional[int] = None
    name: str = ""
    slug: str = ""
    parent: int = 0
    count: int = 0
    taxonomy: str = "category"


@dataclass
class WPMedia:
    """Represents an uploaded media attachment."""
    id: Optional[int] = None
    source_url: str = ""
    alt_text: str = ""
    title: str = ""
    mime_type: str = ""


@dataclass
class RedirectEntry:
    """A URL redirect mapping."""
    old_url: str = ""
    new_url: str = ""
    redirect_type: int = 301
