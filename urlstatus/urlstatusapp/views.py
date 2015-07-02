import requests
from django.shortcuts import render
from models import URL_Model
from xlwt import Workbook
from django.views.generic import View



# Create your views here.

#provie a GUI to fill the urls
class UrlStatus(View):
    def get(self,request):
        template_name="urlstatusapp/url_status_code.html"
        return render(request,template_name)

    def post(self,request):
        template_name="urlstatusapp/url_status_code.html"
        context={}
        if request.method=="POST":
            url1=request.POST['URL1']
            url2=request.POST['URL2']
            url3=request.POST['URL3']
            url4=request.POST['URL4']
            url5=request.POST['URL5']
            list=[url1,url2,url3,url4,url5]
            for value in list:
                if value is u'':
                    pass
                else:
                    self.get_status_code(value)
                    message="Report is generated with status code"
                    context={'message':message}
        return render(request,template_name,context)

    #To get the status code ex:-200,400 etc
    def get_status_code(self,value):
        try:
            request_url = requests.head(value)
            ms, is_new = URL_Model.objects.get_or_create(url=value,url_status_code=request_url.status_code)
            if is_new:
                ms.save()
            self.status_code_xls()
        except requests.ConnectionError:
            print "This webpage is not available",value

    #to store the urls and status code in xls file
    def status_code_xls(self):
        Master_File_UPLOAD_ROOT='urlstatus/filestorage/upload_root/status_code.xls'
        book = Workbook()
        sheet1=book.add_sheet('URL STATUS CODE DATA')
        data_value=self.fetch_url_status_value()
        data_value_list=[entry for entry in data_value]
        try:
            keys=data_value_list[0].keys()
        except KeyError:
            pass
        col=0
        for key in keys:
            sheet1.write(0, col, key)
            col=col+1
        row=0
        for i in data_value_list:
            col1=0
            row_dict=data_value_list[row]
            for key_value in row_dict:
                sheet1.write(row +1,col1,row_dict[key_value])
                col1=col1+1
            row = row + 1
        book.save(Master_File_UPLOAD_ROOT)

    #fetch the url and url status code in database
    def fetch_url_status_value(self):
        ts=URL_Model.objects.values('url','url_status_code')
        return ts



