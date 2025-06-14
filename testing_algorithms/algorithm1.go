package main

import (
	"fmt"
	"errors"
)

type Persona struct {
	nombre string
	edad int
	activo bool
}

func obtenerEdad() int {
	return 30
}

func dividir(a, b int) (int, error) {
	if b == 0 {
		return 0, errors.New("división por cero")
	}
	return a / b, nil
}

func main() {

	// Comentario de una línea
	/*
	Comentario de múltiples líneas
	Este programa evalúa varias estructuras de Go.
	*/

	var nombre string = "Carlos"
	var edad int = obtenerEdad()
	var saldo float64 = 150.75
	var activo bool = true
	var numeros []int = []int{10, 20, 30}
	mapa := map[string]int{"uno": 1, "dos": 2}
	persona := Persona{nombre: nombre, edad: edad, activo: activo}

	fmt.Println("Nombre:", persona.nombre)
	fmt.Println("Edad:", persona.edad)
	fmt.Println("Saldo:", saldo)

	if persona.edad > 18 && persona.activo {
		fmt.Println("Persona activa y mayor de edad.")
	} else {
		fmt.Println("No cumple los criterios.")
	}

	for i := 0; i < len(numeros); i++ {
		fmt.Printf("Número %d: %d\n", i, numeros[i])
		if i == 1 {
			continue
		}
		if i == 2 {
			break
		}
	}

	resultado, err := dividir(10, 2)

	if err != nil {
		fmt.Println("Error:", err)
	} else {
		fmt.Println("Resultado división:", resultado)
	}

	switch persona.nombre {
		case "Carlos":
			fmt.Println("Hola Carlos")
		case "Ana":
			fmt.Println("Hola Ana")
		default:
			fmt.Println("Hola desconocido")
	}

}