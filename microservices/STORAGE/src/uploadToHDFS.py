import os
import requests
import shutil

# Function to upload files and directories to HDFS
def upload_to_hdfs(local_path, hdfs_path):
    if os.path.isdir(local_path):
        # Create the directory on HDFS
        print(f"Creating directory on HDFS: {hdfs_path}")
        url = f"http://192.168.178.27:9864/webhdfs/v1{hdfs_path}?op=MKDIRS&namenoderpcaddress=namenode:9000"
        requests.put(url)

        for item in os.listdir(local_path):
            local_item_path = os.path.join(local_path, item)
            hdfs_item_path = os.path.join(hdfs_path, item)
            upload_to_hdfs(local_item_path, hdfs_item_path)
        shutil.rmtree(local_path)

    else:
        print(f"Uploading file: {local_path}")
        url = f"http://192.168.178.27:9864/webhdfs/v1{hdfs_path}?op=CREATE&namenoderpcaddress=namenode:9000&createflag=&createparent=true&overwrite=false"
        with open(local_path, 'rb') as file:
            requests.put(url, data=file)
        os.remove(local_path)
    