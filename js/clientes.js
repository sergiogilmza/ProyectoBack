/*Alta de Cliente */
const { createApp } = Vue
createApp({
    data() {
        return {
            clientes: [],
            url: 'http://localhost:5000/clientes',
            error: false,
            cargando: true,
            /*atributos para el guardar los valores del formulario */
            id: 0,
            nomape: "",
            edad: 0,
            dni: 0,
            direccion: "",
            imagen: "",
            sueldo: 0,

        }
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.clientes = data;
                    this.cargando = false
                })
                .catch(err => {
                    console.error(err);
                    this.error = true
                })
        },

        eliminar(clientes) {
            opcion = confirm("Confirma eliminar cliente?");
            if (opcion == true) {
                const url = this.url + '/' + clientes;
                var options = {
                    method: 'DELETE',
                }
                fetch(url, options)
                    .then(res => res.text()) // or res.json()
                    .then(res => {
                        location.reload();
                    })
            }
        },



        grabar() {
            opcion = confirm("Confirma Agregar Cliente?");
            if (opcion == true) {
                let cliente = {
                    nomape: this.nomape,
                    edad: this.edad,
                    dni: this.dni,
                    direccion: this.direccion,
                    sueldo: this.sueldo,
                    imagen: this.imagen
                }

                var options = {
                    body: JSON.stringify(cliente),
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    redirect: 'follow'
                }
                fetch(this.url, options)
                    .then(function() {
                        window.location.href = "./clientes.html";
                    })
                    .catch(err => {
                        console.error(err);
                        alert("Error al Grabar")
                    })
            }
        }
    },


    created() {
        this.fetchData(this.url)
    },
}).mount('#app')