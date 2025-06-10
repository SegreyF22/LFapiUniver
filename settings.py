"""File with settings and config for the project"""

from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://fapi:fapi@localhost:15432/fapi"
)
