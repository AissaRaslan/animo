import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from controlador import Controlador


class Vista:
    def __init__(self, root, nombre_usuario):
        self.root = root
        self.nombre_usuario = nombre_usuario

        # Ventana principal
        self.root.title("Control del Ánimo")
        self.root.geometry("800x1080")  # más grande para que escale bien
        self.root.configure(bg="#DAD6F8")
        self.root.minsize(400, 600)

        # Controlador
        self.controlador = Controlador(self)

        # Variables
        self.animo_var = tk.IntVar(value=3)

        # === Hábitos básicos ===
        self.habitos_basicos = {
            "Agua": tk.BooleanVar(),
            "Ejercicio": tk.BooleanVar(),
            "Estudio": tk.BooleanVar()
        }

        # === Factores ===
        self.habitos = {
            "Salud": tk.BooleanVar(),
            "Ejercicio": tk.BooleanVar(),
            "Comida": tk.BooleanVar(),
            "Sueño": tk.BooleanVar(),
            "Pasatiempo": tk.BooleanVar(),
            "Estudio": tk.BooleanVar(),
            "Amigos": tk.BooleanVar(),
            "Familia": tk.BooleanVar(),
        }

        # Estilos globales con fuentes más grandes
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("TButton",
                        background="#9E8BDA",
                        foreground="#2B272E",
                        padding=10,
                        font=("Helvetica", 14, "bold"))  # ⬅ más grande

        style.configure("Custom.TCheckbutton",
                        background="#EDE7FF",
                        foreground="#1E1E2A",
                        font=("Helvetica", 14))  # ⬅ más grande

        # Contenedor redondeado
        self.container_bg = "#EDE7FF"
        self.container_pad = 18
        self.container_radius = 20

        self.canvas = tk.Canvas(self.root, bg=self.root["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.main_frame = tk.Frame(self.canvas, bg=self.container_bg)
        self._container_items = []

        def _on_resize(event=None):
            for item in list(self._container_items):
                try:
                    self.canvas.delete(item)
                except Exception:
                    pass
            self._container_items.clear()

            w = max(self.canvas.winfo_width(), 50)
            h = max(self.canvas.winfo_height(), 50)
            x1 = self.container_pad
            y1 = self.container_pad
            x2 = max(w - self.container_pad, x1 + 10)
            y2 = max(h - self.container_pad, y1 + 10)
            r = min(self.container_radius, (x2 - x1) // 2, (y2 - y1) // 2)

            a1 = self.canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, style='pieslice', outline='', fill=self.container_bg)
            a2 = self.canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, style='pieslice', outline='', fill=self.container_bg)
            a3 = self.canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, style='pieslice', outline='', fill=self.container_bg)
            a4 = self.canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, style='pieslice', outline='', fill=self.container_bg)

            rect_c = self.canvas.create_rectangle(x1 + r, y1, x2 - r, y2, outline='', fill=self.container_bg)
            rect_v = self.canvas.create_rectangle(x1, y1 + r, x2, y2 - r, outline='', fill=self.container_bg)

            self._container_items.extend([a1, a2, a3, a4, rect_c, rect_v])

            inner_w = x2 - x1
            inner_h = y2 - y1
            if hasattr(self, '_frame_window'):
                self.canvas.coords(self._frame_window, x1, y1)
                self.canvas.itemconfig(self._frame_window, width=inner_w, height=inner_h)
            else:
                self._frame_window = self.canvas.create_window(x1, y1, anchor='nw', window=self.main_frame, width=inner_w, height=inner_h)

        self.canvas.bind('<Configure>', _on_resize)

        self.crear_interfaz()

    def crear_interfaz(self):
        # Bienvenida
        tk.Label(self.main_frame, text=f"Hola, {self.nombre_usuario} 👋",
                 font=("Helvetica", 22, "bold"), fg="#1E1E2A", bg=self.container_bg).pack(pady=15)

        tk.Label(self.main_frame, text="¿Cómo te sientes hoy?",
                 font=("Helvetica", 18), fg="#1E1E2A", bg=self.container_bg).pack(pady=10)

        # Imagen + Slider
        self.img_label = tk.Label(self.main_frame, bg=self.container_bg)
        self.img_label.pack(pady=10)
        self.actualizar_imagen()

        escala = tk.Scale(self.main_frame, from_=1, to=5, orient="horizontal",
                          variable=self.animo_var, bg=self.container_bg,
                          highlightthickness=0, troughcolor="#D0C7F0",
                          fg="#1E1E2A", font=("Helvetica", 14))  # ⬅ fuente slider
        escala.pack(pady=10)
        self.animo_var.trace("w", lambda *a: self.actualizar_imagen())

        # Hábitos cumplidos
        tk.Label(self.main_frame, text="Hábitos cumplidos hoy:",
                 font=("Helvetica", 18, "bold"), fg="#1E1E2A", bg=self.container_bg).pack(pady=(20, 10))

        marco_basicos = tk.Frame(self.main_frame, bg=self.container_bg)
        marco_basicos.pack(pady=5)
        for i, (h, var) in enumerate(self.habitos_basicos.items()):
            ttk.Checkbutton(marco_basicos, text=h, variable=var, style="Custom.TCheckbutton").grid(row=0, column=i, padx=10, pady=5)

        # Factores
        tk.Label(self.main_frame, text="¿Qué influye en tu estado?",
                 font=("Helvetica", 18, "bold"), fg="#1E1E2A", bg=self.container_bg).pack(pady=(25, 10))

        marco_habitos = tk.Frame(self.main_frame, bg=self.container_bg)
        marco_habitos.pack(pady=5)
        for i, (h, var) in enumerate(self.habitos.items()):
            row = i // 4
            col = i % 4
            ttk.Checkbutton(marco_habitos, text=h, variable=var, style="Custom.TCheckbutton").grid(row=row, column=col, padx=10, pady=8)

        # Notas
        tk.Label(self.main_frame, text="Notas",
                 font=("Helvetica", 18, "bold"), fg="#1E1E2A", bg=self.container_bg).pack(pady=(25, 5))

        self.texto_nota = tk.Text(self.main_frame, height=6, width=40, wrap="word",
                                  bg="#C4BCE4", fg="#1E1E2A", insertbackground="black",
                                  relief="flat", font=("Helvetica", 14))  # ⬅ más grande
        self.texto_nota.pack()
        self.contador = tk.Label(self.main_frame, text="0/200", fg="#555555",
                                 bg=self.container_bg, font=("Helvetica", 12))
        self.contador.pack()
        self.texto_nota.bind("<KeyRelease>", self.actualizar_contador)

        # Botones
        ttk.Button(self.main_frame, text="Guardar registro", command=self.guardar).pack(pady=15)
        ttk.Button(self.main_frame, text="Ver registros", command=self.ver_registros).pack(pady=10)

    # ==== resto igual que antes ====
    def actualizar_imagen(self):
        nivel = self.animo_var.get()
        try:
            img = Image.open(f"animo{nivel}.png").resize((120, 120))  # más grande
            self.img = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.img, text="")
        except (FileNotFoundError, OSError, tk.TclError):
            self.img_label.config(text=f"[animo{nivel}.png]", image="")

    def actualizar_contador(self, event=None):
        texto = self.texto_nota.get("1.0", "end-1c")
        if len(texto) > 200:
            self.texto_nota.delete("1.0+200c", "end")
        self.contador.config(text=f"{len(texto)}/200")

    def guardar(self):
        registro_usuario = self.nombre_usuario
        registro_animo = self.animo_var.get()
        registro_habitos_basicos = {h: v.get() for h, v in self.habitos_basicos.items()}
        registro_habitos_estado = {h: v.get() for h, v in self.habitos.items()}
        registro_nota = self.texto_nota.get("1.0", "end-1c").strip()

        self.controlador.guardar_registro(
            registro_usuario,
            registro_animo,
            registro_habitos_basicos,
            registro_habitos_estado,
            registro_nota
        )

        self.animo_var.set(3)
        for var in self.habitos_basicos.values():
            var.set(False)
        for var in self.habitos.values():
            var.set(False)
        self.texto_nota.delete("1.0", "end")
        self.contador.config(text="0/200")

    def ver_registros(self):
        data = self.controlador.obtener_registros()

        if not data:
            messagebox.showinfo("Registros", "No hay registros guardados aún.")
            return
        ventana = tk.Toplevel(self.root)
        ventana.title("Registros guardados")
        # tamaño preferido
        vw, vh = 700, 600
        # marcar como transient al padre y asegurar layout calculado
        ventana.transient(self.root)
        ventana.resizable(True, True)
        ventana.update_idletasks()

        # intentar centrar respecto a la ventana principal (root)
        try:
            rx = self.root.winfo_rootx()
            ry = self.root.winfo_rooty()
            rw = self.root.winfo_width()
            rh = self.root.winfo_height()
            x = rx + max((rw - vw) // 2, 0)
            y = ry + max((rh - vh) // 2, 0)
        except Exception:
            # fallback: centrar en pantalla
            sw = ventana.winfo_screenwidth()
            sh = ventana.winfo_screenheight()
            x = max((sw - vw) // 2, 0)
            y = max((sh - vh) // 2, 0)

        ventana.geometry(f"{vw}x{vh}+{x}+{y}")
        ventana.configure(bg=self.root["bg"])

        canvas = tk.Canvas(ventana, bg=self.root["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.container_bg)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # mantener referencias a mini-imágenes para evitar GC
        mini_imgs = []

        for r in reversed(data):
            # fila horizontal por registro
            fila = tk.Frame(scroll_frame, bg=self.container_bg)
            fila.pack(fill="x", pady=6, padx=6)

            nivel = r.get("animo", 3) or 3
            try:
                img = Image.open(f"animo{nivel}.png").resize((48, 48))
                photo = ImageTk.PhotoImage(img)
                mini_imgs.append(photo)
                lbl_img = tk.Label(fila, image=photo, bg=self.container_bg)
            except (FileNotFoundError, OSError, tk.TclError):
                # fallback texto
                lbl_img = tk.Label(fila, text=f"[{nivel}]", width=6, bg=self.container_bg, fg="#1E1E2A")
            lbl_img.pack(side="left", padx=(0, 12))

            contenido = tk.Frame(fila, bg=self.container_bg)
            contenido.pack(side="left", fill="x", expand=True)

            tk.Label(contenido, text=f"{r.get('fecha', '')} - {r.get('usuario', '')}", fg="#1E1E2A", bg=self.container_bg, font=("Helvetica", 14, "bold")).pack(anchor="w")
            tk.Label(contenido, text=f"Ánimo: {r.get('animo', '')}", fg="#1E1E2A", bg=self.container_bg, font=("Helvetica", 13)).pack(anchor="w")

            basicos = [h for h, v in r.get('habitos_basicos', {}).items() if v]
            estado = [h for h, v in r.get('habitos_estado', {}).items() if v]
            tk.Label(contenido, text=("Hábitos cumplidos: " + ", ".join(basicos)) if basicos else "Hábitos cumplidos: Ninguno", fg="#1E1E2A", bg=self.container_bg, font=("Helvetica", 13)).pack(anchor="w")
            tk.Label(contenido, text=("Factores: " + ", ".join(estado)) if estado else "Factores: Ninguno", fg="#1E1E2A", bg=self.container_bg, font=("Helvetica", 13)).pack(anchor="w")
            if r.get("nota"):
                tk.Label(contenido, text=f"Nota: {r.get('nota')}", fg="#555555", bg=self.container_bg, wraplength=500, font=("Helvetica", 13)).pack(anchor="w")
            ttk.Separator(scroll_frame, orient="horizontal").pack(fill="x", pady=8)

        # guardar las imágenes en la ventana para que no las recolecte
        ventana.mini_imgs = mini_imgs

