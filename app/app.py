from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_limiter import Limiter
from flask_limiter.errors import RateLimitExceeded
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = "clave-insegura-del-laboratorio"
limiter = Limiter(get_remote_address, app=app)

usuarios = [
    {"id":1, "nombre":"Juan", "usuario":"juan", "password":"123456"},
    {"id":2, "nombre":"Pedro", "usuario":"pedro", "password":"password"},
    {"id":3, "nombre":"José", "usuario":"jose", "password":"qwerty"},
    {"id":4, "nombre":"Ana", "usuario":"ana", "password":"dragon"},
    {"id":5, "nombre":"Gerente", "usuario":"gerente", "password":"football", "flag":"flag{gerente_pwned}"},
    {"id":100, "nombre":"Admin", "usuario":"admin", "password":"admin123"}
]

lista_ventas = [
    {"idUsuario": 1, "usuarioVendedor": "Juan","usuarioComprador":"Pedro", "producto": "Notebook", "precio":750000, "fecha":"10/03/2026"},
    {"idUsuario": 1, "usuarioVendedor": "Juan","usuarioComprador":"Ana", "producto": "Mouse", "precio":25000,"fecha":"25/06/2026"},
    {"idUsuario": 2, "usuarioVendedor": "Pedro","usuarioComprador":"Ana", "producto": "Celular","precio":550000,"fecha":"13/04/2026"},
    {"idUsuario": 2, "usuarioVendedor": "Pedro","usuarioComprador":"José", "producto": "Monitor","precio":200000,"fecha":"29/06/2026"},
    {"idUsuario": 4, "usuarioVendedor": "Ana","usuarioComprador":"Pedro", "producto": "Teclado","precio":30000, "fecha":"31/05/2026"},
    {"idUsuario": 100, "usuarioVendedor": "Admin", "producto": "flag{me_descubriste}"},
]

lista_comentarios = []

def obtener_usuario_actual():
    usuario_id = session.get("usuario_id")
    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            return usuario
    return None

@app.route("/")
def inicio():
    usuario = obtener_usuario_actual()
    if not usuario:
        return redirect(url_for("iniciar_sesion"))
    return render_template("index.html",usuario=usuario)

@app.route("/ventas/<int:id>")
def ventas(id):
    usuario = obtener_usuario_actual()
    if not usuario:
        return redirect(url_for("iniciar_sesion"))

    if id != usuario["id"]:
        flash("No estás autorizado para acceder a las ventas de otro usuario.", "danger")
        return redirect(url_for("ventas", id=usuario["id"]))

    ventas_usuario = []
    for venta in lista_ventas:
        if venta["idUsuario"] == id:
            ventas_usuario.append(venta)

    return render_template("ventas.html", ventas=ventas_usuario, usuario=usuario)

@app.route("/chat", methods=["GET", "POST"])
def comentarios():
    usuario = obtener_usuario_actual()
    if not usuario:
        return redirect(url_for("iniciar_sesion"))
    

    if request.method == "POST":

        lista_comentarios.append({
            "autor": usuario["nombre"],
            "texto": request.form.get("comentario", "")
        })
        
        return redirect(url_for("comentarios"))

    return render_template(
        "comentarios.html",
        comentarios=lista_comentarios,
        usuario=usuario,
    )

@app.route("/iniciar_sesion", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def iniciar_sesion():
    error = None
    usuario_encontrado = None

    if request.method == "POST":
        usuario_form = request.form.get("usuario", "")
        password_form = request.form.get("password", "")

        for usuario in usuarios:
            if usuario["usuario"] == usuario_form and usuario["password"] == password_form:
                usuario_encontrado = usuario
                break

        if usuario_encontrado:
            session["usuario_id"] = usuario_encontrado["id"]
            return redirect(url_for("inicio"))

        error = "Login incorrecto"

    return render_template("iniciar_sesion.html", error=error)

@app.errorhandler(RateLimitExceeded)
def limite_excedido(error):
    return render_template(
        "iniciar_sesion.html",
        error="Login incorrecto. Demasiados intentos fallidos !!!1"
    ), 429

@app.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear()
    return redirect(url_for("iniciar_sesion"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
