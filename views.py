from utils import (
    adicionar_anotacao,
    alternar_favorito,
    atualizar_anotacao,
    buscar_anotacao,
    load_data,
    load_template,
)

def index():
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(
            title=dados['titulo'],
            details=dados['detalhes'],
            id=dados['id'],
            favorite_icon='★' if dados['favorite'] else '☆',
        )
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)
    

    return load_template('index.html').format(notes=notes)

def submit(titulo, detalhes):
    params = {
        "titulo": titulo,
        "detalhes": detalhes,
    }

    adicionar_anotacao(params)

def edit(id):
    note = buscar_anotacao(id)
    if note is None:
        return None

    return load_template('edit.html').format(
        id=note['id'],
        title=note['titulo'],
        details=note['detalhes'],
    )

def update(id, titulo, detalhes):
    atualizar_anotacao(id, titulo, detalhes)

def favorite(id):
    alternar_favorito(id)
