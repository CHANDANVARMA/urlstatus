import smtplib,email,email.encoders,email.mime.text,email.mime.base
from django.shortcuts import render
from xlrd import open_workbook
from views import get_status_code


#provide the GUI of to enter an email id
def mail(request):
    template_name="urlstatusapp/mail.html"
    context={}
    if request.method=="POST":
        mail_id=request.POST['Email']
        url_xls_read()
        send_mail(mail_id)
    return render(request,template_name,context)

#url_xls_read function for to read the given url in url_list.xls and pass the data into get_status_code
#to get the status code.
def url_xls_read():
    workbook=open_workbook('urlstatus/filestorage/upload_root/url_list.xls',on_demand=True)
    worksheet = workbook.sheet_by_index(0)
    variant_name_dict={}
    num_rows = worksheet.nrows-1
    num_col=worksheet.ncols
    for i in range(num_rows):
        for j in range(num_col):
            variant_name_dict[worksheet.cell(0,j).value]=worksheet.cell(i+1,j).value
            variant_string=''.join(variant_name_dict.values())
            get_status_code(variant_string)


#send_mail function provide a functionality to send a mail with attach status_code.xls which is contain the status code of given urls.
def send_mail(mail_id):
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
    fileMsg.add_header('Content-Disposition','attachment;filename=Output.xls')
    emailMsg.attach(fileMsg)
    # send email
    server = smtplib.SMTP('smtp.gmail.com')
    server.starttls()
    server.login('testmaddy123@gmail.com','testmaddy@123')
    server.sendmail(fromAddr,to,emailMsg.as_string())
    server.quit()