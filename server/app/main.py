import os
import uuid
import aiofiles

from celery.result import AsyncResult
from fastapi.responses import FileResponse, JSONResponse
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Request

from validators import is_valid_image
from worker import image_to_thumbnail


app = FastAPI()
VALID_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
STATIC_FILE_LOCATION = os.path.dirname(os.path.realpath(__file__))


@app.get('/')
async def root():
    return {'message': 'Hello Cogent'}


@app.post('/thumbnail/', status_code=202)
async def resize_image(request: Request, background_tasks: BackgroundTasks, image: UploadFile = File(...)):

    if not is_valid_image(image.file, image.filename, VALID_IMAGE_EXTENSIONS):
        return JSONResponse(status_code=400,
                            content={"Error": f"Image is not valid. Please ensure extension and file is of one of the following formats: {VALID_IMAGE_EXTENSIONS}"})

    image_extension = os.path.splitext(image.filename)[1]
    thumbnail_name = str(uuid.uuid4()) + image_extension

    background_tasks.add_task(image_to_thumbnail, image.file, thumbnail_name)

    thumbnail_url = os.path.join(str(request.url), thumbnail_name)

    return {'Resized image URL': thumbnail_url}


@app.get('/thumbnail/{thumbnail_name}', status_code=200)
async def return_resized_image(thumbnail_name: str):

    if os.path.isfile(thumbnail_name):
        return FileResponse(thumbnail_name)
    else:
        return JSONResponse(status_code=404, content={"Error": "Image not found"})


@app.post('/thumbnail-queue/', status_code=202)
async def resize_image_queue(request: Request, image: UploadFile = File(...)):

    if not is_valid_image(image.file, image.filename, VALID_IMAGE_EXTENSIONS):
        return JSONResponse(status_code=400,
                            content={"Error": f"Image is not valid. Please ensure extension and file is of one of the following formats: {VALID_IMAGE_EXTENSIONS}"})

    image_extension = os.path.splitext(image.filename)[1]
    thumbnail_id = str(uuid.uuid4())
    thumbnail_name = thumbnail_id + image_extension
    file_location = os.path.join(STATIC_FILE_LOCATION, thumbnail_name)

    async with aiofiles.open(file_location, 'wb') as out_file:
        while content := await image.read(1024):
            await out_file.write(content)

    image_to_thumbnail.apply_async(args=[file_location, thumbnail_name], task_id=thumbnail_id)

    thumbnail_url = os.path.join(str(request.url), thumbnail_name)

    return {'Resized image URL': thumbnail_url}


@app.get('/thumbnail-queue/{thumbnail_name}', status_code=200)
async def return_resized_image_queue(thumbnail_name: str):

    thumbnail_id = os.path.splitext(thumbnail_name)[0]
    result_status = AsyncResult(thumbnail_id).status

    if result_status == 'SUCCESS':
        return FileResponse(thumbnail_name)
    else:
        return JSONResponse(status_code=409, content={"Processing": f"Current status of image processing is {result_status}."})
