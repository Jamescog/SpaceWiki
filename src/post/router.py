"""FastAPI Router for Post endpoints."""


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth.utils import decode_token
from database import post_collection
from bson import ObjectId
from post.schemas import (PostCreate,
                          PostResponse,
                          EditPost)


security = HTTPBearer()


router = APIRouter(
    tags=["post"]
)

security = HTTPBearer()

@router.post("/create",
             status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Create post endpoint.
    
    Required: Authorization Token(in Autorization header of the request)
    """
    bearer_token = credentials.credentials
    res = decode_token(bearer_token)
    if "error" in  res:
        raise HTTPException(status_code=401, detail=res["error"])
    
    post_data = dict(post)
    post_data["author"] = res["username"]
    try:
        await post_collection().insert_one(post_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return {"message": "Post created successfully."}


@router.get("/get-by-title", response_model=PostResponse)
async def get_by_title(title:str):
    """Returns the post(s) that matches the given title
    
    Required: Title of the post(title=title_string in query parameter)
    """

    posts = post_collection().find({"title": title})
    posts_list = await posts.to_list(length=10)# length can be customized as needed
    for post in posts_list:
        post["_id"] = str(post["_id"])
    return {"posts": posts_list} 

@router.get("/get-by-author", response_model=PostResponse)
async def get_by_author(author: str):
    """Returns the post(s) that matches given author
    
    Required: Author name(author=author_name in query parameter)
    """

    posts = post_collection().find({"author": author})
    posts_list = await posts.to_list(length=10)# length can be customized as needed
    for post in posts_list:
        post["_id"] = str(post["_id"])
    return {"posts": posts_list}


@router.get("/myposts", response_model=PostResponse)
async def get_my_posts(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Endpoint for user to retrieve his/her post
    
    Required: Authorization Token(in Autorization header of the request)
    """
    bearer_token = credentials.credentials
    res = decode_token(bearer_token)
    if "error" in  res:
        raise HTTPException(status_code=401, detail=res["error"])
    
    posts = post_collection().find({"author": res["username"]})
    posts_list = await posts.to_list(length=10)# length can be customized as needed
    for post in posts_list:
        post["_id"] = str(post["_id"])
    return {"posts": posts_list}

@router.put("/edit")
async def edit_my_post(feild: EditPost, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Endpoint for users to edit their post content

    Required: Authorization Token (in Authorization header of the request)
    Required: Field they want to edit.
    """

    bearer_token = credentials.credentials
    res = decode_token(bearer_token)

    feild = dict(feild)
    if "error" in res:
        raise HTTPException(status_code=401, detail=res["error"])

    field_mapping = {
        "title": "title",
        "content": "content",
        "tags": "tags",
        "video_links": "video_links",
        "image_links": "image_links",
        "references": "references",
        "category": "category",
    }

    field_name = feild.feild
    if field_name not in field_mapping:
        raise HTTPException(status_code=400, detail="Invalid field to edit")

    update_field = field_mapping[field_name]
    await post_collection().update_one({"author": res["username"]}, {"$set": {update_field: feild.data}})

    return {"message": "Post updated successfully"}


@router.delete("/posts/{post_id}")
async def delete_user_post(post_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Endpoint for users to delete their own posts.

    Required: Authorization Token (in Authorization header of the request)
    Required: Post ID to be deleted.
    """

    bearer_token = credentials.credentials
    res = decode_token(bearer_token)

    # Validate user authentication
    if "error" in res:
        raise HTTPException(status_code=401, detail=res["error"])

    # Check if the post belongs to the authenticated user
    post = await post_collection().find_one({"_id": ObjectId(post_id), "author": res["username"]})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or does not belong to the user")

    # Delete the post
    await post_collection().delete_one({"_id": ObjectId(post_id)})

    return {"message": "Post deleted successfully"}


    