const esperar = 3500,random = 1000,extra = 2000,pregunta = 2000,resultado = 2000,cantidad = 5,sprite_inicial = 0;

let c = document.getElementById("app");
let ctx = c.getContext("2d");
let elemento = [
  document.getElementById("fondo0"),
  document.getElementById("fondo1"),
  document.getElementById("fondo2"),
  document.getElementById("fondo3"),
  document.getElementById("fondo4")
];


let cuadro = document.getElementById("pregunta");
let mal = document.getElementById("mal");
let bien = document.getElementById("bien");
let i = sprite_inicial,
  max = cantidad - 1;
let spins,
  tiempo_frame,
  tiempo_anterior,
  tiempo_anterior_e,
  tiempo_anterior_ex,
  tiempo_anterior_pr,
  tiempo_anterior_rs;
let tiempo_espera,
  tiempo_espera_extra,
  tiempo_espera_pregunta,
  tiempo_espera_resultado;
let w = 0,
  h = 0;

let rodar = true,
  preguntar = false,
  corregir = false,
  correcta = true;

function tiempo_aleatorio() {
  tiempo_espera = esperar + Math.random() * random;
  tiempo_espera_extra = extra + tiempo_espera;
  tiempo_espera_pregunta = pregunta + tiempo_espera_extra;
  tiempo_espera_resultado = resultado + tiempo_espera_pregunta;
  tiempo_frame = 0;
  spins = 0;
}

function start() {
  tiempo_aleatorio();
  requestAnimationFrame(loop);
}

function siguiente_sprite() {
  if (i < max) {
    i = i + 1;
  } else {
    i = 0;
  }
}

function actualizar_elemento(tiempo) {
  if (!tiempo_anterior) {
    tiempo_anterior = tiempo;
    tiempo_anterior_e = tiempo;
    tiempo_anterior_ex = tiempo;
    tiempo_anterior_pr = tiempo;
    tiempo_anterior_rs = tiempo;
  }
  if (rodar) {
    if (tiempo - tiempo_anterior > tiempo_frame) {
      siguiente_sprite();
      spins +=1;
      tiempo_anterior = tiempo;
      tiempo_frame = spins * spins;
    }
    if (tiempo - tiempo_anterior_e > tiempo_espera) {
      rodar = false;
    }
  } else {
    if (!preguntar) {
      if (tiempo - tiempo_anterior_ex > tiempo_espera_extra) {
        preguntar = true;
      }
    } else {
      if (!corregir) {
        if (tiempo - tiempo_anterior_pr > tiempo_espera_pregunta) {
          corregir = true;
        }
      } else {
        if (tiempo - tiempo_anterior_rs > tiempo_espera_resultado) {
          tiempo_anterior = tiempo;
          tiempo_anterior_e = tiempo;
          tiempo_anterior_ex = tiempo;
          tiempo_anterior_pr = tiempo;
          tiempo_anterior_rs = tiempo;
          tiempo_aleatorio();
          rodar = true;
          preguntar = false;
          corregir = false;
        }
      }
    }
  }
}

function borrar() {
  ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
}

function restablecer_escalado() {
  var widthToHeight = 16 / 9;
  var newWidth = window.innerWidth;
  var newHeight = window.innerHeight;
  var newWidthToHeight = newWidth / newHeight;

  if (newWidthToHeight < widthToHeight) {
    newWidth = newHeight * widthToHeight;
  } else {
    newHeight = newWidth / widthToHeight;
  }
  w = newWidth;
  h = newHeight;
  c.width = newWidth;
  c.height = newHeight;
}

function dibujar(e) {
  ctx.drawImage(e, 0, 0, w, h);
}

function loop(tiempo) {
  actualizar_elemento(tiempo);
  borrar();
  restablecer_escalado();
  dibujar(elemento[i]);
  if (preguntar) {
    if (!corregir) {
      dibujar(cuadro);
    } else {
      if (correcta) {
        dibujar(bien);
      } else {
        dibujar(mal);
      }
    }
  }
  requestAnimationFrame(loop);
}
start();
