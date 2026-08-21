import importlib.util
import os
import shutil
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent


class EditNotesTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workdir = Path(self.temp_dir.name)

        for filename in ("servidor.py", "views.py", "utils.py"):
            shutil.copy2(PROJECT_ROOT / filename, self.workdir / filename)
        shutil.copytree(PROJECT_ROOT / "static", self.workdir / "static")

        self.original_cwd = Path.cwd()
        os.chdir(self.workdir)
        sys.path.insert(0, str(self.workdir))
        sys.modules.pop("views", None)
        sys.modules.pop("utils", None)

        spec = importlib.util.spec_from_file_location(
            "test_servidor", self.workdir / "servidor.py"
        )
        self.servidor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.servidor)
        self.client = self.servidor.app.test_client()

        sys.modules["utils"].criar_tabela()
        connection = sqlite3.connect("banco.db")
        connection.execute(
            "INSERT INTO note (title, content) VALUES (?, ?)",
            ("Título original", "Detalhes originais"),
        )
        connection.commit()
        connection.close()

    def tearDown(self):
        os.chdir(self.original_cwd)
        sys.path.remove(str(self.workdir))
        sys.modules.pop("views", None)
        sys.modules.pop("utils", None)
        self.temp_dir.cleanup()

    def test_note_card_has_edit_link(self):
        page = self.client.get("/").get_data(as_text=True)

        self.assertIn('name="edit_button"', page)
        self.assertIn('href="/update/1"', page)

    def test_update_page_displays_the_existing_note(self):
        response = self.client.get("/update/1")

        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn('name="id" value="1"', page)
        self.assertIn('name="titulo" value="Título original"', page)
        self.assertIn('name="detalhes" value="Detalhes originais"', page)
        self.assertIn('<button type="submit">Salvar</button>', page)
        self.assertIn('>Cancelar<', page)
        self.assertIn('name="edit_cancel"', page)

    def test_post_update_persists_changes_and_redirects_home(self):
        response = self.client.post(
            "/update",
            data={"id": "1", "titulo": "Título alterado", "detalhes": "Detalhes alterados"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/")

        connection = sqlite3.connect("banco.db")
        note = connection.execute(
            "SELECT title, content FROM note WHERE id = 1"
        ).fetchone()
        connection.close()
        self.assertEqual(note, ("Título alterado", "Detalhes alterados"))


if __name__ == "__main__":
    unittest.main()
