.PHONY: install start restart database dotenv servershell psqlshell testunit testinteg teste2e testall


start:
	@docker-compose up


test:
	@docker exec -it cogent.server pytest tests/ -p no:warnings -vv


send-image:
	@curl --request POST \
     --url http://127.0.0.1:8000/thumbnail/ \
     --header 'Content-Type: multipart/form-data' \
     --form image=@example_image.jpg

