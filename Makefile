deploy: node_modules
	serverless deploy --verbose

node_modules:
	npm i

clean: remove

remove:
	- serverless remove

dist-clean: remove
	- rm -rf node_modules package-lock.json
	- find . -name .serverless -exec rm -rf "{}" +
