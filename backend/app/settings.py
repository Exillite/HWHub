from envparse import Env

env = Env()
MONGODB = env.str(
    "MONGODB", default="test_database")
MONGODB_URL = env.str(
    "MONGODB_URL", default="mongodb://localhost:27017")
