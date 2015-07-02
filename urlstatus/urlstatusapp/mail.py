import smtplib,email,email.encoders,email.mime.text,email.mime.base
from django.shortcuts import render
from xlrd import open_workbook
from views import UrlStatus
from django.views.generic import View

#to provide a facility to enter a email id
class Mail(View):
    def get(self,request):
        template_name="urlstatusapp/mail.html"
        return render(request,template_name)

    def post(self,request):
        template_name="urlstatusapp/mail.html"
        context={}
        if request.method=="POST":
            mail_id=request.POST['Email']
            self.url_xls_read()
            self.send_mail(mail_id)
            message="Mail is successfully sent"
            context={'message':message}
        return render(request,template_name,context)
    #Read the each url in given xls file.
    def url_xls_read(self):
        workbook=open_workbook('urlstatus/filestorage/upload_root/url_list.xls',on_demand=True)
        worksheet = workbook.sheet_by_index(0)
        variant_name_dict={}
        num_rows = worksheet.nrows-1
        num_col=worksheet.ncols
        for i in range(num_rows):
            for j in range(num_col):
                variant_name_dict[worksheet.cell(0,j).value]=worksheet.cell(i+1,j).value
                variant_string=''.join(variant_name_dict.values())
                url=UrlStatus()
                UrlStatus.get_status_code(url,variant_string)


    #To send a mail with attach status_code.xls which is contain the status code of given urls.
    def send_mail(self,mail_id):
        Master_File_UPLOAD_ROOT='urlstatus/filestorage/upload_root/status_code.xls'
        to = [mail_id]
        fromAddr = mail_id
        subject = "Status Report of URLs"
        cc=['testmaddy123@gmail.com']
         # create html email
        html = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '
        html +='"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml">'
        html +='<body style="font-size:12px;font-family:Verdana">Kindly Find the Status Report<p>...</p>'
        html += "</body></html>"
        emailMsg = email.MIMEMultipart.MIMEMultipart('alternative')
        emailMsg['Subject'] = subject
        emailMsg['From'] = fromAddr
        emailMsg['To'] = ', '.join(to)
        emailMsg['Cc'] = ", ".join(cc)
        emailMsg.attach(email.mime.text.MIMEText(html,'html'))

        # now attach the file
        fileMsg = email.mime.base.MIMEBase('application','vnd.ms-excel')
        fileMsg.set_payload(file(Master_File_UPLOAD_ROOT).read())
        email.encoders.encode_base64(fileMsg)
        fileMsg.add_header('Content-Disposition','attachment;filename=status_report.xls')
        emailMsg.attach(fileMsg)
        # send email
        server = smtplib.SMTP('smtp.gmail.com')
        server.starttls()
        server.login('testmaddy123@gmail.com','testmaddy@123')
        server.sendmail(fromAddr,to,emailMsg.as_string())
        server.quit()