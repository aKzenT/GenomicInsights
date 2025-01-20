from fastapi import FastAPI, Query
from src import getData
from src import uploadData
import os
from fastapi import File, UploadFile
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

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
VALID_REPORT_NAME_REGEX = r"^[a-zA-Z0-9_\-\.]+$"

@app.get("/")
async def root():
    return {"message": "GenomicInsights Storage Microservice"}


@app.get("/getData")
async def getData():
    return getData.get_files(rawDataPath)


@app.post("/upload/")
async def upload(file: List[UploadFile] = File(...)):
    return uploadData.upload(rawDataPath, file)


@app.get("/downloadReportURL/{report}")
async def downloadReportURL(report: Annotated[str, Query(pattern=VALID_REPORT_NAME_REGEX)]):):
    return getData.downloadReport(reportDataPath + "/" + report)
