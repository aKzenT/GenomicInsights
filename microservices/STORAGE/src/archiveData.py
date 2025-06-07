import os
import shutil
import hashlib
import base64
import json
import requests

def archiveData(directory_name):
    # Define the source and destination directories for copying the file
    source_file = '../archivematica-metadata/processingMCP.xml'
    destination_dir = f'/cache/{directory_name}'

    # Ensure the destination directory exists
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    # Copy the processingMCP.xml file to the destination directory
    try:
        shutil.copy(source_file, destination_dir)
        print(f"Copied {source_file} to {destination_dir}")
    except Exception as e:
        print(f"Error copying {source_file}: {e}")
        return
    
    # Create checksum.md5 file in the destination directory
    checksum_file = os.path.join(destination_dir, 'metadata', 'checksum.md5')
    
    try:
        with open(checksum_file, 'w') as checksum:
            # Recursively calculate MD5 checksums for each file in the directory
            for root, dirs, files in os.walk(destination_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file != 'checksum.md5':  # Skip the checksum file
                        # Calculate the MD5 checksum
                        md5_hash = hashlib.md5()
                        with open(file_path, 'rb') as f:
                            while chunk := f.read(8192):
                                md5_hash.update(chunk)
                        checksum_value = md5_hash.hexdigest()
                        relative_path = os.path.relpath(file_path, start=destination_dir)
                        checksum.write(f"{checksum_value}  {relative_path}\n")
            print(f"Checksum written to {checksum_file}")
    except Exception as e:
        print(f"Error writing checksum.md5: {e}")
        return    
    
    # Get the base64 encoding of ARCHIVEMATICA_LOCATION_UUID:/home/archivematica_submodules/microbiome/{directory_name}
    try:
        with open('../archivematica-metadata/.env', 'r') as env_file:
            env_vars = {}
            for line in env_file:
                key, value = line.strip().split('=', 1)
                env_vars[key] = value
        location_uuid = env_vars.get('ARCHIVEMATICA_LOCATION_UUID')
        if location_uuid is None:
            print("ARCHIVEMATICA_LOCATION_UUID not found in .env file.")
            return
        
        # Create the path string and base64 encode it
        path_string = f"{location_uuid}:/home/archivematica/microbiome/{directory_name}"
        path = base64.b64encode(path_string.encode('utf-8')).decode('utf-8')
        print(f"Encoded path: {path}")
    except Exception as e:
        print(f"Error reading .env or base64 encoding: {e}")
        return

    # Send the cURL request via Python's requests library
    try:
        with open('../archivematica-metadata/.env', 'r') as env_file:
            env_vars = {}
            for line in env_file:
                key, value = line.strip().split('=', 1)
                env_vars[key] = value

        # Prepare the cURL request data
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"ApiKey {env_vars['USERNAME']}:{env_vars['ARCHIVEMATICA_API_KEY']}"
        }
        data = {
            "name": directory_name,
            "type": "standard",
            "processing_config": "default",
            "accession": "1",
            "access_system_id": "1",
            "auto_approve": True,
            "path": path,
            "metadata_set_id": ""
        }

        # Sending the request to Archivematica's API
        api_url = f"http://{env_vars['ARCHIVEMATICA_IP']}/api/v2beta/package/"
        response = requests.post(api_url, headers=headers, data=json.dumps(data))

        # Check if the request was successful
        if response.status_code == 201 or response.status_code == 202 or response.status.code == 200:
            delete_path = os.path.join('/cache', dir_name)
            shutil.rmtree(delete_path)
            print(f"Package created successfully: {response.json()}")
        else:
            print(f"Failed to create package: {response.status_code}, {response.text}")

        # Retry logic if the request fails
        attempts = 3
        for attempt in range(attempts):
            response = requests.post(api_url, headers=headers, data=json.dumps(data))

        # Check if the request was successful
            if response.status_code == 201 or response.status_code == 202 or response.status_code == 200:
                delete_path = os.path.join('/cache', directory_name)
                shutil.rmtree(delete_path)
                print(f"Package created successfully: {response.json()}")
                break  # Exit the loop on success
            else:
                print(f"Attempt {attempt + 1} failed: {response.status_code}, {response.text}")
                if attempt < attempts - 1:
                    print("Retrying...")
                    time.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    print("Max attempts reached. Failed to create package.")
    except Exception as e:
        print(f"Error sending cURL request: {e}")
        