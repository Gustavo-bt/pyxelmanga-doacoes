
from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DOACOES_FILE = 'data/doacoes.json'
SENHA_ADMIN = 'pyxelsecreto'

def carregar_doacoes():
    if os.path.exists(DOACOES_FILE):
        with open(DOACOES_FILE, 'r') as f:
            return json.load(f)
    return []

def salvar_doacoes(doacoes):
    with open(DOACOES_FILE, 'w') as f:
        json.dump(doacoes, f, indent=2)

@app.route('/')
def index():
    doacoes = carregar_doacoes()
    doacoes_aprovadas = [d for d in doacoes if d['status'] == 'aprovado']
    total = sum([float(d['valor']) for d in doacoes_aprovadas])
    return render_template('index.html', doacoes=doacoes_aprovadas, total=total)

@app.route('/doar', methods=['POST'])
def doar():
    nome = request.form.get('nome') or "Anônimo"
    valor = request.form.get('valor') or "0.00"
    comprovante = request.form.get('comprovante') or "Nenhum"

    doacoes = carregar_doacoes()
    doacoes.append({
        "nome": nome,
        "valor": valor,
        "comprovante": comprovante,
        "status": "pendente"
    })
    salvar_doacoes(doacoes)
    return redirect('/')

@app.route('/painel', methods=['GET', 'POST'])
def painel():
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == SENHA_ADMIN:
            doacoes = carregar_doacoes()
            return render_template('painel.html', doacoes=doacoes)
        return "Senha incorreta"
    return render_template('painel.html', doacoes=None)

@app.route('/aprovar/<int:index>')
def aprovar(index):
    doacoes = carregar_doacoes()
    if 0 <= index < len(doacoes):
        doacoes[index]['status'] = 'aprovado'
        salvar_doacoes(doacoes)
    return redirect('/painel')

@app.route('/rejeitar/<int:index>')
def rejeitar(index):
    doacoes = carregar_doacoes()
    if 0 <= index < len(doacoes):
        doacoes[index]['status'] = 'rejeitado'
        salvar_doacoes(doacoes)
    return redirect('/painel')

if __name__ == '__main__':
    app.run(debug=True)
