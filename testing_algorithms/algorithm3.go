package main

import "fmt"


type Persona struct {
	nombre string
	edad   int
}

func saludar(p Persona) string {
	if p.edad >= 18 {
		return "Hola " + p.nombre + ", eres mayor de edad."
	}
	return "Hola " + p.nombre + ", eres menor de edad."
}

func main() {
	// Declaración de variables
	var mensaje string
	var contador int = 0
	nombre := ""
	var notas [3]int
	calificaciones := []float64{8.5, 9.2, 7.0}
	puntajes := map[string]int{"Ana": 90, "Luis": 85}

	// Entrada de datos
	fmt.Print("Ingresa tu nombre: ")
	fmt.Scanln(&nombre)

	fmt.Print("Ingresa tu edad: ")
	var edad int
	fmt.Scanln(&edad)

	// Uso de struct
	p := Persona{nombre: nombre, edad: edad}

	// Llamado a función
	mensaje = saludar(p)
	fmt.Println(mensaje)

	// Expresión aritmética
	total := (10 + 5) * 2 / (3 - 1)

	// Expresión booleana y estructura de control
	if total > 10 && edad >= 18 {
		fmt.Println("Total válido y edad suficiente.")
	} else {
		fmt.Println("Condición no cumplida.")
	}

	// Bucle for
	for i := 0; i < 3; i++ {
		notas[i] = i * 10
		fmt.Println("Nota", i, ":", notas[i])
	}

	// Switch
	switch edad {
	case 18:
		fmt.Println("Tienes 18 años.")
	case 21:
		fmt.Println("Tienes 21 años.")
	default:
		fmt.Println("Edad no registrada específicamente.")
	}
}
