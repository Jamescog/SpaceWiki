"""This module contains database connection logic."""


from motor.motor_asyncio import AsyncIOMotorClient
from os import getenv
from dotenv import load_dotenv, find_dotenv
import asyncio

load_dotenv(find_dotenv())

def connect_to_mongodb():
    """Connect to MongoDB."""
    mongodb_uri = getenv("DB_URI")
    mongodb_client = AsyncIOMotorClient(mongodb_uri)
    return mongodb_client

def user_collection():
    """Return user collection."""
    mongodb_client = connect_to_mongodb()
    return mongodb_client[getenv("DB_NAME")]["users"]

def post_collection():
    """Return post collection."""
    mongodb_client = connect_to_mongodb()
    return mongodb_client[getenv("DB_NAME")]["posts"]
