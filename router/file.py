from fastapi import APIRouter, File, UploadFile
import shutil
from fastapi.responses import FileResponse

router = APIRouter(
    prefix='/file',
    tags=['file']
)

@router.post('/file')
def get_file(file: bytes = File(...)):
    content = file.decode('utf-8')
    lines = content.split('\n')
    return {'lines': lines}


@router.post('/uploadfile')
def get_uploadfile(file_to_upload: UploadFile = File(...)):
    path = f"data/{file_to_upload.filename}"
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(file_to_upload.file, buffer)

    return {
        'file_name': path,
        'type': file_to_upload.content_type
    }


@router.get('/download/{name}', response_class=FileResponse)
def get_file(name: str):
    path = f'data/{name}'
    return path