"""It contains the schemas for the post module."""


from typing import Optional, List, Any
from pydantic import BaseModel, Field, HttpUrl, validator
from enum import Enum


class PostCategory(str, Enum):
    """Represents the category of a post."""

    NEWS = "news"
    SCIENCE = "science"
    TECHNOLOGY = "technology"
    SPACE = "space"
    OTHER = "other"

    # add more as needed


class EditFeildEnum(str, Enum):
    """Enums for choices of feilds to be edited"""

    TITLE:str = "title",
    CATEGORY: PostCategory = "category"
    CONTENT: str = "content"
    TAGS: list = "tags"
    VIDEO_LINKS: list = "video_links"
    IMAGE_LINKS:str = "image_links"
    REFERENCES:str = "references"



class PostCreate(BaseModel):
    """
    Represents the schema for post creation.

    Attributes:
        title (str): The title of the post.
        content (str): The content of the post.
        tags (list): The tags of the post.
        video_links (list): The video links of the post.
        image_links (list): The image links of the post.
        references (list): The references of the post.
        category (str): The category of the post.
    """

    title: str
    content: str
    tags: List[str]
    video_links: Optional[List[str]] = None
    image_links: Optional[List[str]] = None
    references: Optional[List[str]] = None
    category: PostCategory

    class Config:
        """example schema for the post creation"""
        json_schema_extra = {
            "examples": [
                {
                    "title": "The title of the post",
                    "content": "The content of the post",
                    "tags": ["tag1", "tag2"],
                    "video_links": ["https://www.youtube.com/watch?v=video1",
                                    "https://www.youtube.com/watch?v=video2"],
                    "image_links": ["https://www.image1.com",
                                    "https://www.image2.com"],
                    "references": ["https://www.reference1.com",
                                   "https://www.reference2.com"],
                    "category": "news"
                }
            ]
        }


class Post(BaseModel):
    """Pydanctic class that represents post"""
    _id: str
    title: str
    content: str
    tags: List[str]
    video_links: List[HttpUrl]
    image_links: List[HttpUrl]
    references: List[HttpUrl]
    category: str
    author: str


class EditPost(BaseModel):
    feild: EditFeildEnum
    data:Any

class PostResponse(BaseModel):
    posts: List[Post]
