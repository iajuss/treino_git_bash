from utils import load_data, load_template, adicionar_anotacao

def index():
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados['titulo'], details=dados['detalhes'], id=dados['id'])
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
