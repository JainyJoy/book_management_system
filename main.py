# Copyright (C) 2020 EdGE Networks Private Limited - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential, no part of this file may be replicated in any form
from fastapi import FastAPI
import uvicorn
import logging
from logging.config import dictConfig
import os
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from routes import book, user, review, summary


log = logging.getLogger('file')
# Set root logger to log DEBUG and above
log.setLevel(logging.DEBUG)
book_app = FastAPI()

# this imports the route in the logger into the app file
book_app.include_router(book.router)
book_app.include_router(user.router)
book_app.include_router(review.router)
book_app.include_router(summary.router)


class Settings(BaseModel):
    authjwt_secret_key: str = os.environ.get("JWT_SECRET_KEY", "my_jwt_secret_key")


@AuthJWT.load_config
def get_config():
    return Settings()

if __name__ == "__main__":
    uvicorn.run(book_app, host="0.0.0.0", port=int(os.environ.get('PORT_NUMBER', 8000)))

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] {%(filename)s:%(lineno)d} %(threadName)s %(levelname)s in %(module)s\
        (PID:%(process)d): %(message)s',
    }},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        'file': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': ''
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
})