clamavs3
========

This Dockerfile and small python script demonstrate using a container to run clamav on an s3 stored object.

It can be run locally or using Scaleway Serverless Containers.

A use case is for exemple to run a call on the container after uploading a file to Scaleway Object Storage.

A metadata is also added to the object with the result of the scan.

```
$ curl -k -X POST -u 'test:test' -F 'bucket=demo-arno' -F 'key=clamav-testfile' https://myfunction.url
{"status": "ok", "result": "('FOUND', 'Win.Test.EICAR_HDB-1')"}

$ aws s3api head-object --bucket demo-arno --key clamav-testfile
{
    "AcceptRanges": "bytes",
    "LastModified": "Mon, 03 Oct 2022 15:07:04 GMT",
    "ContentLength": 68,
    "ContentType": "application/octet-stream",
    "Metadata": {
        "scan-result": "('FOUND', 'Win.Test.EICAR_HDB-1')"
    }
}
```

NB: Current version of this demo will take a lot of time if the object is heavy.
