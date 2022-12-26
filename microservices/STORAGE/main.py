from fastapi import FastAPI
from src import getData
from src import uploadData
import os
from fastapi import File, UploadFile
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


rawDataPath = os.getenv("rawDataPath", default="/raw")
reportDataPath = os.getenv("rawDataPath", default="/report")


@app.get("/")
async def root():
    return {"message": "GenomicInsights Storage Microservice"}


@app.get("/getData")
async def root():
    return getData.get_files(rawDataPath)


@app.post("/upload/")
async def uploadFile(file: List[UploadFile] = File(...)):
    return uploadData.upload(rawDataPath, file)


@app.get("/downloadReportURL/{report}")
async def downloadReportURL(report: str):
    return getData.downloadReport(reportDataPath + "/" + report)