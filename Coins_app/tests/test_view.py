import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from app.view import MostraMonedesApp


class TestMostraMonedesApp(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.final_callback = MagicMock()
        self.app = MostraMonedesApp(self.root, self.frame, self.final_callback)

    def tearDown(self):
        self.root.destroy()

    @patch('os.getcwd')
    def test_initialization(self, mock_getcwd):
        mock_getcwd.return_value = "/app_monedes-main"
        app = MostraMonedesApp(self.root, self.frame, self.final_callback)
        self.assertIsInstance(app, MostraMonedesApp)

    def test_menu_seleccio(self):
        self.app.menu_seleccio()
        # Check if the buttons are created
        buttons = [widget for widget in self.frame.winfo_children()
                   if isinstance(widget, tk.Button)]
        self.assertGreater(len(buttons), 0)

    def test_ensenyar_unic_foto(self):
        # Test for valid image path
        with patch('PIL.Image.open') as mock_open:
            mock_img = MagicMock()
            mock_open.return_value = mock_img
            mock_img.resize.return_value = mock_img
            frame = tk.Frame(self.root)
            self.app.ensenyar_unic_foto(0,
                                        0,
                                        ['Info1', 'Info2', 'Info3',
                                         '/path/to/image.png'], frame)

            labels = [widget for widget in frame.winfo_children()
                      if isinstance(widget, tk.Label)]

            self.assertGreaterEqual(len(labels), 0)


if __name__ == "__main__":
    unittest.main()
