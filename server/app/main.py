import os

from fastapi import FastAPI

from views.fast_views import router as fast_views_router
from views.queue_views import router as queue_views_router


app = FastAPI()
VALID_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
STATIC_FILE_LOCATION = os.path.dirname(os.path.realpath(__file__))


@app.get('/')
async def root():
    return {'message': 'Hello Cogent'}


app.include_router(fast_views_router)
app.include_router(queue_views_router)
