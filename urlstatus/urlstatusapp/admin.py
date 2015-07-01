from django.contrib import admin
from models import URL_Model

# Register your models here.
class URL_Model_Admin(admin.ModelAdmin):
    list_display = ('id','url','url_status_code')
    list_filter = ('url',)
    list_per_page = 2000


admin.site.register(URL_Model, URL_Model_Admin)