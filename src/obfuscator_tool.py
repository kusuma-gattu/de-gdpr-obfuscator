import re, io, tempfile, logging
import boto3
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def read_data(format, data, pii_fields):
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
        
        # Write the anonymized data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as temp_file:
            if format == 'csv':
                df.to_csv(temp_file.name, index=False)
            elif format == 'json':
                df.to_json(temp_file.name, orient="records")
            elif format == 'parquet':
                df.to_parquet(temp_file.name, index=False)
            
            logger.info(f"Data successfully written to {temp_file.name}")
            return temp_file.name

    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise


def lambda_handler(event, context):
    try:
        # get s3 url from input
        s3_url = event['file_to_obfuscate']
        # extract bucket name and key from s3 url
        b = s3_url.split("//")
        bucket = re.search(r"[a-z_-]+", b[1])
        bucket_name = bucket.group(0)
        logger.info(f"bucket name: {bucket_name}")
        key = re.search(r"(/)([a-z._0-9-]+/[a-z_.0-9-]+)", b[1])
        object_key = key.group(2)
        logger.info(f"key name: {object_key}")

        # create s3 client
        s3_client = boto3.client("s3")
        # get data object
        response = s3_client.get_object(
            Bucket = bucket_name,
            Key = object_key
        )
        # read data from response
        data = response['Body'].read()
        # check file type
        file_format = re.search(r"([.])([a-z]+)", s3_url)
        file_format = file_format.group(2)       
        output_file = read_data(file_format, data, event['pii_fields']) 
        return {
            "status_code" : 200,
            "file": output_file
        }
           
    except Exception as e:
        logger.error(e)
