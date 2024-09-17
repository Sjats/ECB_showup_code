import unittest
import tkinter as tk
from app.add import Afegir_contingut


class TestAfegirContingut(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.final_action = lambda: None  # Dummy final action
        self.app = Afegir_contingut(
            master=self.root, frame=self.frame, final=self.final_action)

    def test_initial_state(self):
        # Ensure the initial widgets are loaded properly
        self.assertTrue(any(widget.cget("text") == "Què vols afegir?"
                            for widget in self.frame.winfo_children()))

        self.assertTrue(any(widget.cget("text") == "Enrere"
                            for widget in self.frame.winfo_children()))

    def test_button_visibility(self):
        # Test if specific buttons are visible
        buttons = [widget for widget in self.frame.winfo_children()
                   if isinstance(widget, tk.Button)]

        button_texts = [button.cget("text") for button in buttons]
        expected_buttons = [
            "Afegir Moneda", "Afegir Títol", "Afegir Senyor",
            "Afegir Govern", "Afegir Dinastia", "Afegir Peça",
            "Afegir Devisa", "Enrere"
        ]
        for text in expected_buttons:
            self.assertIn(text, button_texts)

    def tearDown(self):
        self.root.destroy()


if __name__ == "__main__":
    unittest.main()
