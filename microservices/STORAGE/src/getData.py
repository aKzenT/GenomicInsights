import os
from fastapi.responses import FileResponse


def get_files(rawDataPath):
    rawFilesList = []
    rawFiles = os.listdir(rawDataPath)
    for rawFile in rawFiles:
        rawFilesList.append(rawFile)
    return {'files': rawFilesList}


def downloadReport(reportDataPath):
    path = reportDataPath.split('/')
    file = path[len(path) - 1]

    return FileResponse(path=reportDataPath, filename=file, media_type='application/pdf')
