# Minio for Local Development

Minio is an open-source object storage server compatible with Amazon S3. This guide explains how to set up and use Minio for local development.

## Setting Up Minio

### 1. Pull Minio Docker Image

First, download the latest Minio Docker image:

```sh
docker pull minio/minio
```

### 2. Run Minio

To start Minio for the first time:

```sh
docker run -d --name minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -e "MINIO_ROOT_USER=admin" \
  -e "MINIO_ROOT_PASSWORD=admin123" \
  minio/minio server /data --console-address ":9001"
```

This command:
- Runs Minio in detached mode (`-d`)
- Names the container "minio" (`--name minio`)
- Maps port 9000 for the API and 9001 for the web console
- Sets the root user and password
- Starts the Minio server with the web console on port 9001

To stop Minio:

```sh
docker stop minio
```

To start Minio again after stopping:

```sh
docker start minio
```

## Using Minio Client (mc)

Minio Client (mc) is a command-line tool for interacting with Minio and other S3-compatible services.

### Setting up mc

First, set an alias for your local Minio server:

```sh
mc alias set dev-minio http://localhost:9000 admin admin123
```

This creates an alias "myminio" for your local Minio server.

### Copying Files to Minio

To copy a local file to a Minio bucket:

```sh
mc mb dev-minio/bucket-name/
mc cp /path/to/local/file dev-minio/bucket-name/

mc mb dev-minio/warmup/
mc cp ./dev/warmup/requests1.jsonl dev-minio/warmup/
mc ls dev-minio/warmup
```


## Accessing Minio

- API Endpoint: http://localhost:9000
- Web Console: http://localhost:9001 (login with admin/admin123)

Use the web console to create buckets, manage files, and configure access policies.


## Using AWS CLI with local minio

```sh
aws configure --profile minio
```

When prompted, enter the following:
- AWS Access Key ID: admin (or your Minio access key)
- AWS Secret Access Key: admin123 (or your Minio secret key)
- Default region name: us-east-1 (this can be any valid region name)
- Default output format: json (or your preferred format)


List buckets:
```
aws --endpoint-url http://localhost:9000 --profile minio s3 ls
```

List contents of a bucket:
```
aws --endpoint-url http://localhost:9000 --profile minio s3 ls s3://warmup
```
