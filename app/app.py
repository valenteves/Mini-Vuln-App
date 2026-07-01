from flask import Flask, render_template

app = Flask(__name__)

usuarios = [
    {"id":1, "nombre":"Juan"},
    {"id":2, "nombre":"Pedro"},
    {"id":3, "nombre":"José"},
    {"id":4, "nombre":"Ana"},
    {"id":100, "nombre":"Admin"}
]

lista_ventas = [
    {"idUsuario": 1, "usuarioVendedor": "Juan","usuarioComprador":"Pedro", "producto": "Notebook", "precio":750000, "fecha":"10/03/2026"},
    {"idUsuario": 1, "usuarioVendedor": "Juan","usuarioComprador":"Ana", "producto": "Mouse", "precio":25000,"fecha":"25/06/2026"},
    {"idUsuario": 2, "usuarioVendedor": "Pedro","usuarioComprador":"Ana", "producto": "Celular","precio":550000,"fecha":"13/04/2026"},
    {"idUsuario": 2, "usuarioVendedor": "Pedro","usuarioComprador":"José", "producto": "Monitor","precio":200000,"fecha":"29/06/2026"},
    {"idUsuario": 4, "usuarioVendedor": "Ana","usuarioComprador":"Pedro", "producto": "Teclado","precio":30000, "fecha":"31/05/2026"},
    {"idUsuario": 100, "usuarioVendedor": "Admin", "producto": "flag{me_descubriste}"},
]

usuario_actual=usuarios[0]

@app.route("/")
def inicio():
    return render_template("index.html",usuario=usuario_actual)

@app.route("/ventas/<int:id>")
def ventas(id):
    ventas_usuario=[]
    for venta in lista_ventas:
        if venta["idUsuario"] == id:
            ventas_usuario.append(venta)
    return render_template("ventas.html",ventas=ventas_usuario, usuario=usuario_actual)

@app.route("/iniciar_sesion")
def iniciar_sesion():
    return render_template("iniciar_sesion.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)