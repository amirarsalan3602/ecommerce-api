from Bucket import bucket
from celery import shared_task


def all_bucket_objects_task():
    result = bucket.get_object()
    return result


@shared_task
def delete_object_task(key):
    bucket.delete_object(key)