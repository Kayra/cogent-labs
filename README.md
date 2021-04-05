
Install app:

```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run server:

```bash
cd server
uvicorn server:app --reload
```

Run server unit_tests:

```bash
pytest server/unit_tests/ -p no:warnings -vv
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


Build and start server:

```bash
make start
```

Run unit tests in docker container:

```bash
make unit-test
```

Run integration tests in docker container:

```bash
make integration-test
```

Send image to fast view:

```bash
make send-image-fast
```

Send image to queue view:

```bash
make send-image-queue
```