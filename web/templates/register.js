function EnviarDatos(){
            $.ajax({
                url: 'http://127.0.0.1:8080/users',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                     "email":  $('#email').val(),
                     "username":  $('#username').val(),
                     "name":  $('#name').val(),
                     "lastname":  $('#lastname').val(),
                           "password":  $('#password').val()
                }),
                dataType: 'json',
                success: function(response){
                window.location.href="http://127.0.0.1:8080/static/dologin.html"
                },
            error: function(response){
                if(response['status']==401){
                    $('#Ocupado').show();
                }
                 else{
                window.location.href="http://127.0.0.1:8080/static/dologin.html"
                  }}
            });
        }
