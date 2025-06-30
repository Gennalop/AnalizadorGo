// Correctos
var suma int = 5 + 3
var texto string = "Hola" + " Mundo"
var esMayor bool = edad > 18
var esIgual bool = nombre == "Carlos"
var esVerdad bool = activo && true
var letraMas int = letra + 1      // rune + number (depende si aceptas rune como number, sino error)

// Incorrectos
var errorSuma = "5" + 3          // Error: string + int no permitido
var errorBool = true + 1         // Error: bool + number no permitido
var errorComparacion = "hola" > 3  // Error: string > number no permitido
var errorLogico = 1 && true      // Error: number && bool no permitido
