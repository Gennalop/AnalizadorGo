package main

import "fmt"

// Producto representa un artículo en la tienda
type Producto struct {
	nombre  string
	precio  float64
	enStock bool
}

func main() {
	// Comentario: Lista de productos
	productos := []Producto{
		{"Camisa", 25.5, true},
		{"Pantalón", 40.0, false},
		{"Zapatos", 60.75, true}
	}

	// Mapa con stock por producto
	stock := map[string]int{
		"Camisa":   10,
		"Pantalón": 0,
		"Zapatos":  5
	}

	if producto.enStock && producto.precio < 50 {
		precioFinal := aplicarDescuento(producto, 10.0)
		fmt.Println("Producto disponible:", producto.nombre)
		fmt.Println("Precio con descuento:", precioFinal)
		fmt.Println("Stock:", stock[producto.nombre])
	}

	// Operaciones matemáticas
	subtotal := 10 + 5*2 - 3/1
	var iva float64 = 12.0
	total := float64(subtotal) * (1 + iva/100)

	fmt.Println("Total con IVA:", total)

	// Variables y expresiones booleanas
	var usuario string = "cliente_01"
	var edad int = 30
	activo := true

	if edad >= 18 && activo {
		fmt.Println("Usuario autorizado:", usuario)
	} else {
		fmt.Println("Acceso restringido")
	}
}
