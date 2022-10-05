from fastapi import FastAPI, File, UploadFile
from tempfile import NamedTemporaryFile
from doctor.schemas.user import UserDummyBase, UserDummyCreate
import os
import csv


async def read_csv_file(*, contents, schema) -> list:
    data = []
    file_copy = NamedTemporaryFile(delete=False)

    try:
        with file_copy as f:  # The 'with' block ensures that the file closes and data are stored
            f.write(contents)
        
        with open(file_copy.name,'r', encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            for rows in csvReader:
                data.append(schema(**rows))
    finally:
        file_copy.close()  # Remember to close any file instances before removing the temp file
        os.unlink(file_copy.name)  # delete the file
    
    return data
    