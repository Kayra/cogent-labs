
Install app:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run server:

```bash
uvicorn server:app --reload
```


Upload image:

```bash
curl --request POST \
--url http://127.0.0.1:8000/thumbnail/ \
--header 'Content-Type: multipart/form-data' \
--form image=@example_image.jpg
```
