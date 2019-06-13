function getData(){
        var email = $('#email').val();
        var password = $('#password').val();
        var message = JSON.stringify({
                "email": email,
                "password": password
            });

        $.ajax({
            url:'/authenticate',
            type:'POST',
            contentType: 'application/json',
            data : message,
            dataType:'json',
            success: function(response){
                },
            error: function(response){
                if(response['status']==401){
                	$('#Incorrecta').show();
                    }
                 else{
                window.location.href="http://127.0.0.1:8080/static/main_menu.html"
                  }}
        });
    }
