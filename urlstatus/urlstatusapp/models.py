from django.db import models

# Create your models here.

class URL_Model(models.Model):
    '''
    captured book reading details
    '''
    url = models.TextField(verbose_name=u'URL',max_length=255, null=False, blank=False)
    url_status_code = models.IntegerField(verbose_name=u'URL STATUS CODE',max_length=15, null=True, blank=False)
    class Meta:
        verbose_name_plural = 'URL_Status'
        verbose_name = 'URL_Status'
        db_table = 'url_status_table'

    def __unicode__(self):
        return "{}".format(self.id)