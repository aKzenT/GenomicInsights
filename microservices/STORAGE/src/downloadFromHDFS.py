import os
import requests
import mimetypes
from io import BytesIO
from fastapi.responses import StreamingResponse

# Function to download files and directories from HDFS
def download_from_hdfs(hdfs_path, local_base_path='../raw', is_Root=True):
    if is_Root:
        dir_name = os.path.basename(hdfs_path.rstrip('/'))
        local_path = os.path.join(local_base_path, dir_name)
    else:
        local_path = local_base_path

    if not os.path.exists(local_path):
        os.makedirs(local_path)

    # HDFS Web URL to list files and directories
    url = f"http://192.168.178.27:9870/webhdfs/v1/{hdfs_path}?op=LISTSTATUS&namenoderpcaddress=namenode:9000"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # Process the files and directories returned
        for file_info in data['FileStatuses']['FileStatus']:
            file_name = file_info['pathSuffix']
            file_hdfs_path = os.path.join(hdfs_path, file_name)
            local_file_path = os.path.join(local_path, file_name)

            if file_info['type'] == 'DIRECTORY':
                download_from_hdfs(file_hdfs_path, local_file_path, is_Root=False)
            else:
                download_file_from_hdfs(file_hdfs_path, local_file_path)
    else:
        print(f"Failed to list contents of {hdfs_path}. Error: {response.text}")
    return {"status": "Download gestartet"}
    

# Helper function to download a single file from HDFS
def download_file_from_hdfs(hdfs_file_path, local_file_path):
    url = f"http://192.168.178.27:9864/webhdfs/v1/{hdfs_file_path}?op=OPEN&namenoderpcaddress=namenode:9000"

    with open(local_file_path, 'wb') as f:
        response = requests.get(url)
        if response.status_code == 200:
            f.write(response.content)
        else:
            print(f"Failed to download file {hdfs_file_path}. Error: {response.text}")

# Function to download and return a file from HDFS
def return_file_from_hdfs(file_path: str):
    open_url = f"http://192.168.178.27:9870/webhdfs/v1/{file_path}"
    params = {
        "op": "OPEN",
        "namenoderpcaddress": "namenode:9000",
        "offset": "0"
    }
    redirect_resp = requests.get(open_url, params=params, allow_redirects=False)

    if redirect_resp.status_code != 307:
        return {"error": f"Unexpected response: {redirect_resp.status_code}"}

    redirect_url = redirect_resp.headers["Location"]
    stream_resp = requests.get(redirect_url, stream=True)

    filename = file_path.split("/")[-1]
    mime_type, _ = mimetypes.guess_type(filename)
    mime_type = mime_type or "application/octet-stream"

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }

    return StreamingResponse(stream_resp.iter_content(chunk_size=8192), media_type=mime_type, headers=headers)