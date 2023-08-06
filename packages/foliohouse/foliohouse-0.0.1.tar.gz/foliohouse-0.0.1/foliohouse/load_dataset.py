import io
import csv
import pandas as pd
from Crypto.Cipher import AES
import requests

def load_dataset(file_url: str) -> pd.DataFrame:

    secret_key = "0ed60d684aea75f4f4c761c9d9beab51"
    response = requests.get(file_url)
    
    encrypted_data = response.content
    
    # Extract initialization vector (IV)
    iv = encrypted_data[:16]

    # Decrypt data
    cipher = AES.new(secret_key.encode(), AES.MODE_GCM, iv)
    decrypted_data = cipher.decrypt(encrypted_data[16:])

    # Convert decrypted data to string and parse CSV
    transaltion_table = bytes.maketrans(b'', b'')
    decrypted_data = decrypted_data.translate(transaltion_table, b'\x80-\xff')
    decoded_data = decrypted_data.decode('utf-8','ignore')
    # Replace all newline and null characters within CSV data
    decoded_data = decoded_data.replace('\r\n', '\n').replace('\r', '\n').replace('\x00', '')
    # Parse CSV using csv.reader()
    df = pd.read_csv(io.StringIO(decoded_data))

    api_endpoint = 'https://foliohouse-prototype.vercel.app/api/datasetaccess'
    payload = {
        "dataset": file_url
    }
    api_response = requests.get(api_endpoint, json=payload)
    print(api_response.status_code)

    return df