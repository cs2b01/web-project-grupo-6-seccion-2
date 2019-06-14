$.getJSON("/current", function(data){
         if(data==null){
          window.location.href="http://127.0.0.1:8080/static/dologin.html"
         }
             });

function Settings(){
                window.location.href="http://127.0.0.1:8080/static/settings.html"
    }
function Rankings(){
                window.location.href="http://127.0.0.1:8080/static/rankings.html"
    }
function Subir_contenido(){
                window.location.href="http://127.0.0.1:8080/static/subir_contenido.html"
    }
function Jugar(){
                window.location.href="http://127.0.0.1:8080/static/jugar.html"
    }
