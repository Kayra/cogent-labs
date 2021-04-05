.PHONY: start unit-test send-image


start:
	@docker-compose up


unit-test:
	@docker exec -it cogent.server pytest unit_tests/ -p no:warnings -vv


send-image:
	@curl --request POST \
     --url http://127.0.0.1:8000/thumbnail/ \
     --header 'Content-Type: multipart/form-data' \
     --form image=@example_image.jpg
