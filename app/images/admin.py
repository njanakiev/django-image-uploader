from django.contrib import admin
from .models import Image
from django.contrib.auth import get_user_model


class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at', 'image']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if self.obj:
            kwargs["initial"] = self.obj.author_id
            kwargs["queryset"] = get_user_model().objects.filter(id=self.obj.author_id)
        else:
            kwargs["initial"] = request.user.id
            kwargs["queryset"] = get_user_model().objects.filter(id=request.user.id)
        kwargs["disabled"] = True
        return super(ImageAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def get_form(self, request, obj=None, **kwargs):
        self.obj = obj
        return super(ImageAdmin, self).get_form(request, obj, **kwargs)

# Register your models here.
admin.site.register(Image, ImageAdmin)
