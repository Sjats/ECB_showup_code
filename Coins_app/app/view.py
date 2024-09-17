import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
import os


class MostraMonedesApp:

    def __init__(self, master, frame, final):

        self.master = master
        self.master.title("Mirar la colecció de Monedes")
        self.frame = frame
        self.final = final
        self.opcio_seleccionada = tk.StringVar()
        self.path = os.getcwd()

        self.menu_seleccio()

    def scrollable_frame_fun(self):
        # Create a container for the scrollable section
        container = ttk.Frame(self.frame)
        container.grid(row=0, column=0, sticky='nsew')

        # Configure grid weights for the container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=0)
        container.grid_rowconfigure(1, weight=0)

        # Create a canvas
        self.canvas = tk.Canvas(container, height=800, width=950)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Add a vertical scrollbar to the canvas
        v_scrollbar = ttk.Scrollbar(container,
                                    orient="vertical",
                                    command=self.canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=v_scrollbar.set)

        # Create a frame inside the canvas to hold the content
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0),
                                  window=self.scrollable_frame,
                                  anchor="nw")

        # Ensure the scrollable region is updated when the size
        # of the content changes
        self.scrollable_frame.bind(
            "<Configure>",
            lambda event: self.update_scrollregion())

    def update_scrollregion(self):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def menu_seleccio(self):
        # Etiqueta per a triar què vol afegir l'usuari
        self.ocultar_widgets()
        tk.Label(self.frame,
                 text="Quines monedes vols consultar?").grid(row=0,
                                                             column=0,
                                                             columnspan=3,
                                                             pady=10)

        # Botons per a cada opció
        button_width = 15  # Adjust width as needed
        button_height = 2  # Adjust height as needed
        button_padding_x = 10  # Adjust horizontal padding as needed
        button_padding_y = (10, 5)  # Adjust vertical padding as needed

        def aux_but(mode, exe, r, c):
            tk.Button(self.frame,
                      text=mode,
                      width=button_width,
                      height=button_height,
                      command=lambda: self.mostrar_widgets(exe)).grid(
                          row=r,
                          column=c,
                          padx=button_padding_x,
                          pady=button_padding_y)
        aux_but("Pesetes", "pesetes", 2, 1)
        aux_but("Croats", "croat", 1, 0)
        aux_but("Colecció Completa", "tot", 3, 0)
        aux_but("Monedes 2002", "2002", 2, 0)
        aux_but("Plata", "plata", 1, 1)

        # Botó per sortir de l'aplicació
        tk.Button(self.frame,
                  text="Enrere",
                  command=self.final).grid(row=5, columnspan=2, pady=10)

    def mostrar_widgets(self, opcio):
        # Oculta tots els widgets abans de mostrar els nous
        self.ocultar_widgets()
        if opcio == 'pesetes':
            self.ensenyar_pesetes()
        elif opcio == 'croat':
            self.ensenyar_croat()
        elif opcio == '2002':
            self.ensenyar_2002()
        elif opcio == 'plata':
            self.ensenyar_plata()
        elif opcio == "tot":
            self.ensenyar_tot()

    def ensenyar_llista(self, llista):
        self.ocultar_widgets()

        self.tree = ttk.Treeview(self.frame,
                                 columns=llista,
                                 show="headings",
                                 height=35)

        for columna in llista:
            self.tree.heading(columna, text=columna)

        self.tree.pack(fill=tk.BOTH, expand=True)

        tk.Button(self.frame,
                  text="Enrere",
                  command=self.menu_seleccio).pack(pady=10)

    def ensenyar_unic_foto(self, i, j, informacio, frame):
        # Calcular la fila correcta basada en la seva posició
        i *= 3

        placeholder_img_path = informacio[-1]
        if informacio[-1] is None:
            placeholder_img_path = self.path + "/imatges/no_trobat.png"
        try:
            img = Image.open(placeholder_img_path)
            # Redimensiona la imatge si és necessari
            img = img.resize((400, 200))
            img_tk = ImageTk.PhotoImage(img)

            # Mostra la imatge en un Label
            example_image = tk.Label(frame, image=img_tk)
            # Manté una referència a la imatge per evitar que sigui eliminada
            example_image.image = img_tk
            example_image.grid(row=i, column=j, padx=10, pady=10)

            informacio_liniea_1 = informacio[0]
            example_info_1 = tk.Label(frame,
                                      text=informacio_liniea_1,
                                      wraplength=400,
                                      anchor="w", justify="left")
            example_info_1.grid(row=i+1, column=j, padx=10, pady=4, sticky="w")

            informacio_liniea_2 = informacio[1]
            example_info_2 = tk.Label(frame, text=informacio_liniea_2,
                                      wraplength=400, anchor="w",
                                      justify="left")
            example_info_2.grid(row=i+2, column=j, padx=10, pady=4, sticky="w")

            informacio_liniea_3 = informacio[2]
            example_info_3 = tk.Label(frame, text=informacio_liniea_3,
                                      wraplength=400, anchor="w",
                                      justify="left")
            example_info_3.grid(row=i+3, column=j, padx=10, pady=4, sticky="w")

        except FileNotFoundError:
            print(f"Error: No s'ha trobat la imatge: {placeholder_img_path}")
        except Exception as e:
            print(f"Error carregant la imatge: {e}")

    def ensenyar_unic_foto_petita(self, i, j, informacio, frame):

        placeholder_img_path = informacio[-1]
        try:
            img = Image.open(placeholder_img_path)
            img = img.resize((50, 50))
            img_tk = ImageTk.PhotoImage(img)

            # Mostra la imatge en un Label
            example_image = tk.Label(frame, image=img_tk)
            example_image.image = img_tk
            example_image.grid(row=i, column=j, padx=10, pady=10)

            informacio_liniea_1 = informacio[0]
            example_info_1 = tk.Label(frame, text=informacio_liniea_1,
                                      wraplength=400, anchor="w",
                                      justify="left")
            example_info_1.grid(row=i+1, column=j, padx=10, pady=4, sticky="w")

        except FileNotFoundError:
            print(f"Error: No s'ha trobat la imatge: {placeholder_img_path}")
        except Exception as e:
            print(f"Error carregant la imatge: {e}")

    def ocultar_widgets(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def ensenyar_pesetes(self):
        self.ensenyar_llista(["Valor Nominal", "Nom Governador",
                              "Any", "Serie d'Emissio",
                              "Estat", "Valor Estimat",
                              "LLoc", "identificant"])
        self.populate_treeview_pesetes()

    def populate_treeview_pesetes(self):
        # Connecta amb la base de dades
        conn = sqlite3.connect(self.path + "/data/bdd_numismatica.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""SELECT m.valor_nominal, s.nom, g.numero,
                           s.ordinal, m.any, p.serie_emissio, p.estat,
                           p.valor_estimat, p.lloc, p.id
                                FROM peça p
                                JOIN moneda m ON p.moneda_id = m.id
                                JOIN devisa d ON m.devisa_id = d.id
                                JOIN govern g ON m.govern_id = g.id
                                JOIN senyor s ON g.senyor_id = s.id
                                WHERE d.id = 3
                                ORDER BY  m.any ASC, p.serie_emissio ASC;
                                """)
            monedes = cursor.fetchall()

            for moneda in monedes:
                label = [moneda[0], moneda[1] + " " + moneda[2] + " " +
                         moneda[3]]
                for i in range(4, len(moneda)):
                    label.append(moneda[i])
                self.tree.insert("", "end", values=label)

        except sqlite3.Error as e:
            print("Error en obtenir les monedes de la base de dades:", e)

        finally:
            # Tanca la connexió
            conn.close()

    def ensenyar_croat(self):
        self.ocultar_widgets()
        self.scrollable_frame_fun()
        self.populate_croats()
        self.update_scrollregion()

    def populate_croats(self):
        conn = sqlite3.connect(self.path + "/data/bdd_numismatica.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""SELECT s.nom, g.data_debut,
                           g.data_final, s.ordinal, t.nom, g.numero,
                                p.estat, p.lloc,
                           p.valor_estimat, p.descripcio, p.foto_path
                                FROM peça p
                                JOIN moneda m ON p.moneda_id = m.id
                                JOIN govern g ON m.govern_id = g.id
                                JOIN senyor s ON g.senyor_id = s.id
                                JOIN titol t ON t.id=g.titol_id
                                JOIN devisa d ON d.id = m.devisa_id
                                WHERE d.id = 1
                                ORDER BY g.data_debut ASC;
                                """)
            monedes = cursor.fetchall()
            for index in range(len(monedes)):
                i = index // 2
                j = index % 2
                moneda = monedes[index]
                informacio = [moneda[0] + " " + moneda[3] + " (" +
                              moneda[1][0:4] + "-" + moneda[2][0:4] + ") "
                              + moneda[5] + moneda[4][3:]]
                informacio.append("Descripció: " + moneda[9] +
                                  ", Conservació: " + moneda[6])
                informacio.append("Localització: " + moneda[7] +
                                  ", Valor actual: " + str(moneda[8]) + " €")

                informacio.append(self.path + "/" + moneda[10])
                self.ensenyar_unic_foto(i, j, informacio,
                                        self.scrollable_frame)

        except sqlite3.Error as e:
            print("Error en obtenir les monedes de la base de dades:", e)

        finally:
            # Tanca la connexió
            conn.close()

        tk.Button(
            self.frame,
            text="Enrere",
            command=self.menu_seleccio).grid(row=len(monedes)*4 + 1,
                                             column=0,
                                             padx=10,
                                             pady=10)

    def ensenyar_2002(self):
        self.ocultar_widgets()
        self.scrollable_frame_fun()
        self.populate_2002()
        self.update_scrollregion()

    def populate_2002(self):
        conn = sqlite3.connect(self.path + "/data/bdd_numismatica.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""SELECT m.valor_nominal, t.territori,
                           p.descripcio, m.foto_path
                                FROM peça p
                                JOIN moneda m ON p.moneda_id = m.id
                                JOIN govern g ON m.govern_id = g.id
                                JOIN senyor s ON g.senyor_id = s.id
                                JOIN titol t ON t.id=g.titol_id
                                JOIN devisa d ON d.id = m.devisa_id
                                WHERE m.any=2002
                                ORDER BY d.id, t.territori,
                           m.valor_nominal DESC;
                                """)
            monedes = cursor.fetchall()
            territori_index = monedes[0][1]
            # Create and place the first territory label
            example_info_3 = tk.Label(self.scrollable_frame,
                                      text=territori_index, wraplength=400,
                                      anchor="w", justify="left",
                                      font=("Arial", 16, "bold"))
            example_info_3.grid(row=0, column=0, padx=10, pady=4, sticky="w")

            col = 0
            lin = 0
            for moneda in monedes:
                col = col % 4
                if col == 0:
                    lin += 3

                # Check if the territory has changed
                if moneda[1] != territori_index:
                    territori_index = moneda[1]
                    # Create and place a new territory label
                    example_info_3 = tk.Label(self.scrollable_frame,
                                              text=territori_index,
                                              wraplength=400, anchor="w",
                                              justify="left",
                                              font=("Arial", 16, "bold"))
                    example_info_3.grid(row=lin + 2, column=0, padx=10,
                                        pady=4, sticky="w")
                    lin += 3
                    col = 0

                # Prepare the coin information
                if moneda[2] != "":
                    informacio = [str(moneda[0]) + " €, " + moneda[2]]
                else:
                    informacio = [str(moneda[0]) + " €"]

                if moneda[3] != "":
                    informacio.append(self.path + "/" + moneda[3])
                else:
                    informacio.append(self.path + "/imatges/no_trobat.png")

                # Display the coin information
                self.ensenyar_unic_foto_petita(lin, col + 1, informacio,
                                               self.scrollable_frame)
                col += 1

        except sqlite3.Error as e:
            print("Error en obtenir les monedes de la base de dades:", e)

        finally:
            # Tanca la connexió
            conn.close()
        tk.Button(self.frame,
                  text="Enrere",
                  command=self.menu_seleccio).grid(row=lin + 2,
                                                   column=0,
                                                   padx=10,
                                                   pady=10)

    def ensenyar_plata(self):
        self.ocultar_widgets()
        self.scrollable_frame_fun()
        self.populate_plata()
        self.update_scrollregion()

    def populate_plata(self):
        conn = sqlite3.connect(self.path + "/data/bdd_numismatica.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""SELECT s.nom, g.data_debut,
                           g.data_final, s.ordinal, t.nom, g.numero,
                                p.estat, p.lloc, p.valor_estimat,
                           p.descripcio, p.foto_path
                                FROM peça p
                                JOIN moneda m ON p.moneda_id = m.id
                                JOIN govern g ON m.govern_id = g.id
                                JOIN senyor s ON g.senyor_id = s.id
                                JOIN titol t ON t.id=g.titol_id
                                JOIN devisa d ON d.id = m.devisa_id
                                WHERE m.material = "Plata"
                                ORDER BY g.data_debut ASC;
                                """)
            monedes = cursor.fetchall()
            for index in range(len(monedes)):
                i = index // 2
                j = index % 2
                moneda = monedes[index]
                informacio = [moneda[0] + " " + moneda[3] +
                              " (" + moneda[1][0:4] + "-" + moneda[2][0:4]
                              + ") " + moneda[5] + moneda[4][3:]]

                informacio.append("Descripció: " + moneda[9] +
                                  ", Conservació: " + moneda[6])
                informacio.append("Localització: " + moneda[7] +
                                  ", Valor actual: " + str(moneda[8]) + " €")
                if moneda[10] == "":
                    informacio.append(None)
                else:
                    informacio.append(self.path + "/" + moneda[10])

                self.ensenyar_unic_foto(i, j, informacio,
                                        self.scrollable_frame)

        except sqlite3.Error as e:
            print("Error en obtenir les monedes de la base de dades:", e)

        finally:
            # Tanca la connexió
            conn.close()

        tk.Button(self.frame,
                  text="Enrere",
                  command=self.menu_seleccio).grid(row=len(monedes)*4 + 1,
                                                   column=0, padx=10, pady=10)

    def ensenyar_tot(self):
        self.ensenyar_llista(["Devisa", "Territori", "Valor Nominal",
                              "Nom Governador", "Any",
                              "Serie d'Emissio", "Estat",
                              "Valor Estimat", "LLoc",
                              "identificant"])
        self.populate_treeview_tot()

    def populate_treeview_tot(self):
        # Connecta amb la base de dades
        conn = sqlite3.connect(self.path + "/data/bdd_numismatica.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""SELECT d.nom, t.territori, m.valor_nominal,
                           s.nom, g.numero, s.ordinal, m.any, p.serie_emissio,
                           p.estat, p.valor_estimat, p.lloc, p.id
                                FROM peça p
                                JOIN moneda m ON p.moneda_id = m.id
                                JOIN devisa d ON m.devisa_id = d.id
                                JOIN govern g ON m.govern_id = g.id
                                JOIN senyor s ON g.senyor_id = s.id
                                JOIN titol t ON t.id = g.titol_id
                                ORDER BY  d.id, t.territori, m.any ASC,
                           p.serie_emissio ASC;
                                """)
            monedes = cursor.fetchall()

            for moneda in monedes:
                label = [moneda[0], moneda[1], moneda[2], moneda[3] +
                         " " + moneda[4] + " " + moneda[5]]
                for i in range(6, len(moneda)):
                    label.append(moneda[i])
                self.tree.insert("", "end", values=label)

        except sqlite3.Error as e:
            print("Error en obtenir les monedes de la base de dades:", e)

        finally:
            # Tanca la connexió
            conn.close()


if __name__ == "__main__":
    master = tk.Tk()
    app = MostraMonedesApp(master)
    master.mainloop()
