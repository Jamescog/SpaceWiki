"""FastAPI Router for authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from werkzeug.security import check_password_hash, generate_password_hash

from auth.schemas import (LoginSuccess, SignupSuccess, UserLoginDefault,
                          UserSignupDefault)
from auth.utils import create_token, decode_token
from database import user_collection


router = APIRouter(
    tags=["auth"]
)
security = HTTPBearer()


@router.post("/signup",
             response_model=SignupSuccess,
             status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignupDefault):
    """Signup endpoint."""
    query = {
        "$or": [
            {"username": user.username},
            {"email": user.email}
        ]
    }
    in_db = await user_collection().find_one(query)

    if in_db:
        raise HTTPException(status_code=400,
                            detail="User already exists.")
    else:
        user_dict = dict(user)
        user_dict["password_hash"] =\
            generate_password_hash(user_dict["password"])
        del user_dict["password"]
        await user_collection().insert_one(user_dict)
        return {"message": "User created successfully."}


@router.post("/login",
             response_model=LoginSuccess,
             status_code=status.HTTP_200_OK)
async def login(user: UserLoginDefault):
    """Login endpoint."""
    query = {
        "$or": [
            {"username": user.username},
            {"email": user.username}
        ]
    }
    user_in_db = await user_collection().find_one(query)
    if user_in_db:
        if check_password_hash(user_in_db["password_hash"], user.password):
            return {"token": create_token({"username": user.username})}
        else:
            raise HTTPException(status_code=401,
                                detail="Invalid credentials.")
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials.")


@router.get("/get-me")
async def get_me(credentials: HTTPAuthorizationCredentials
                 = Depends(security)):
    """Get the current user."""
    bearer_token = credentials.credentials
    res = decode_token(bearer_token)
    if "error" in res:
        raise HTTPException(status_code=401, detail=res["error"])
    else:
        user = await user_collection().find_one({"username": res["username"]})
        del user["password_hash"]
        user["_id"] = str(user["_id"])
        return user
