"""Aplication entry point.

The module contains FastAPI application instance and its configuration.
"""


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.router import router as auth_router
from post.router import router as post_router

title = "SpaceWiki API"
discription = """
The SpaceWiki API is designed to provide access to space-related
content from our SpaceWiki platform.
This API allowsusers to retrieve information about planets,
stars, solar systems,and space-related vocabulary."""

VERSION = "0.0.1"

app = FastAPI(
    title=title,
    description=discription,
    version=VERSION
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    'https://space-wiki-main.vercel.app/'
    # add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    # everything from localhost for now,
    allow_origins=origins,
    allow_credentials=True,  # allow cookies
    allow_methods=["GET", "POST", "PUT",
                   "DELETE", "OPTIONS"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)

app.include_router(auth_router, tags=["auth"], prefix="/v1/auth")
app.include_router(post_router, tags=["post"], prefix="/v1/post")
@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Such empty. More content coming soon."}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app)  # you can change host, port, etc using kwargs
