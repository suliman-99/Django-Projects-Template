from django.utils import timezone
from django.conf import settings
from django.core.management import call_command
from django.http.response import HttpResponse
from rest_framework.generics import RetrieveAPIView
from common.permissions import IsSuperuser


class Backup(RetrieveAPIView):
    permission_classes = (IsSuperuser, )
    
    def retrieve(self, request, *args, **kwargs):
        now = str(timezone.now()).replace(' ', 'T').replace(':', '-')[:19]
        filename = f"{settings.BACKUP_FILE_PREFIX}-{now}.sql"
        backup_file_path = f'{settings.DBBACKUP_STORAGE_OPTIONS["location"]}{filename}'

        call_command('dbbackup', output_filename=filename)

        with open(backup_file_path, 'rb') as backup_file:
            backup_content = backup_file.read()

        response = HttpResponse(backup_content, content_type='application/sql')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response
