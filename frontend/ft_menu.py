import customtkinter as ctk
from PIL import Image

class MenuPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#1a1c1e")  # Fondo oscuro

        try:
            logo_img = ctk.CTkImage(Image.open("assets/logo2.png"), size=(100, 100))
            ctk.CTkLabel(self, image=logo_img, text="").pack(pady=(20, 10))
        except:
            ctk.CTkLabel(self, text="🧠", font=("Arial", 48), text_color="#6c63ff").pack(pady=(20, 10))

        # Título principal
        titulo = ctk.CTkLabel(
            self,
            text="Bienvenido a ModelaMath",
            font=("Segoe UI", 30, "bold"),
            text_color="#6c63ff"
        )
        titulo.pack(pady=(0, 10))

        # Subtítulo
        subtitulo = ctk.CTkLabel(
            self,
            text="Selecciona una categoría desde el menú lateral para comenzar",
            font=("Segoe UI", 18),
            text_color="#c4c7d4"
        )
        subtitulo.pack(pady=(0, 30))

        # Contenedor para la información
        contenedor_scroll = ctk.CTkFrame(self, fg_color="#292d32", corner_radius=16)
        contenedor_scroll.pack(padx=40, pady=20, fill="both", expand=True)

        # Información organizada en líneas con iconos
        info = [
            ("🔧 Módulos disponibles:\n", 
             "• Operaciones con matrices y vectores\n"
             "• Cálculo simbólico (derivadas e integrales)\n"
             "• Gráficas interactivas en 2D y 3D\n"
             "• Manipulación y visualización de polinomios\n"
             "• Información sobre la aplicación y su desarrollo\n"),

            ("📌 Recomendaciones de uso:\n", 
             "• Ingresa datos numéricos válidos en cada módulo\n"
             "• Utiliza el modo pantalla completa para mejor experiencia\n"
             "• Los sistemas Ax = B requieren matrices cuadradas\n"),

            ("✅ Aplicación modular, intuitiva y preparada para futuras expansiones 🚀", "")
        ]

        # Agregar la información en el contenedor
        for icono, texto in info:
            fila = ctk.CTkFrame(contenedor_scroll, fg_color="transparent")
            fila.pack(anchor="w", fill="x", padx=20, pady=6)

            # Etiqueta del icono con texto
            ctk.CTkLabel(fila, 
                         text=icono, 
                         font=("Segoe UI", 16, "bold"), 
                         text_color="#a4c8f0", 
                         width=160, 
                         anchor="w").pack(side="left", padx=5)

            # Etiqueta del texto
            ctk.CTkLabel(fila, 
                         text=texto, 
                         font=("Segoe UI", 14), 
                         text_color="#e0e0e0", 
                         wraplength=640, 
                         justify="left").pack(side="left", padx=5)

        # Ajustes finales: control de espaciado y visibilidad
        contenedor_scroll.grid_rowconfigure(0, weight=1)

