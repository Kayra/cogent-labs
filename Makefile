.PHONY: start unit-tests integration-tests send-image


start:
	@docker-compose up


unit-tests:
	@docker exec -it cogent.server pytest tests/unit_tests/ -p no:warnings -vv


integration-tests:
	@docker exec -it cogent.server pytest tests/integration_tests/ -p no:warnings -vv


send-image:
	@curl --request POST \
     --url http://127.0.0.1:8000/thumbnails/ \
     --header 'Content-Type: multipart/form-data' \
     --form image=@example_image.jpeg \
     --form sizes=200
