"""FastAPI Router for Post endpoints."""


from fastapi import (APIRouter,
                     Depends,
                     HTTPException,
                     status,
                     File,
                     UploadFile,
                     Form,
                     )
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth.utils import decode_token
from database import post_collection
from bson import ObjectId
from typing import List, Optional
import os
from secrets import token_urlsafe
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
    return {"message": "Post created successfully.", "id": str(post_data["_id"])}


@router.post("/create-with-file",
             status_code=status.HTTP_201_CREATED)
async def create_post_with_file(credentials: HTTPAuthorizationCredentials = Depends(security),
                                title: str = Form(...),
                                content: str = Form(...),
                                tags: List[str] = Form(...),
                                videos: List[UploadFile] = File(...),
                                images: List[UploadFile] = File(...),
                                references: List[str] = Form(None),
                                category: str = Form(...),
                                ):
    """Create post with file endpoint.
    
    Required: Authorization Token(in Autorization header of the request)
    """
    bearer_token = credentials.credentials
    res = decode_token(bearer_token)
    if "error" in  res:
        raise HTTPException(status_code=401, detail=res["error"])
    

    # save the files with unique names
    base_url= "http://localhost:8000/v1/post/files/" # change this in production
    try:
        video_links = []
        image_links = []

        # create the direcotries if they don't exist
        if not os.path.exists("videos"):
            os.makedirs("videos")
        if not os.path.exists("images"):
            os.makedirs("images")
        for video in videos:
            ext = video.filename.split(".")[-1]
            video_name =f"videos/{token_urlsafe(32)}.{ext}"
            with open(video_name, "wb") as f:
                f.write(video.file.read())
            video_links.append(base_url + video_name)

        for image in images:
            ext = image.filename.split(".")[-1]
            image_name = f"images/{token_urlsafe(32)}.{ext}"
            with open(image_name, "wb") as f:
                f.write(image.file.read())
            image_links.append(base_url + image_name)

        

        post_data = {
            "title": title,
            "content": content,
            "tags": tags,
            "video_links": video_links,
            "image_links": image_links,
            "references": references if not references  == [""] else None,
            "category": category,
            "author": res["username"]
        }

        await post_collection().insert_one(post_data)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

    return {"message": "Post created successfully.",
            "id": str(post_data["_id"])
            }

@router.get("/get", response_model=PostResponse)
async def get_post(post_id: str):
    """Returns the post that matches the given id
    
    Required: Post ID(post_id in query parameter)
    """

    post = await post_collection().find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post["_id"] = str(post["_id"])
    return {"post": post}

@router.get("/get-all", response_model=PostResponse)
async def get_all_post(skip: int = 0, limit: int = 10):
    """Returns all the posts
    
    Optional: Skip and Limit parameters(skip and limit in query parameter)
    """

    posts = post_collection().find().skip(skip).limit(limit)
    posts_list = await posts.to_list(length=limit)
    for post in posts_list:
        print(post)
        post["_id"] = str(post["_id"])
    return {"posts": posts_list}




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
async def get_by_author(author: str,
                        skip: int = 0, limit: int = 10):
    """Returns the post(s) that matches given author
    
    Required: Author name(author=author_name in query parameter)
    """

    posts = post_collection().find({"author": author}).skip(skip).limit(limit)
    posts_list = await posts.to_list(length=limit)# length can be customized as needed
    for post in posts_list:
        post["_id"] = str(post["_id"])
    return {"posts": posts_list}


@router.get("/myposts", response_model=PostResponse)
async def get_my_posts(credentials: HTTPAuthorizationCredentials = Depends(security),
                       skip: int = 0, limit: int = 10):
    """Endpoint for user to retrieve his/her post
    
    Required: Authorization Token(in Autorization header of the request)
    """
    bearer_token = credentials.credentials
    res = decode_token(bearer_token)
    if "error" in  res:
        raise HTTPException(status_code=401, detail=res["error"])
    
    posts = post_collection().find({"author": res["username"]}).skip(skip).limit(limit)
    posts_list = await posts.to_list(length=limit)# length can be customized as needed
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




@router.get("/files/{file_path:path}", include_in_schema=False)
async def get_file(file_path: str, download: Optional[str] = False):
    """
    Endpoint to serve files from the server.

    Required: File path to be served.
    Optional: download parameter to force download the file.
    """

    print(file_path)

    if download:
        return FileResponse(file_path, media_type="application/octet-stream", filename=file_path)
    return FileResponse(file_path)