import tkinter as tk
from add import Afegir_contingut
from view import MostraMonedesApp
from tkinter import ttk


class APP:
    def __init__(self, master) -> None:
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)
        self.master.title("Aplicació de Monedes")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.opcio_seleccionada = tk.StringVar()
        self.menu_seleccio()

    def menu_seleccio(self):
        # Etiqueta per a triar què vol afegir l'usuari
        self.ocultar_widgets()
        self.master.title("Aplicació de Monedes")

        ttk.Label(self.frame, text="Què vols fer?").grid(row=0, column=0,
                                                         columnspan=3, pady=10)

        # Botons per a cada opció
        button_width = 15  # Adjust width as needed
        button_height = 2  # Adjust height as needed
        button_padding_x = 10  # Adjust horizontal padding as needed
        button_padding_y = (10, 5)  # Adjust vertical padding as needed

        ttk.Button(self.frame, text="Visualitzar la colecció",
                   command=lambda: self.mostrar_widgets('vis')).grid(
                       row=1,
                       column=0,
                       padx=button_padding_x,
                       pady=button_padding_y,
                       ipadx=button_width,
                       ipady=button_height+7
                  )
        ttk.Button(self.frame,
                   text="Afegir Moneda",
                   command=lambda: self.mostrar_widgets('afg')).grid(
                       row=1, column=1,
                       padx=button_padding_x,
                       pady=button_padding_y,
                       ipadx=button_width+20,
                       ipady=button_height+7)

    def ocultar_widgets(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def mostrar_widgets(self, opcio):
        # Oculta tots els widgets abans de mostrar els nous
        self.ocultar_widgets()

        if opcio == 'vis':
            MostraMonedesApp(self.master, self.frame, self.menu_seleccio)
        elif opcio == 'afg':
            Afegir_contingut(self.master, self.frame, self.menu_seleccio)


if __name__ == "__main__":
    master = tk.Tk()
    app = APP(master)
    master.mainloop()
