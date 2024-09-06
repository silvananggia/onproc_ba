import os
import wget
import json
import requests

def download_images(data, id_proses):
    reqdata = requests.get(f'https://earth-search.aws.element84.com/v1/collections/sentinel-2-c1-l2a/items/{data}')
   
    if reqdata.status_code != 200:
        raise Exception("Failed to download image metadata.")
    
    jsondata = json.loads(reqdata.text)
    
    folder = os.path.join(f"./workspace/{id_proses}/data")
    os.makedirs(folder, exist_ok=True)

    fldata = os.path.join(folder, data)
    os.makedirs(fldata, exist_ok=True)
    wget.download(jsondata['assets']['nir08']['href'], out=os.path.join(fldata, "B8A.tif"))  # NIR band
    wget.download(jsondata['assets']['swir22']['href'], out=os.path.join(fldata, "B12.tif"))  # SWIR band
