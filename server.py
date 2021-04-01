import shutil

from fastapi import FastAPI, File, UploadFile

from thumbnail_resizer import image_to_thumbnail


app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello Cogent'}


@app.post('/thumbnail/')
async def resize_image(image: UploadFile = File(...)):

    with open('destination.jpg', 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': image.filename}
