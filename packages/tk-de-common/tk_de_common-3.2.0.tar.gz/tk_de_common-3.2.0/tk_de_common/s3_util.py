"""A class providing common s3 functions"""
import json
import os
import boto3
from botocore.exceptions import ClientError


class S3Util:
    """Provides common s3 functions"""
    def __init__(self, bucket=None):
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket or self.get_bucket()

    def prefix(self, key):
        if os.environ.get('S3_PREFIX') is None:
            return key

        return f"{os.environ.get('S3_PREFIX')}/{key}"

    def get_bucket(self):
        """Get the bucket name from the environment or raise exception"""
        if os.environ.get('S3_BUCKET') is None:
            raise ValueError('S3_BUCKET environment variable not set')
        return os.environ.get('S3_BUCKET')

    def exists(self, key):
        try:
            client = boto3.client('s3')
            client.head_object(Bucket=self.bucket_name, Key=self.prefix(key))
            return True
        except ClientError:
            return False

    def read_json(self, key):
        return json.loads(self.read_file(key))

    def write_json(self, key, data):
        self.write_file(key, json.dumps(data))

    def read_file(self, key):
        obj = self.s3.Object(self.bucket_name, self.prefix(key))
        return obj.get()['Body'].read().decode('utf-8')

    def write_file(self, key, data):
        self.s3.Object(self.bucket_name, self.prefix(key)).put(Body=data)

    def delete_file(self, key: str):
        """Deletes a file from S3"""
        self.s3.delete_object(Bucket=self.bucket_name, Key=key)

    def list_contents(self, prefix: str = None) -> list:
        """Return list of keys within the bucket/prefix set, 1000 keys max per call"""
        items = []
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)

        try:
            for obj in response['Contents']:
                if obj['Key'][-1] == '/':
                    continue

                items.append(obj['Key'])
        except KeyError:
            return None

        return items

    def copy_file(self, source_key, destination_key):
        """Copies a file from one location to another"""
        copy_source = {
            'Bucket': self.bucket_name,
            'Key': source_key
        }
        self.s3.meta.client.copy(copy_source, self.bucket_name, destination_key)
