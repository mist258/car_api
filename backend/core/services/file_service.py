import os
from uuid import uuid1


class FileService:

    @staticmethod
    def upload_file(instance, file: str):
        ext = file.split('.')[-1]
        if ext not in ['png', 'jpg', 'jpeg']:
            return ValueError('File type not supported')

        return os.path.join('uploads', f'{uuid1()}.{ext}')