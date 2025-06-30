// Correctos
var nombre string = "Carlos"
var edad int = 30
activo := true
var letra rune = 'a'
var precio float64 = 10.5

edad = 35               // reasignación válida
activo = false          // reasignación válida

// Incorrectos
var error1 bool = "true"        // Error: string no asignable a bool
var error2 int = 3.14           // Error: float no asignable a int
nombre = 123                    // Error: int no asignable a string
letra = "b"                    // Error: string no asignable a rune