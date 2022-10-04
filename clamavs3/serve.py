import os, sys, uuid, subprocess

import pyclamd
import boto3
from botocore.exceptions import ClientError as BotoClientError
from bottle import run, route, request, response, auth_basic

def check_pass(username, password):
    return username == os.environ.get("LOGIN") and password == os.environ.get("PASSWORD")


@route("/", method="GET")
def root_get():
    cd = pyclamd.ClamdAgnostic()
    response.status = 200
    return {"status": "ok", "version": cd.version()}


@route("/fresh", method="GET")
@auth_basic(check_pass)
def fresh_get():
    exec = subprocess.run(["freshclam"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if exec.returncode == 0:
        response.status = 200
        return {"status": "ok", "result": exec.stdout.decode('utf-8')}
    else:
        response.status = 500
        return {"status": "ko", "result": exec.stdout.decode('utf-8')}

@route("/", method="POST")
@auth_basic(check_pass)
def root_post():
    bucket = request.forms.get("bucket")
    key = request.forms.get("key")
    if not bucket or not key:
        response.status = 400
        return {
            "status": "ko",
            "reason": "bad request (missing either/or bucket/key parameter)",
        }

    region = os.environ.get("REGION")
    if not region:
        response.status = 500
        return {"status": "ko", "reason": "server error, REGION is missing"}

    cd = pyclamd.ClamdAgnostic()
    s3 = boto3.resource(
        "s3", endpoint_url=f"https://s3.{region}.scw.cloud/", region_name=region
    )

    try:
        temp_uuid = uuid.uuid4()
        s3.Bucket(bucket).download_file(key, f"/scandir/{temp_uuid}")
        found = cd.scan_file(f"/scandir/{temp_uuid}")
        os.remove(f"/scandir/{temp_uuid}")
        result = "('CLEAN','')" if not found else str(found[f"/scandir/{temp_uuid}"])
        s3_object = s3.Object(bucket, key)
        s3_object.metadata.update({"scan-result": result})
        s3_object.copy_from(
            CopySource={"Bucket": bucket, "Key": key},
            Metadata=s3_object.metadata,
            MetadataDirective="REPLACE",
        )
        response.status = 200
        return {"status": "ok", "result": result}
    except BotoClientError as e:
        response.status = int(e.response["Error"]["Code"])
        return {"status": "ko", "reason": e.response["Error"]["Message"]}

if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, server='paste')
