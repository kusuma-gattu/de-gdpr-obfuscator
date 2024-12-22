import pytest, logging, os
import pandas as pd
from unittest.mock import MagicMock, patch
from src.obfuscator_tool import (
    read_data,
    lambda_handler
)


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
    
    
class Test_lambda_handler:
    
    @patch("src.obfuscator_tool.boto3.client")
    @patch("src.obfuscator_tool.read_data")
    def test_lambda_handler_success(self, mock_read_data, mock_boto_client):
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        
        mock_s3.get_object.return_value = {"Body": MagicMock(read=lambda: b"name,email,contact\nkusuma,kusuma@mail.com")}

        mock_read_data.return_value = "/tmp/ty123.cvs"
        
        event = {
            "file_to_obfuscate": "s3://bucket_name/test.csv",
            "pii_fields": ["email"]
        }
        
        response = lambda_handler(event, None)
        
        assert response["status_code"] == 200
        assert response["file"] == "/tmp/ty123.cvs"
        
    
    @patch("src.obfuscator_tool.boto3.client")
    def test_lambda_handler_invalid_s3(self, mock_boto_client, caplog):
        event = {
            "file_to_obfuscate": "invalid_s3_url",
            "pii_fields": ["email"]
        }
        
        with caplog.at_level(logging.ERROR):  
            lambda_handler(event, None)
        assert "Invalid S3 URL format" in caplog.text 
        
        
    
    
