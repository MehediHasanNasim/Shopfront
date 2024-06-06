from django.contrib import admin
from .models import * 
# Register your models here.




@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['label']

# admin.site.register(TaggedItem)
# admin.site.register(TaggedItemManager)