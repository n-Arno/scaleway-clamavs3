#!/bin/bash
docker run -d --name test --rm -p 8080:8080 -e LOGIN=test -e PASSWORD=test -e REGION=fr-par -e AWS_ACCESS_KEY_ID=$SCW_ACCESS_KEY -e AWS_SECRET_ACCESS_KEY=$SCW_SECRET_KEY clamavs3:latest
sleep 45
curl -X POST -u 'test:test' -F 'bucket=demo-arno' -F 'key=clamav-testfile' http://localhost:8080
