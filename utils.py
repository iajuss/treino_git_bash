import sqlite3

def load_data():
    criar_tabela()

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT title, content, id FROM note")
    notes = cursor.fetchall()

    conexao.close()

    return [
        {"titulo": title, "detalhes": content, "id":id}
        for title, content, id in notes
    ]

def load_template(filename):
    path = 'static/templates/' + filename

    with open(path, 'r', encoding='utf-8') as arquivo:
        template = arquivo.read()

    return template

def adicionar_anotacao(anotacao):
    criar_tabela()

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO note (title, content) VALUES (?, ?)",
        (anotacao["titulo"], anotacao["detalhes"])
    )

    conexao.commit()
    conexao.close()

def buscar_anotacao(id):
    criar_tabela()

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT id, title, content FROM note WHERE id = ?", (id,))
    note = cursor.fetchone()

    conexao.close()

    if note is None:
        return None

    id, title, content = note
    return {"id": id, "titulo": title, "detalhes": content}

def atualizar_anotacao(id, titulo, detalhes):
    criar_tabela()

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE note SET title = ?, content = ? WHERE id = ?",
        (titulo, detalhes, id)
    )

    conexao.commit()
    conexao.close()

def criar_tabela():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS note (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
""")
    conexao.commit()
    conexao.close()


