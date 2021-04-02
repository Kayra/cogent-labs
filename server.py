import os
import uuid

from fastapi.responses import FileResponse, JSONResponse
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Request

from thumbnail_resizer import image_to_thumbnail


app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello Cogent'}


@app.post('/thumbnail/', status_code=202)
async def resize_image(request: Request, background_tasks: BackgroundTasks, image: UploadFile = File(...)):

    image_extension = os.path.splitext(image.filename)[1]
    thumbnail_name = str(uuid.uuid4()) + image_extension

    background_tasks.add_task(image_to_thumbnail, image.file, thumbnail_name)

    thumbnail_url = os.path.join(str(request.url), thumbnail_name)

    return {'filename': thumbnail_url}


@app.get('/thumbnail/{thumbnail_name}', status_code=202)
async def return_resized_image(thumbnail_name: str):

    if os.path.isfile(thumbnail_name):
        return FileResponse(thumbnail_name)
    else:
        return JSONResponse(status_code=404, content={"message": "Image not found"})
