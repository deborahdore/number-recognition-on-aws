# Guide for the configuration of S3

1. Go to AWS S3 and create a new bucket following the configuration in this [file](bucket_configuration.pdf)
2. Upload the two datasets
3. Add this [policy](policy.json) to the bucket
4. Save the bucket name (es. number-recognition-on-aws-bucket)
5. Create a new bucket, block all access and upload [main.py](../../../spark-job/main.py)