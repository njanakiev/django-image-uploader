from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.urls import reverse


def validate_file_size(obj):
    if obj.size > settings.MAX_FILESIZE:
        return obj
    else:
        return ValidationError("The File is too large")


class Image(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(
        default=timezone.now, editable=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        #blank=True,
        #null=True,
        #storage=SFTPStorage(),
        validators=[
            validate_file_size,
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png']
            )
        ]
    )

    def get_absolute_url(self):
        return reverse('image', kwargs={'pk': self.pk})
