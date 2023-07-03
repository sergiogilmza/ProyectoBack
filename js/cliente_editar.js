console.log(location.search) // lee los argumentos pasados a este formulario
var id = location.search.substr(4)
console.log(id)
const { createApp } = Vue
createApp({
    data() {
        return {
            id: 0,
            nomape: "",
            edad: 0,
            dni: 0,
            direccion: "",
            imagen: "",
            sueldo: 0,
            url: 'http://localhost:5000/clientes/' + id,
        }
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    this.id = data.id
                    this.nomape = data.nomape;
                    this.edad = data.edad
                    this.dni = data.dni
                    this.direccion = data.direccion
                    this.sueldo = data.sueldo
                    this.imagen = data.imagen
                })
                .catch(err => {
                    console.error(err);
                    this.error = true
                })
        },
        modificar() {
            opcion = confirm("Confirma modificar datos del cliente?");
            if (opcion == true) {
                let clientes = {
                    nomape: this.nomape,
                    edad: this.edad,
                    dni: this.dni,
                    direccion: this.direccion,
                    sueldo: this.sueldo,
                    imagen: this.imagen
                }
                var options = {
                    body: JSON.stringify(clientes),
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    redirect: 'follow'
                }
                fetch(this.url, options)
                    .then(function() {

                        window.location.href = "./clientes.html";
                    })
                    .catch(err => {
                        console.error(err);
                        alert("Error al Modificar")
                    })
            } else { window.location.href = "./clientes.html"; }
        }
    },
    created() {
        this.fetchData(this.url)
    },
}).mount('#app')