import time
from datetime import datetime

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "dtime-local-secret"


@app.route("/", methods=["GET", "POST"])
def relogio():
    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "iniciar" and "inicio" not in session:
            session["inicio"] = time.time()
        elif acao == "pausar" and "inicio" in session:
            decorrido = time.time() - session.pop("inicio")
            session["acumulado"] = session.get("acumulado", 0) + decorrido
        elif acao == "zerar":
            session.pop("inicio", None)
            session["acumulado"] = 0

        return redirect(url_for("relogio"))

    acumulado = session.get("acumulado", 0)
    rodando = "inicio" in session
    if rodando:
        acumulado += time.time() - session["inicio"]

    total_segundos = int(acumulado)
    horas, resto = divmod(total_segundos, 3600)
    minutos, segundos = divmod(resto, 60)
    cronometro = f"{horas:02}:{minutos:02}:{segundos:02}"

    return render_template(
        "index.html",
        hora=datetime.now().strftime("%H:%M:%S"),
        cronometro=cronometro,
        rodando=rodando,
    )


if __name__ == "__main__":
    app.run()
