"""Aplication entry point.

The module contains FastAPI application instance and its configuration.
"""


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

title = "SpaceWiki API"
discription = """
The SpaceWiki API is designed to provide access to space-related
content from our SpaceWiki platform.
This API allowsusers to retrieve information about planets,
stars, solar systems,and space-related vocabulary."""

version = "0.0.1"

app = FastAPI(
    title=title,
    description=discription,
    version=version
)

app.add_middleware(
    CORSMiddleware,
    # everything from localhost for now,
    allow_origin_regex="^http://.*localhost.*",
    allow_credentials=True,  # allow cookies
    allow_methods=["GET", "POST", "PUT",
                   "DELETE", "OPTIONS"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)

@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Such empty. More content coming soon."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)  # you can change host, port, etc using kwargs
