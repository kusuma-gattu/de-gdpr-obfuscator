import re, io, tempfile, logging, json
import boto3
import pandas as pd
from urllib.parse import urlparse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def read_data(format, data, pii_fields):
    """
    Reads data from a byte stream, anonymizes specified PII fields, 
    and writes the obfuscated data to a temporary file.

    Args:
        format (str): The format of the input data ('csv', 'json', or 'parquet').
        data (bytes): The byte stream of the data to process.
        pii_fields (list): A list of field names containing PII that need to be anonymized.

    Returns:
        dict: The path to the temporary file containing the obfuscated data and buffer object 

    Raises:
        ValueError: If an unsupported file format is provided.
        Exception: For any errors encountered during processing.
    """
    try:
        # Read content into a DataFrame
        if format == 'csv':
            df = pd.read_csv(io.BytesIO(data))
        elif format == 'json':
            df = pd.read_json(io.BytesIO(data))
        elif format == 'parquet':
            df = pd.read_parquet(io.BytesIO(data))
        else:
            raise ValueError(f"Unsupported file format: {format}")
        
        # Anonymize PII fields
        for field in pii_fields:
            if field in df.columns:
                df[field] = "****"
            else:
                logger.warning(f"PII field '{field}' not found in the data")
        buffer = io.StringIO()
        # Write the anonymized data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as temp_file:
            if format == 'csv':
                df.to_csv(temp_file.name, index=False)
                df.to_csv(buffer)
            elif format == 'json':
                df.to_json(temp_file.name, orient="records")
                df.to_json(buffer)
            elif format == 'parquet':
                df.to_parquet(temp_file.name, index=False)
                df.to_parquet(buffer)
                            
            logger.info(f"Data successfully written to {temp_file.name}")
            return {
                'file': temp_file.name,
                'buffer': buffer
            }

    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise


def lambda_handler(event, context):
    """
    AWS Lambda function handler to read a file from S3, 
    anonymize specified PII fields, and return the obfuscated file's path.

    Args:
        event (dict): Event data passed by the Lambda trigger, expected to contain:
            - 'file_to_obfuscate' (str): S3 URL of the file to process.
            - 'pii_fields' (list): List of PII field names to be anonymized.
        context (object): Lambda context runtime information (not used).

    Returns:
        dict: A dictionary with 'status_code' and 'file' keys, where:
            - 'status_code' is the HTTP status code.
            - 'file' is the path to the obfuscated file.

    Raises:
        Exception: For any errors encountered during execution.
    """
    try:
        # get s3 url from input
        s3_url = event['file_to_obfuscate']
        # extract bucket name and object key from s3 url
        url = urlparse(s3_url)
        logger.info(url)
        if url.scheme == 's3':
            # check if S3 url has bucket name
            if url.netloc:
                bucket_name = url.netloc
            else:
                logger.warning("S3 url is missing bucket name")
            # ckeck S3 url has object key
            if url.path:
                object_key = url.path.lstrip("/")
            else:
                logger.warning("S3 url is missing object key")              
        else:
            logger.error("Invalid S3 URL format")

        # create s3 client
        s3_client = boto3.client("s3")
        # get data object
        if bucket_name and object_key: 
            response = s3_client.get_object(
                Bucket = bucket_name,
                Key = object_key
            )
            # read data from response
            data = response['Body'].read()
            # check file type
            file_format = re.search(r"([.])([a-z]+)", s3_url)
            file_format = file_format.group(2) 
            file_name = re.search(r"[a-z0-9_-]+[.][a-z]+", s3_url)      
            output = read_data(file_format, data, event['pii_fields'])
             # Optional: ingest data into S3 bucket
            res = s3_client.put_object(
                Body = output['buffer'].getvalue(),
                Bucket = bucket_name,
                Key = f"transformed/{file_name.group()}"
            )
            if res["ResponseMetadata"]["HTTPStatusCode"] == 200:
                logger.info(f"file ingested successfully into S3")
            if output:
                return {
                "status_code" : 200,
                "file": output['file']
            }
         
    except Exception as e:
        logger.error(e)
