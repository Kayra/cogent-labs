
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

Get image:

```bash
curl -O --request GET \
  --url http://127.0.0.1:8000/thumbnail/f52896c1-8833-4a1e-b84e-ba4c9dfa1c15.jpg
```