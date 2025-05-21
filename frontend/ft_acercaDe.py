import customtkinter as ctk
from PIL import Image

class AcercaDePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#1a1c1e")  # Fondo general

        ctk.CTkLabel(self, text="📘 ModelaMath", font=("Segoe UI", 30, "bold"), text_color="#6c63ff").pack(pady=(30, 5))
        ctk.CTkLabel(self, text="Proyecto Académico - Modelos Matemáticos", font=("Segoe UI", 18), text_color="#d3d3d3").pack(pady=(0, 10))

        # ---------- CONTENEDOR CON SCROLL ----------
        contenedor_scroll = ctk.CTkScrollableFrame(self, fg_color="#292d32", corner_radius=15, border_width=1, border_color="#444")
        contenedor_scroll.pack(padx=40, pady=10, fill="both", expand=True)

        # ---------- LOGO ----------
        try:
            logo = ctk.CTkImage(dark_image=Image.open("assets/logo2.png"), size=(120, 120))
            ctk.CTkLabel(contenedor_scroll, image=logo, text="").pack(pady=(15, 5))
        except:
            ctk.CTkLabel(contenedor_scroll, text="🧠", font=("Arial", 50)).pack(pady=(15, 5))

        ctk.CTkLabel(contenedor_scroll, text="CALCULADORA CIENTÍFICA", font=("Segoe UI", 20, "bold"), text_color="#7d74ff").pack(pady=5)

        # ---------- INFO LÍNEA POR LÍNEA ----------
        info = [
            ("📌 Título:", "Calculadora Científica con Interfaz Gráfica en Python"),
            ("👨‍🎓 Autor:", "Victor Alejandro Celi Rivadeneira"),
            ("🎓 Carrera:", "Ingeniería en Software"),
            ("📆 Semestre:", "6to Semestre C1"),
            ("📚 Materia:", "Modelos Matemáticos y Simulación"),
            ("👨‍🏫 Docente:", "Isidro Fabricio Morales Torres"),
            ("🧩 Descripción:", 
             "Aplicación desarrollada para resolver operaciones simbólicas y gráficas de matemáticas: matrices, vectores, polinomios, derivadas, integrales y funciones 2D/3D."),
            ("🛠 Herramientas:", "Python, CustomTkinter, SymPy, NumPy, Matplotlib"),
            ("📦 Año:", "2025"),
        ]

        for icono, texto in info:
            fila = ctk.CTkFrame(contenedor_scroll, fg_color="transparent")
            fila.pack(anchor="w", fill="x", padx=20, pady=4)
            ctk.CTkLabel(fila, text=icono, font=("Segoe UI", 14, "bold"), text_color="#a4c8f0", width=120, anchor="w").pack(side="left")
            ctk.CTkLabel(fila, text=texto, font=("Segoe UI", 14), text_color="#e0e0e0", wraplength=640, justify="left").pack(side="left", padx=5)

        # ---------- CRÉDITO ----------
        ctk.CTkLabel(self, text="© 2025 - Todos los derechos reservados", font=("Segoe UI", 12), text_color="#999").pack(pady=10)
