$.getJSON("/current", function(data){
    document.getElementById("username").value = data['username'];
    document.getElementById("name").value = data['name'];
    document.getElementById("lastname").value = data['lastname'];
    document.getElementById("password").value = data['password'];});

function Actualizar(){
            $.ajax({
                url: 'http://127.0.0.1:8080/users',
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify({
                     "username":  $('#username').val(),
                     "name":  $('#name').val(),
                     "lastname":  $('#lastname').val(),
                     "password":  $('#password').val()
                }),
                dataType: 'json',
                success: function(response){
                    $('#success').show();
                },
            error: function(response){
                if(response['status']==401){}
                 else{
                 $('#success').show();
                  }}
            });
        }

function Borracuenta(){
                $.ajax({
                url: 'http://127.0.0.1:8080/users',
                type: 'DELETE',
                success: function(response){
                                    window.location.href="http://127.0.0.1:8080/static/dologin.html"
                },
            error: function(response){
                if(response['status']==401){}
                 else{
                window.location.href="http://127.0.0.1:8080/static/dologin.html"
                  }}
            });

}
