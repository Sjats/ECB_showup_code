import tkinter as tk
from tkinter import messagebox
import sqlite3
import os


class Afegir_contingut:

    def __init__(self, master, frame, final):
        self.master = master
        self.master.title("Afegir Monedes")

        self.frame = frame
        self.frame.pack(padx=10, pady=10)

        self.opcio_seleccionada = tk.StringVar()
        self.final = final

        self.menu_seleccio()
        self.choice_devisa = tk.StringVar()
        self.choice_govern = tk.StringVar()
        self.choice_senyor_govern = tk.StringVar()
        self.choice_titol_govern = tk.StringVar()
        self.monedes_dict = {}

    def menu_seleccio(self):
        # Etiqueta per a triar què vol afegir l'usuari
        self.ocultar_widgets()
        tk.Label(self.frame, text="Què vols afegir?").grid(
            row=0,
            column=0,
            columnspan=3,
            pady=10)

        # Botons per a cada opció
        button_width = 15  # Adjust width as needed
        button_height = 2  # Adjust height as needed
        button_padding_x = 10  # Adjust horizontal padding as needed
        button_padding_y = (10, 5)  # Adjust vertical padding as needed

        def insert_buton_menu(title, widget_t, r, c):
            tk.Button(self.frame,
                      text=title,
                      width=button_width,
                      height=button_height,
                      command=lambda: self.mostrar_widgets(widget_t)).grid(
                        row=r,
                        column=c,
                        padx=button_padding_x,
                        pady=button_padding_y)

        insert_buton_menu("Afegir Moneda",
                          'moneda',
                          r=3,
                          c=0)
        insert_buton_menu("Afegir Títol", "titol", 1, 1)
        insert_buton_menu("Afegir Senyor", "senyor", 2, 1)
        insert_buton_menu("Afegir Govern", "govern", 2, 0)
        insert_buton_menu("Afegir Dinastia", "dinastia", 1, 0)
        insert_buton_menu("Afegir Peça", "peça", 3, 1)
        insert_buton_menu("Afegir Devisa", "devisa", 4, 0)

        # Botó per sortir de l'aplicació
        tk.Button(self.frame,
                  text="Enrere",
                  command=self.final).grid(row=5,
                                           columnspan=2,
                                           pady=10)

    def mostrar_widgets(self, opcio):
        # Oculta tots els widgets abans de mostrar els nous
        self.ocultar_widgets()

        if opcio == 'moneda':
            self.crear_widgets_moneda()
        elif opcio == 'titol':
            self.crear_widgets_titol()
        elif opcio == 'senyor':
            self.crear_widgets_senyor()
        elif opcio == 'govern':
            self.crear_widgets_govern()
        elif opcio == 'dinastia':
            self.crear_widgets_dinastia()
        elif opcio == 'peça':
            self.crear_widgets_peça()
        elif opcio == "devisa":
            self.crear_widgets_devisa()

    def ocultar_widgets(self):
        for widget in self.frame.winfo_children():
            widget.grid_remove()

    def entry_w(self, title, r, c=0):
        tk.Label(self.frame, text=title).grid(row=r, column=c, sticky=tk.W)
        entry = tk.Entry(self.frame)
        entry.grid(row=r, column=c+1)

        return entry

    def c_entry_w(self, title, r, c=0):
        tk.Label(self.frame, text=title).grid(row=r, column=c, sticky=tk.W)
        choice = tk.StringVar()
        dropdown = tk.OptionMenu(self.frame,
                                 choice,
                                 "")

        dropdown.grid(row=r, column=c+1)
        return choice, dropdown

    def crear_widgets_peça(self):
        # Implementació de widgets per a afegir peces
        tk.Label(self.frame, text="Moneda:").grid(row=0, column=0, sticky=tk.W)

        self.moneda_frame = tk.Frame(self.frame)
        self.moneda_frame.grid(row=0, column=1, sticky=tk.W)

        self.scrollbar_moneda = tk.Scrollbar(self.moneda_frame,
                                             orient=tk.VERTICAL,
                                             width=18)
        self.listbox_moneda = tk.Listbox(
            self.moneda_frame,
            yscrollcommand=self.scrollbar_moneda.set,
            height=8, width=45)

        self.scrollbar_moneda.config(command=self.listbox_moneda.yview)

        self.scrollbar_moneda.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_moneda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Populate the listbox with moneda options from the database
        self.populate_monedes_listbox()
        self.entry_estat = self.entry_w("Estat:", 1)
        self.entry_descripcio_peça = self.entry_w("Descripció:", 2)
        self.entry_serie_emissio = self.entry_w("Sèrie d'Emissió:", 3)
        self.entry_valor_estimat = self.entry_w("Valor Estimat:", 4)
        self.entry_lloc = self.entry_w("Lloc:", 5)
        self.entry_foto_path_peça = self.entry_w("Ruta de la Foto:", 6)

        tk.Button(self.frame, text="Afegir Peça",
                  command=self.afegir_peça).grid(row=7, columnspan=2, pady=10)

        tk.Button(self.frame, text="Enrere",
                  command=self.menu_seleccio).grid(row=8, column=0, pady=10)

    def crear_widgets_senyor(self):
        # Implementació de widgets per a afegir règims
        self.entry_nom_senyor = self.entry_w(title="Nom del Senyor:", r=0, c=0)
        self.entry_data_naixement_senyor = self.entry_w(
            "Data de Naixement:",
            1)
        self.entry_data_mort_senyor = self.entry_w("Data de defunció:", 2)
        self.entry_ordinal_senyor = self.entry_w("Ordinal", 3)

        auxi_din = self.c_entry_w("Dinastia:", 4)
        self.choice_dinastia_senyor, self.dropdown_dinastia_senyor = auxi_din
        self.populate_dinasties_dropdown()

        self.entry_foto_path_senyor = self.entry_w("Ruta Foto:", 5)

        tk.Button(self.frame,
                  text="Afegir Senyor",
                  command=self.afegir_senyor).grid(row=6,
                                                   columnspan=2,
                                                   pady=10)
        tk.Button(self.frame,
                  text="Enrere",
                  command=self.menu_seleccio).grid(row=7,
                                                   column=0,
                                                   pady=10)

    def crear_widgets_dinastia(self):
        # Implementació de widgets per a afegir dinasties
        self.entry_nom_dinastia = self.entry_w("Nom de la Dinastia:", 0)
        self.entry_data_principi_dinastia = self.entry_w(
            "Data de Començament:",
            1)
        self.entry_data_final_dinastia = self.entry_w("Data Final:", 2)
        self.entry_foto_path_dinastia = self.entry_w("Ruta de la Foto:", 3)

        tk.Button(self.frame,
                  text="Afegir Dinastia",
                  command=self.afegir_dinastia).grid(
                      row=4,
                      columnspan=2,
                      pady=10)
        tk.Button(self.frame,
                  text="Enrere",
                  command=self.menu_seleccio).grid(
                      row=5,
                      column=0,
                      pady=10)

    def crear_widgets_titol(self):
        # Implementació de widgets per a afegir títols
        self.entry_nom_titol = self.entry_w("Nom del Títol:", 0)
        self.entry_data_principi_titol = self.entry_w(
            "Data de Començament:",
            1)
        self.entry_data_final_titol = self.entry_w(
            "Data de Final:",
            2)
        self.entry_territori_titol = self.entry_w("Territori:", 3)
        self.entry_foto_path_titol = self.entry_w("Ruta de la Foto:", 4)

        tk.Button(self.frame,
                  text="Afegir Títol",
                  command=self.afegir_titol).grid(row=5,
                                                  columnspan=2,
                                                  pady=10)
        tk.Button(self.frame,
                  text="Enrere",
                  command=self.menu_seleccio).grid(row=6,
                                                   column=0,
                                                   pady=10)

    def crear_widgets_govern(self):
        # Implementació de widgets per a afegir governs
        auxi_c = self.c_entry_w("Nom del Senyor:", 0)
        self.choice_senyor_govern, self.dropdown_senyor_govern = auxi_c

        # Populate the choice box with senyor options from the database
        self.populate_senyors_dropdown()

        auxi_c2 = self.c_entry_w("Titol:", 1)
        self.choice_titol_govern, self.dropdown_titol_govern = auxi_c2

        # Populate the choice box with titol options from the database
        self.populate_titols_dropdown()

        self.entry_numero_govern = self.entry_w("Número:", 2)
        self.entry_data_debut_govern = self.entry_w("Data de Començament:", 3)
        self.entry_data_final_govern = self.entry_w("Data Final:", 4)

        tk.Button(self.frame,
                  text="Afegir govern",
                  command=self.afegir_govern).grid(row=5,
                                                   columnspan=2,
                                                   pady=10)

        tk.Button(self.frame,
                  text="Enrere",
                  command=self.menu_seleccio).grid(row=6,
                                                   column=0,
                                                   pady=10)

    def crear_widgets_moneda(self):
        # Implementació de widgets per a afegir monedes
        self.entry_valor_nominal = self.entry_w("Valor Nominal:", 0)
        self.entry_any = self.entry_w("Any:", 1)

        self.choice_govern, self.dropdown_govern = self.c_entry_w("Govern:", 2)
        self.populate_govern_dropdown()

        self.choice_devisa, self.dropdown_devisa = self.c_entry_w("Devisa:", 3)
        self.populate_devisa_dropdown()

        self.entry_descripcio_moneda = self.entry_w("Descripció:", 4)

        auxi_c = self.c_entry_w("Material:", 5)
        self.choice_material_moneda, self.dropdown_material_moneda = auxi_c
        self.populate_material_dropdown()

        self.entry_foto_path_moneda = self.entry_w("Ruta de la Foto:", 6)

        tk.Button(self.frame,
                  text="Afegir Moneda",
                  command=self.afegir_moneda).grid(row=7,
                                                   columnspan=2,
                                                   pady=10)
        tk.Button(self.frame,
                  text="Enrere",
                  command=self.menu_seleccio).grid(row=8,
                                                   column=0,
                                                   pady=10)

    def crear_widgets_devisa(self):
        # Implementació de widgets per a afegir devises
        self.entry_nom_devisa = self.entry_w("Nom de la Devisa:", 0)
        self.entry_data_creacio_devisa = self.entry_w("Data de Creació", 1)
        self.entry_data_final_devisa = self.entry_w("Darrera Emició:", 2)
        self.entry_foto_path_devisa = self.entry_w("Ruta de la Foto:", 3)

        tk.Button(self.frame,
                  text="Afegir Devisa",
                  command=self.afegir_devisa).grid(row=4,
                                                   columnspan=2,
                                                   pady=10)
        tk.Button(self.frame,
                  text="Enrere",
                  command=self.menu_seleccio).grid(row=5,
                                                   column=0,
                                                   pady=10)

    def populate_devisa_dropdown(self):
        # Populate the choice box with moneda options from the database
        conn, cursor = self.connect_database()
        try:
            cursor.execute("SELECT id, nom FROM devisa")
            devises = cursor.fetchall()
            for devisa in devises:
                self.dropdown_devisa['menu'].add_command(
                    label=devisa[1],
                    command=tk._setit(self.choice_devisa, devisa[0]))
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error",
                "Error en obtenir les devises de la base de dades:\n" + str(e))
        finally:
            conn.close()

    def populate_monedes_listbox(self):
        # Populate the listbox with moneda options from the database
        conn, cursor = self.connect_database()
        try:
            cursor.execute("""SELECT m.id, d.nom, s.nom, s.ordinal,
                           m.valor_nominal, m.any, t.territori FROM moneda m
                                JOIN devisa d ON m.devisa_id = d.id
                                JOIN govern g ON m.govern_id = g.id
                                JOIN senyor s ON g.senyor_id = s.id
                                JOIN titol t ON t.id = g.titol_id
                                ORDER BY d.nom, t.territori
                                """)
            monedes = cursor.fetchall()
            for moneda in monedes:
                if moneda[1] == "Euro":
                    label_moneda = (str(moneda[4]) + " " +
                                    moneda[1] + " de " + moneda[6])
                elif moneda[3] == "sense titol nobiliari":
                    label_moneda = (str(moneda[4]) + " " + moneda[1]
                                    + ", " + moneda[2])
                else:
                    label_moneda = (str(moneda[4]) + " " + moneda[1]
                                    + ", " + moneda[2] + " " + moneda[3])
                if moneda[5] != "":
                    label_moneda += " del " + str(moneda[5])
                self.listbox_moneda.insert(tk.END, label_moneda)
                self.monedes_dict[label_moneda] = moneda[0]
                # Store the label and ID in the dictionary

        except sqlite3.Error as e:
            messagebox.showerror(
                "Error",
                "Error en obtenir les monedes de la base de dades:\n" + str(e))
        finally:
            conn.close()

    def populate_material_dropdown(self):
        # Exemple de dades - substituir per una consulta a la base de dades
        material_options = ["Or",
                            "Plata",
                            "Bronze",
                            "Coure",
                            "Acer cobert de coure",
                            "Llautó",
                            "Alumini",
                            "Niquel"
                            "cuproníquel"]
        menu = self.dropdown_material_moneda['menu']
        menu.delete(0, 'end')
        for material in material_options:
            menu.add_command(
                label=material,
                command=tk._setit(self.choice_material_moneda, material))

    def populate_dinasties_dropdown(self):
        # Populate the choice box with dinastia options from the database
        conn, cursor = self.connect_database()
        try:
            cursor.execute("SELECT id, nom FROM dinastia")
            dinasties = cursor.fetchall()
            for dinastia in dinasties:
                self.dropdown_dinastia_senyor['menu'].add_command(
                    label=dinastia[1],
                    command=tk._setit(
                        self.choice_dinastia_senyor,
                        dinastia[0]))

        except sqlite3.Error as e:
            messagebox.showerror(
                "Error",
                ("Error en obtenir les dinasties" +
                 " de la base de dades:\n" + str(e)))
        finally:
            conn.close()

    def populate_senyors_dropdown(self):
        # Populate the choice box with senyor options from the database
        conn, cursor = self.connect_database()
        try:
            cursor.execute("""SELECT s.id, s.nom, s.ordinal, d.nom
                              FROM senyor s
                              JOIN dinastia d ON s.dinastia_id = d.id;""")
            senyors = cursor.fetchall()
            for senyor in senyors:
                label_senyor = (senyor[1] + " " +
                                senyor[2] + " (" + senyor[3] + ")")
                self.dropdown_senyor_govern['menu'].add_command(
                    label=label_senyor,
                    command=tk._setit(self.choice_senyor_govern, senyor[0]))
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error",
                "Error en obtenir els règims de la base de dades:\n" + str(e))
        finally:
            conn.close()

    def populate_titols_dropdown(self):
        # Populate the choice box with titol options from the database
        conn, cursor = self.connect_database()
        try:
            cursor.execute("SELECT id, nom FROM titol")
            titols = cursor.fetchall()
            for titol in titols:
                self.dropdown_titol_govern['menu'].add_command(
                    label=titol[1],
                    command=tk._setit(self.choice_titol_govern, titol[0]))
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error",
                "Error en obtenir els títols de la base de dades:\n" + str(e))
        finally:
            conn.close()

    def populate_govern_dropdown(self):
        # Populate the choice box with govern options from the database
        conn, cursor = self.connect_database()
        try:
            cursor.execute("""SELECT g.id, s.nom, s.ordinal, g.numero,
                           t.nom FROM govern g
                              JOIN titol t ON t.id = g.titol_id
                              JOIN senyor s ON s.id = g.senyor_id""")
            governs = cursor.fetchall()
            for govern in governs:
                if govern[2] == "":
                    label_govern = govern[1]
                else:
                    label_govern = (govern[1] + " " +
                                    govern[2] + ", " + govern[4] + ", " +
                                    govern[3] + " del seu nom")
                self.dropdown_govern['menu'].add_command(
                    label=label_govern,
                    command=tk._setit(self.choice_govern, govern[0]))
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error",
                "Error en obtenir els governs de la base de dades:\n" + str(e))
        finally:
            conn.close()

    def afegir_senyor(self):
        nom_senyor = self.entry_nom_senyor.get()
        data_naixement = self.entry_data_naixement_senyor.get()
        data_mort = self.entry_data_mort_senyor.get()
        ordinal = self.entry_ordinal_senyor.get()
        dinastia_id = self.choice_dinastia_senyor.get()
        foto_path = self.entry_foto_path_senyor.get()

        conn, cursor = self.connect_database()
        try:
            cursor.execute("INSERT INTO senyor (nom, data_neixement," +
                           "data_mort, ordinal, dinastia_id, " +
                           "foto_path) VALUES (?, ?, ?, ?, ?, ?)",
                           (nom_senyor, data_naixement,
                            data_mort, ordinal, dinastia_id, foto_path))
            conn.commit()
            messagebox.showinfo(
                "Afegit correctament",
                "Senyor afegit a la base de dades!")
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error",
                "Error en afegir el senyor a la base de dades:\n" + str(e))
        finally:
            conn.close()

    def afegir_dinastia(self):
        nom_dinastia = self.entry_nom_dinastia.get()
        data_principi = self.entry_data_principi_dinastia.get()
        data_final = self.entry_data_final_dinastia.get()
        foto_path = self.entry_foto_path_dinastia.get()

        conn, cursor = self.connect_database()
        try:
            cursor.execute(("INSERT INTO dinastia (nom, data_principi," +
                           " data_final, foto_path) VALUES (?, ?, ?, ?)"),
                           (nom_dinastia, data_principi,
                            data_final, foto_path))
            conn.commit()
            messagebox.showinfo(
                "Afegit correctament",
                "Dinastia afegida a la base de dades!")
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error",
                "Error en afegir la dinastia a la base de dades:\n" + str(e))
        finally:
            conn.close()

    def afegir_titol(self):
        nom_titol = self.entry_nom_titol.get()
        data_principi = self.entry_data_principi_titol.get()
        data_final = self.entry_data_final_titol.get()
        territori = self.entry_territori_titol.get()
        foto_path = self.entry_foto_path_titol.get()

        conn, cursor = self.connect_database()
        try:
            cursor.execute(("INSERT INTO titol (nom, data_principi, " +
                           "data_final, territori, foto_path)" +
                            " VALUES (?, ?, ?, ?, ?)"),
                           (nom_titol, data_principi, data_final,
                            territori, foto_path))
            conn.commit()
            messagebox.showinfo("Afegit correctament",
                                "Títol afegit a la base de dades!")
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error",
                "Error en afegir el títol a la base de dades:\n" + str(e))
        finally:
            conn.close()

    def afegir_govern(self):
        senyor_id = self.choice_senyor_govern.get()
        titol_id = self.choice_titol_govern.get()
        data_debut = self.entry_data_debut_govern.get()
        data_final = self.entry_data_final_govern.get()
        numero = self.entry_numero_govern.get()

        conn, cursor = self.connect_database()
        try:
            cursor.execute(("INSERT INTO govern (senyor_id, titol_id, " +
                            "numero, data_debut, data_final) " +
                            "VALUES (?, ?, ?, ?, ?)"),
                           (senyor_id, titol_id, numero,
                            data_debut, data_final))
            conn.commit()
            messagebox.showinfo("Afegit correctament",
                                "Govern afegit a la base de dades!")
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error",
                "Error en afegir el govern a la base de dades:\n" + str(e))
        finally:
            conn.close()

    def afegir_moneda(self):
        valor_nominal = self.entry_valor_nominal.get()
        any_moneda = self.entry_any.get()
        govern_id = self.choice_govern.get()
        descripcio = self.entry_descripcio_moneda.get()
        material = self.choice_material_moneda.get()
        foto_path = self.entry_foto_path_moneda.get()
        devisa = self.choice_devisa.get()

        conn, cursor = self.connect_database()
        try:
            cursor.execute(("INSERT INTO moneda (valor_nominal, any, " +
                            "govern_id, descripcio, material, " +
                            "foto_path, devisa_id) " +
                            "VALUES (?, ?, ?, ?, ?, ?, ?)"),
                           (valor_nominal, any_moneda, govern_id,
                            descripcio, material, foto_path, devisa))
            conn.commit()
            messagebox.showinfo(
                "Afegit correctament",
                "Moneda afegida a la base de dades!")
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error",
                "Error en afegir la moneda a la base de dades:\n" + str(e))
        finally:
            conn.close()

    def afegir_devisa(self):
        nom = self.entry_nom_devisa.get()
        data_creacio = self.entry_data_creacio_devisa.get()
        data_final = self.entry_data_final_devisa.get()
        foto = self.entry_foto_path_devisa.get()

        conn, cursor = self.connect_database()
        try:
            cursor.execute(("INSERT INTO devisa (nom, data_creacio, " +
                            "data_final, foto_path) VALUES (?, ?, ?, ?)"),
                           (nom, data_creacio, data_final, foto))
            conn.commit()
            messagebox.showinfo("Afegit correctament",
                                "Devisa afegida a la base de dades!")
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error",
                "Error en afegir la devisa a la base de dades:\n" + str(e))
        finally:
            conn.close()

    def afegir_peça(self):
        selected_index = self.listbox_moneda.curselection()
        if selected_index:
            selected_moneda_label = self.listbox_moneda.get(selected_index)
            moneda_id = self.monedes_dict[selected_moneda_label]
            # Retrieve the ID using the label
        else:
            messagebox.showwarning("Selecció requerida",
                                   "Si us plau, selecciona una moneda.")
            return
        estat = self.entry_estat.get()
        descripcio = self.entry_descripcio_peça.get()
        serie_emissio = self.entry_serie_emissio.get()
        valor_estimat = self.entry_valor_estimat.get()
        lloc = self.entry_lloc.get()
        foto_path = self.entry_foto_path_peça.get()

        conn, cursor = self.connect_database()
        try:
            cursor.execute(("INSERT INTO peça (moneda_id, estat, " +
                            "descripcio, serie_emissio," +
                            " valor_estimat, lloc, foto_path) " +
                            "ALUES (?, ?, ?, ?, ?, ?, ?)"),
                           (moneda_id, estat, descripcio,
                            serie_emissio, valor_estimat, lloc, foto_path))
            conn.commit()
            messagebox.showinfo("Afegit correctament",
                                "Peça afegida a la base de dades!")
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error",
                "Error en afegir la peça a la base de dades:\n" + str(e))
        finally:
            conn.close()

    def connect_database(self):
        # Connect to SQLite database
        path = os.getcwd()
        if os.path.basename(os.getcwd()) != "app_monedes-main":
            raise ValueError("Not in good place, should be" +
                             ".../app_monedes-main")
        conn = sqlite3.connect(path + "/data/bdd_numismatica.db")
        cursor = conn.cursor()
        return conn, cursor
