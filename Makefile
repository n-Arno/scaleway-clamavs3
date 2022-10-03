all:
	docker build . -t clamavs3:latest

test:
	./test.sh
