from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from routers import auth, post, user, vote


description = """
### Posts
You can create, read, update and delete posts.
All action except for reading post require authentication.

### Users
You can create users and retrieve user data.

### Vote
You can vote for posts.
"""
tags_metadata = [
    {
        "name": "Posts",
        "description": "CRUD operations with posts.",
    },
    {
        "name": "Users",
        "description": "Create and retrieve users.",
    },
    {
        "name": "Vote",
        "description": "Upvote and downvote posts (1 for upvote and 0 for downvote).",
    },
]

app = FastAPI(title="Simple Blog Application", description=description, openapi_tags=tags_metadata)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return RedirectResponse("/docs")
