from flask import Flask, render_template_string, request, redirect
import views
import sqlite3


app = Flask(__name__)

# Configurando a pasta de arquivos estáticos
app.static_folder = 'static'

@app.route('/')
def index():

    return render_template_string(views.index())

@app.route('/submit', methods=['POST'])
def submit_form():
    titulo = request.form.get('titulo')  # Obtém o valor do campo 'titulo'
    detalhes = request.form.get('detalhes')  # Obtém o valor do campo 'detalhes'

    views.submit(titulo, detalhes)
    return redirect('/')

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute(f"DELETE FROM note WHERE id={id}")

    conexao.commit()
    cursor.close()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET'])
def edit(id):
    page = views.edit(id)
    if page is None:
        return redirect('/')

    return render_template_string(page)

@app.route('/update', methods=['POST'])
def update():
    id = request.form.get('id', type=int)
    titulo = request.form.get('titulo')
    detalhes = request.form.get('detalhes')

    views.update(id, titulo, detalhes)
    return redirect('/')


    


if __name__ == '__main__':
    app.run(debug=True)

