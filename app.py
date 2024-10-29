from flask import Flask, render_template
import subprocess

app = Flask(__name__)


@app.route("/")
def home():
    return'<h1 style="color: blueviolet;">Busca de Tarifas</h1> ' \
          '<form action="/run_script" method="get"><button type="submit">Executar Script</button> </form>'


@app.route("/run_script")
def run_script():
    try:
        # Aqui você chama o seu script Python
        result = subprocess.run(["python3", "main.py"], capture_output=True, text=True, check=True)
        return f"Script executado com sucesso! Saída: {result.stdout}"
    except Exception as e:
        return f"Ocorreu um erro: {e}", 500


if __name__ == "__main__":
    app.run(port=5001, debug=True)
