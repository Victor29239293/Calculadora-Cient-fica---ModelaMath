import customtkinter as ctk
from PIL import Image
from frontend.ft_menu import MenuPage
from frontend.ft_matriz import MatricesPage
from frontend.ft_polinomio import PolinomiosPage
from frontend.ft_vector import VectoresPage 
from frontend.ft_grafica2D import Graficas2DPage
from frontend.ft_grafica3D import Graficas3DPage
from frontend.ft_calculo import CalculoPage
from frontend.ft_acercaDe import AcercaDePage
from frontend.ft_sistema_diferencialEDO import SistemaDiferencialPage
from frontend.ft_ecucionesdiferencial    import EcuacionesDiferencialesUI
from frontend.ft_distribuciones import DistribucionesPage
from frontend.ft_agricultura_I import AgriculturaApp
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLOR_BG = "#1a1c1e"
COLOR_NAV = "#2b2e33"
COLOR_ACCENT = "#6c63ff"
COLOR_ACCENT_HOVER = "#7d74ff"
COLOR_TEXT = "#ffffff"
COLOR_SPLASH_BG = "#1f2327"
COLOR_TEXTO_NORMAL = "#b2ebf2"

class MenuPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Científica - ModelaMath")
        self.geometry("1280x800")
        self.minsize(1024, 640)
        self.configure(fg_color=COLOR_BG)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.init_sidebar()
        self.init_main_content()
        self.abrir_inicio()

    def init_sidebar(self):
        # Sidebar scrollable
        sidebar_container = ctk.CTkFrame(self, fg_color=COLOR_NAV, width=240, corner_radius=0)
        sidebar_container.grid(row=0, column=0, sticky="ns")
        sidebar_container.grid_propagate(False)

        scroll = ctk.CTkScrollableFrame(sidebar_container,  fg_color = "#101117", 
                                                     scrollbar_fg_color="#1A1B26",
                                                     scrollbar_button_color="#7B68EE",
                                                     scrollbar_button_hover_color="#634BD6", width=240)
        scroll.pack(fill="both", expand=True)

        try:
            logo = ctk.CTkImage(Image.open("assets/logo2.png"), size=(100, 125))
            ctk.CTkLabel(scroll, image=logo, text="").pack(pady=(30, 10))
        except:
            ctk.CTkLabel(scroll, text="🧠", font=("Arial", 48), text_color=COLOR_ACCENT).pack(pady=(30, 10))

        ctk.CTkLabel(scroll, text="ModelaMath", font=("Segoe UI", 22, "bold"), text_color=COLOR_TEXT).pack(pady=(0, 20))

        self.botones = [
            ("Menú Principal", self.abrir_inicio),
            ("Matrices", self.abrir_matrices),
            ("Polinomios", self.abrir_polinomios),
            ("Vectores", self.abrir_vectors),
            ("Gráficas 2D", self.abrir_graficas_2d),
            ("Gráficas 3D", self.abrir_graficas_3d),
            ("Derivada e Integral", self.abrir_calculo),
            ("Ecuaciones D.", self.abrir_sistema_ecuaciones_lineales),
            ("Sistema De EDOS.", self.abrir_sistemaEDO),
            ("Distribucion.", self.abrir_distribuciones),
            ("Agricultura inteligente", self.abrir_sir),
            ("Acerca de", self.abrir_acerca_de)
        ]

        for nombre, accion in self.botones:
            ctk.CTkButton(
                scroll,
                text=nombre,
                command=accion,
                font=("Segoe UI", 16, "bold"),
                fg_color=COLOR_ACCENT,
                hover_color=COLOR_ACCENT_HOVER,
                text_color=COLOR_TEXT,
                corner_radius=12,
                height=46
            ).pack(fill="x", padx=20, pady=8)

    def init_main_content(self):
        self.frame_contenido = ctk.CTkFrame(self, fg_color="#23272a", corner_radius=20)
        self.frame_contenido.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.frame_contenido.grid_propagate(True)

    def limpiar_pantalla(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    def abrir_inicio(self):
        self.limpiar_pantalla()
        self.pagina_actual = MenuPage(self.frame_contenido)
        self.pagina_actual.pack(fill="both", expand=True, padx=10, pady=10)

    def abrir_matrices(self):
        self.limpiar_pantalla()
        self.pagina_actual = MatricesPage(self.frame_contenido)
        self.pagina_actual.pack(fill="both", expand=True, padx=10, pady=10)
    def abrir_polinomios(self):
        self.limpiar_pantalla()
        self.pagina_actual = PolinomiosPage(self.frame_contenido)
        self.pagina_actual.pack(fill="both", expand=True, padx=10, pady=10)
    def abrir_vectors(self):
        self.limpiar_pantalla()
        self.pagina_actual = VectoresPage(self.frame_contenido)
        self.pagina_actual.pack(fill="both", expand=True, padx=10, pady=10)
        
    def abrir_graficas_2d(self):
        self.limpiar_pantalla()
        self.pagina_actual = Graficas2DPage(self.frame_contenido)
        self.pagina_actual.pack(fill="both", expand=True, padx=10, pady=10)
    def abrir_graficas_3d(self):
        self.limpiar_pantalla()
        self.pagina_actual = Graficas3DPage(self.frame_contenido)
        self.pagina_actual.pack(fill="both", expand=True, padx=10, pady=10)
    def abrir_calculo(self):
        self.limpiar_pantalla()
        self.pagina_actual = CalculoPage(self.frame_contenido)
        self.pagina_actual.pack(fill="both", expand=True, padx=10, pady=10)
    def abrir_sistema_ecuaciones_lineales(self):
        self.limpiar_pantalla()
        self.pagina_actual = EcuacionesDiferencialesUI(self.frame_contenido)
        self.pagina_actual.pack(fill="both", expand=True, padx=10, pady=10)
    def abrir_sistemaEDO(self):
        self.limpiar_pantalla()
        self.pagina_actual = SistemaDiferencialPage(self.frame_contenido)
        self.pagina_actual.pack(fill="both", expand=True, padx=10, pady=10)
    def abrir_distribuciones(self):
        self.limpiar_pantalla()
        self.pagina_actual = DistribucionesPage(self.frame_contenido)
        self.pagina_actual.pack(fill="both", expand=True, padx=10, pady=10)
    def abrir_sir(self):
        self.limpiar_pantalla()
        self.pagina_actual = AgriculturaApp(self.frame_contenido)
        self.pagina_actual.pack(fill="both", expand=True, padx=10, pady=10)
    def abrir_acerca_de(self):
        self.limpiar_pantalla()
        self.pagina_actual = AcercaDePage(self.frame_contenido)
        self.pagina_actual.pack(fill="both", expand=True, padx=10, pady=10)
    
class SplashScreen(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("500x360")
        self.overrideredirect(True)
        self.configure(fg_color=COLOR_SPLASH_BG)
        self.lift()

        try:
            logo = ctk.CTkImage(Image.open("assets/logo2.png"), size=(140, 140))
            ctk.CTkLabel(self, image=logo, text="").pack(pady=(50, 10))
        except:
            ctk.CTkLabel(self, text="🧠", font=("Arial", 64), text_color=COLOR_TEXTO_NORMAL).pack(pady=(50, 10))

        ctk.CTkLabel(self, text="CALCULADORA CIENTÍFICA", font=("Segoe UI", 22, "bold"), text_color=COLOR_TEXTO_NORMAL).pack(pady=(0, 5))
        ctk.CTkLabel(self, text="Cargando módulo de operaciones...", font=("Segoe UI", 16), text_color="#81d4fa").pack()

        self.after(2500, self.close_splash)

    def close_splash(self):
        self.master.state("zoomed")
        self.master.deiconify()
        self.destroy()


if __name__ == "__main__":
    app = MenuPrincipal()
    app.withdraw()
    splash = SplashScreen(app)
    app.mainloop()
