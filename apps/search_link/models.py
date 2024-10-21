from django.db import models
import uuid

class ExcelFile(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    file = models.FileField(upload_to='excel_files/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.token)