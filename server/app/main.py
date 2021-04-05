import os

from fastapi import FastAPI

from views.thumbnail_views import router as thumbnail_views_router


app = FastAPI()
VALID_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
STATIC_FILE_LOCATION = os.path.dirname(os.path.realpath(__file__))


@app.get('/')
async def root():
    return {'message': 'Hello Cogent'}


app.include_router(thumbnail_views_router)
