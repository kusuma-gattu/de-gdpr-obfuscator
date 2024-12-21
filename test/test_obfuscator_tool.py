import pytest, logging, os
import boto3
import pandas as pd
from botocore.exceptions import ClientError
from unittest.mock import Mock, patch
from src.obfuscator_tool import (
    read_data,
    lambda_handler
)


@pytest.fixture(scope="function")
def mock_aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

class Test_Read_Data:
           
    def test_read_csv_data(self):
        data = b"name,email,contact\nkusuma,kusuma@mail.com,0123456789\nram,ram@mail.com,0123456789"
        output_file = read_data("csv", data, ["contact"])
        assert os.path.exists(output_file) == True
        df = pd.read_csv(output_file)
        assert df["contact"][1] == "****"
        os.remove(output_file)
               
    def test_read_json_data(self):
        data = pd.DataFrame({
                "name": ["kusuma", "ram"],
                "email": ["kusuma@mail.com", "ram@mail.com"],
                "contact": ["0123456789", "0123456789"]
                }).to_parquet(index=False)
        output_file = read_data("parquet", data, ["email"])
        assert os.path.exists(output_file) == True
        df = pd.read_parquet(output_file)
        assert df["email"][1] == "****"
        os.remove(output_file)

    def test_read_parquet_data(self):
        data = b'[{"name":"kusuma","email":"kusuma@mail.com","contact": "0123456789"}, \
                        {"name":"ram","email":"ram@mail.com","contact":"0123456789"}]'
        output_file = read_data("json", data, ["name"])
        assert os.path.exists(output_file) == True
        df = pd.read_json(output_file)
        assert df["name"][1] == "****"
        os.remove(output_file)
        
    def test_un_supported_file_format(self):
        with pytest.raises(ValueError):
            read_data("xml", b"name,email,contact\nkusuma,kusuma@mail.com,0123456789", "name")
    
    
# class Test_lambda_handler:
    
    


    
    
