from fastapi import File, UploadFile
from typing import List


def upload(rawDataPath, files: List[UploadFile] = File(...)):
    for file in files:
        try:
            contents = file.file.read()
            with open(rawDataPath + '/' + file.filename, 'wb+') as f:
                f.write(contents)

        except Exception as err:

            return {"message": str(err)}
        finally:
            file.file.close()

    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}
