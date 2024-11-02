import os
from uuid import uuid1

from django.utils.translation import gettext_lazy as _


class FileService:

    @staticmethod
    def upload_file(instance, file: str):
        ext = file.split('.')[-1]
        if ext not in ['png', 'jpg', 'jpeg']:
            return ValueError(_('File type not supported'))

        return os.path.join('uploads', f'{uuid1()}.{ext}')
