var uploads="Felicidades. Has subido ";
function Actual() {
    $.getJSON("/current", function (data) {
        if (data == null) {
            window.location.href = "http://127.0.0.1:8080/static/dologin.html"
        }
        else {
            var x= data['uploads']+1;
            uploads = uploads + x + " preguntas. Sigue colaborando para obtener más puntos!";
            $('#h1').html(uploads)}
    });
}

function Subir_contenido(){
                window.location.href="http://127.0.0.1:8080/static/subir_contenido.html"
    }
function Menu(){
                window.location.href="http://127.0.0.1:8080/static/main_menu.html"
    }
