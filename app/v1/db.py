from pymongo import MongoClient
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient(os.getenv("MONGO")) 
db = client['dominical']