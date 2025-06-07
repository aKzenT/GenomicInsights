import requests
import json

def get_hdfs_file_status(verzeichnisname):
    url = f"http://192.168.178.27:9870/webhdfs/v1/{verzeichnisname}?op=LISTSTATUS&namenoderpcaddress=namenode:9000"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            result = []
            for file_status in data['FileStatuses']['FileStatus']:
                result.append({
                    "pathSuffix": file_status['pathSuffix'],
                    "type": file_status['type']
                })
            
            return {'files': result}
        else:
            return f"Fehler: HTTP {response.status_code}"

    except Exception as e:
        return f"Fehler bei der Anfrage: {str(e)}"
