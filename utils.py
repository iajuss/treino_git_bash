import json

def load_data(filename):

    path = "static/data/" + filename

    with open(path, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return dados

def load_template(filename):
    path = 'static/templates/' + filename

    with open(path, 'r', encoding='utf-8') as arquivo:
        template = arquivo.read()

    return template

def adicionar_anotacao(anotacao):
    try:
        with open("static/data/notes.json", "r", encoding="utf-8") as arquivo:
            notes = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        notes = []

    notes.append(anotacao)

    with open("static/data/notes.json", "w", encoding="utf-8") as arquivo:
        json.dump(notes, arquivo, ensure_ascii=False, indent=4)