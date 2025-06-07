from fastapi import FastAPI, Path
from src.getData import get_files, downloadReport
from src import uploadData
from src import archiveData
from src.getHDFSFiles import get_hdfs_file_status
from src.uploadToHDFS import upload_to_hdfs
from src import downloadFromHDFS
import os
from fastapi import File, UploadFile
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import asyncio
from concurrent.futures import ThreadPoolExecutor
import shutil

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


rawDataPath = os.getenv("rawDataPath", default="/raw")
reportDataPath = os.getenv("rawDataPath", default="/report")
archiveDataPath = os.getenv("archiveDataPath", default="/archive")
VALID_REPORT_NAME_REGEX = r"^[a-zA-Z0-9_\-\.]+$"
executor = ThreadPoolExecutor()

@app.get("/")
async def root():
    return {"message": "GenomicInsights Storage Microservice"}

@app.get("/getData")
async def getDataHandler():
    return get_files(rawDataPath)


@app.get("/getHDFSFiles/{dir:path}")
async def getHDFSFiles(dir: str):
    return get_hdfs_file_status(dir)

@app.get("/downloadFromHDFS/{dir:path}")
async def downloadDataFromHDFS(dir: str):
    return downloadFromHDFS.download_from_hdfs(dir)

@app.post("/upload/")
async def upload(file: List[UploadFile] = File(...)):
    return uploadData.upload(rawDataPath, file)

@app.get("/downloadReportURL/{report}")
async def downloadReportURL(report: str):
    return downloadReport(reportDataPath + "/" + report)

@app.post("/archive/{run_id}")
async def archive_data(run_id: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, archiveData, run_id)
    return {"message": "Data archived successfully."}

@app.get("/downloadFileFromHDFS/{file_path:path}")
def download_from_hdfs(file_path: str):
    return downloadFromHDFS.return_file_from_hdfs(file_path)


directories_to_watch = ['/input', '/report', '/results', '/archive']
HDFS_BASE = "/microbiome-data"
upload_lock = threading.Lock()

class NewDirectoryHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            dir_name = os.path.basename(event.src_path)
            print(f"New directory detected: {dir_name}")
            if event.src_path.startswith('/archive'):
                hdfs_path = os.path.join(HDFS_BASE, dir_name)
                time.sleep(3)
                upload_to_hdfs(event.src_path, hdfs_path)
                time.sleep(3)
                downloadFromHDFS.download_from_hdfs(hdfs_path)
                time.sleep(3)
                archiveData.archiveData(dir_name)                
            else:
                hdfs_path = os.path.join(HDFS_BASE, dir_name)
                time.sleep(2)
                with upload_lock:
                    upload_to_hdfs(event.src_path, hdfs_path)

def start_watcher():
    observer = Observer()
    for directory in directories_to_watch:
        observer.schedule(NewDirectoryHandler(), path=directory, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

@app.on_event("startup")
def on_startup():
    watcher_thread = threading.Thread(target=start_watcher, daemon=True)
    watcher_thread.start()

@app.post("/mock-workflow/{workflow_name}")
async def mock_workflow(workflow_name: str):
    mock_report = '/mock-report'
    mock_results = '/mock-results'
    results_dir = f'/results/'
    report_dir = f'/report/'

    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)

    def copy_files(src_dir, dest_dir):
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                src_file = os.path.join(root, file)
                relative_path = os.path.relpath(src_file, src_dir)
                dest_file = os.path.join(dest_dir, relative_path)
                
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)

                shutil.copy(src_file, dest_file)

    try:
        copy_files(mock_report, report_dir)
        copy_files(mock_results, results_dir)

        return {"status": "success", "message": f"Mock workflow {workflow_name} completed."}
    except Exception as e:
        return {"error": f"An error occurred while processing the workflow: {str(e)}"}