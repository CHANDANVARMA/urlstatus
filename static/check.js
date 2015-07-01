
function check()
        {
            if (!MailSend.Email.value)
            {
                alert ("Please Enter a Email ID");
                return (false);
            }
            document.MailSend.submit();
        }


function login(){
    document.Login.submit();
    }