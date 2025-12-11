from django.contrib import admin

# Register your models here.

from . models import Blogpost

class Blogpostadmin(admin.ModelAdmin):
    list_display=(
        'post_id',
        'title',
        'pub_date',
    )
    list_filter=()
    search_fields=('title','post_id')
admin.site.register(Blogpost,Blogpostadmin)