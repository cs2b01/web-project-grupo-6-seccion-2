var uploads="Felicidades. Has subido ";
$.getJSON("/current", function(data){
         if(data==null){
          window.location.href="http://127.0.0.1:8080/static/dologin.html"
         }
         uploads=uploads+data['uploads']+" preguntas. Sigue colaborando para obtener más puntos!";
         document.getElementById("h1").innerText=uploads;
             });


function Subir_contenido(){
                window.location.href="http://127.0.0.1:8080/static/subir_contenido.html"
    }
function Menu(){
                window.location.href="http://127.0.0.1:8080/static/main_menu.html"
    }
