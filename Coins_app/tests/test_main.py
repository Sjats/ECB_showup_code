import unittest
from unittest.mock import patch
import tkinter as tk
from tkinter import ttk
from app.main import APP


class TestAPP(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = APP(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_initialization(self):
        # Check if the APP class initializes correctly
        self.assertIsInstance(self.app, APP)

    def test_menu_seleccio(self):
        # Check if the menu is set up correctly
        label = self.root.children['!frame'].children['!label']
        self.assertEqual(label.cget('text'), "Què vols fer?")

        buttons = [widget for widget in
                   self.root.children['!frame'].winfo_children()
                   if isinstance(widget, ttk.Button)]

        self.assertEqual(len(buttons), 2)
        self.assertEqual(buttons[0].cget('text'), "Visualitzar la colecció")
        self.assertEqual(buttons[1].cget('text'), "Afegir Moneda")

    @patch('app.MostraMonedesApp')
    def test_mostrar_widgets_vis(self, mock_MostraMonedesApp):
        self.app.mostrar_widgets('vis')
        mock_MostraMonedesApp.assert_called_once_with(self.root,
                                                      self.app.frame,
                                                      self.app.menu_seleccio)

    @patch('app.Afegir_contingut')
    def test_mostrar_widgets_afg(self, mock_Afegir_contingut):
        self.app.mostrar_widgets('afg')
        mock_Afegir_contingut.assert_called_once_with(self.root,
                                                      self.app.frame,
                                                      self.app.menu_seleccio)

    def test_ocultar_widgets(self):
        # Add widgets to the frame
        ttk.Label(self.app.frame, text="Test Label").grid(row=0, column=0)
        self.assertEqual(len(self.app.frame.winfo_children()), 4)

        # Call ocultar_widgets and check if widgets are removed
        self.app.ocultar_widgets()
        self.assertEqual(len(self.app.frame.winfo_children()), 0)


if __name__ == "__main__":
    unittest.main()
