import boto3
import base64

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = "your-bucket-name"
    file_name = event['fileName']
    file_content = base64.b64decode(event['fileContent'])

    s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
    return {"message": "File uploaded successfully"}