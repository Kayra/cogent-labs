import shutil

from fastapi import FastAPI, File, UploadFile, BackgroundTasks

from thumbnail_resizer import image_to_thumbnail


app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello Cogent'}


@app.post('/thumbnail/')
async def resize_image(background_tasks: BackgroundTasks, image: UploadFile = File(...)):

    with open('destination.jpg', 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)

    background_tasks.add_task(image_to_thumbnail, image.file)

    return {'filename': image.filename}
