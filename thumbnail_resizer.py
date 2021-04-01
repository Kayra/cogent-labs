from PIL import Image



size = 100, 100

image = Image.open('example_image.jpg')
resized_image = image.resize(size)
resized_image.save('thumbnail.jpg')
