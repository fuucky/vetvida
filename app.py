from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)                                            # Cria uma instância da aplicação Flask

#chave secreta
app.secret_key = 'abacaxi'
#futuramente atualizar para
#app.secret_key = os.getenv('SECRET_KEY')

#Dicionario de usuarios (some quando reinicia)
usuarios = {
    'admin': {
        'senha': '123',
        'email': '123@123.com',
        'nome': 'Administrador Teste'
    }
}


#host local http://127.0.0.1:5000
@app.route('/')                                                  # Pagina principal /
def home():
    return render_template("home.html")

@app.route('/sobre')
def sobre():
    return render_template("sobre.html")
    
@app.route('/servicos')
def servicos():
    return render_template("servicos.html")
    
@app.route('/contato', methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        mensagem = request.form.get("mensagem")
       
        #teste
        print(f"Nova mensagem de {nome} ({email}): {mensagem}")

        flash("Mensagem enviada com sucesso! Entraremos em contato em breve.", "success")
        return redirect(url_for("contato")) #recarrega para mostrar o flash

    return render_template("contato.html")

@app.route('/registro', methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form.get('username')
        senha = request.form.get('senha')
        email = request.form.get('email')
        nome = request.form.get('nome')
    
        if not username or not senha:
            flash('Usuário e senha são obrigatórios!', "error")
            return redirect(url_for('registro'))
        
        if username in usuarios:
            flash('Esse usuário já existe! Escolha outro.')
            return redirect(url_for('registro'))

        #salva o novo usuario
        usuarios[username] = {
            'senha': senha,
            'email': email or '',
            'nome': nome or username
        }    
        flash('Cadastro realizado com sucesso! Agora faça login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == ('POST'):
        username = request.form.get('username')
        senha = request.form.get('senha')

        if username in usuarios and usuarios[username]['senha'] == senha:
            session['logado'] = True
            session['usuario'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos!', 'error')

    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)          # Executa o site em modo de depuração (mostra alguns erros, se houver)

