import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import messagebox
from frontend.ft_menu import MenuPage
from frontend.ft_matriz import MatricesPage
from frontend.ft_polinomio import PolinomiosPage
from frontend.ft_vector import VectoresPage 
from frontend.ft_grafica2D import Graficas2DPage
from frontend.ft_grafica3D import Graficas3DPage
from frontend.ft_calculo import CalculoPage
from frontend.ft_acercaDe import AcercaDePage
from frontend.ft_sistema_diferencialEDO import SistemaDiferencialPage
from frontend.ft_ecucionesdiferencial import EcuacionesDiferencialesUI
from frontend.ft_distribuciones import DistribucionesPage
from frontend.ft_agricultura_I import AgriculturaApp

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ColorTheme:
    PRIMARY_BG = "#0d1117"           
    SECONDARY_BG = "#161b22"         
    SIDEBAR_BG = "#21262d"           # Fondo del sidebar
    CARD_BG = "#30363d"              # Fondo de tarjetas
    
    # Colores de acento
    ACCENT_PRIMARY = "#58a6ff"       # Azul principal
    ACCENT_SECONDARY = "#7c3aed"     # Púrpura
    ACCENT_SUCCESS = "#3fb950"       # Verde
    ACCENT_WARNING = "#d29922"       # Amarillo
    ACCENT_DANGER = "#f85149"        # Rojo

    TEXT_PRIMARY = "#f0f6fc"         # Texto principal
    TEXT_SECONDARY = "#8b949e"       # Texto secundario
    TEXT_MUTED = "#6e7681"           # Texto deshabilitado
    
    BORDER_DEFAULT = "#30363d"       
    SHADOW_LIGHT = "#0d1117"
    
    GRADIENT_PRIMARY = ["#7c3aed", "#58a6ff"]
    GRADIENT_SECONDARY = ["#3fb950", "#58a6ff"]

class ModernButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):

        default_config = {
            "font": ("Segoe UI", 15, "bold"),
            "fg_color": ColorTheme.ACCENT_PRIMARY,
            "hover_color": ColorTheme.ACCENT_SECONDARY,
            "text_color": ColorTheme.TEXT_PRIMARY,
            "corner_radius": 12,
            "height": 50,
            "border_width": 0,
        }
        
        default_config.update(kwargs)
        super().__init__(master, **default_config)
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, event=None):  
        self.configure(cursor="hand2")
        
    def _on_leave(self, event=None):  
        self.configure(cursor="")

class AnimatedSidebar(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.is_expanded = True
        self.width_collapsed = 80
        self.width_expanded = 280
        
    def toggle_sidebar(self):
        if self.is_expanded:
            self.collapse()
        else:
            self.expand()
            
    def collapse(self):
        self.is_expanded = False
        self.configure(width=self.width_collapsed)
        
    def expand(self):
        self.is_expanded = True
        self.configure(width=self.width_expanded)

class MenuPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_variables()
        self.init_components()
        self.load_initial_page()

    def setup_window(self):
        self.title("ModelaMath - Calculadora Científica Avanzada")
        self.geometry("1400x900")
        self.minsize(1200, 700)
        self.configure(fg_color=ColorTheme.PRIMARY_BG)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
    def setup_variables(self):
        self.current_page = None
        self.sidebar_expanded = True
        
    def init_components(self):
        self.create_header()
        self.create_sidebar()
        self.create_main_content()
        
    def create_header(self):
        self.header_frame = ctk.CTkFrame(
            self, 
            height=88, 
            fg_color=ColorTheme.SECONDARY_BG,
            corner_radius=0
        )
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        self.header_frame.grid_propagate(False)
        self.header_frame.pack_propagate(False)

        header_container = ctk.CTkFrame(self.header_frame, fg_color="transparent", height=24)
        header_container.pack(fill="both", expand=True)
        header_container.pack_propagate(False) 

        self.toggle_btn = ctk.CTkButton(
            header_container,
            text="☰",
            width=25,
            height=30,
            font=("Segoe UI", 9),
            fg_color=ColorTheme.ACCENT_PRIMARY,
            hover_color=ColorTheme.ACCENT_SECONDARY,
            command=self.toggle_sidebar
        )
        self.toggle_btn.pack(side="left", padx=(2, 4), pady=0)


        title_label = ctk.CTkLabel(
            header_container,
            text="ModelaMath",
            font=("Segoe UI", 18, "bold"),
            text_color=ColorTheme.TEXT_PRIMARY
        )
        title_label.pack(side="left", pady=0)

        subtitle_label = ctk.CTkLabel(
            header_container,
            text="Calculadora Científica Avanzada",
            font=("Segoe UI", 12),
            text_color=ColorTheme.TEXT_SECONDARY
        )
        subtitle_label.pack(side="left", padx=(3, 0), pady=0)

        controls_frame = ctk.CTkFrame(header_container, fg_color="transparent", height=18)
        controls_frame.pack(side="right", pady=0)
        
    def create_sidebar(self):

        self.sidebar_frame = ctk.CTkFrame(
            self, 
            width=280, 
            fg_color=ColorTheme.SIDEBAR_BG,
            corner_radius=0
        )
        self.sidebar_frame.grid(row=1, column=0, sticky="ns", padx=0, pady=0)
        self.sidebar_frame.grid_propagate(False)

        self.sidebar_scroll = ctk.CTkScrollableFrame(
            self.sidebar_frame,
            fg_color=ColorTheme.SIDEBAR_BG,
            scrollbar_fg_color=ColorTheme.BORDER_DEFAULT,
            scrollbar_button_color=ColorTheme.ACCENT_PRIMARY,
            scrollbar_button_hover_color=ColorTheme.ACCENT_SECONDARY,
            width=280
        )
        self.sidebar_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_logo_section()
        
        separator = ctk.CTkFrame(self.sidebar_scroll, height=2, fg_color=ColorTheme.BORDER_DEFAULT)
        separator.pack(fill="x", padx=20, pady=(10, 20))

        self.create_navigation_buttons()
        
    def create_logo_section(self):
        logo_frame = ctk.CTkFrame(self.sidebar_scroll, fg_color="transparent")
        logo_frame.pack(fill="x", pady=(0, 20))
        
        try:
            logo_image = ctk.CTkImage(Image.open("assets/logo2.png"), size=(80, 80))
            logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="")
            logo_label.pack(pady=(20, 10))
        except:
            logo_label = ctk.CTkLabel(
                logo_frame, 
                text="🧠", 
                font=("Arial", 48), 
                text_color=ColorTheme.ACCENT_PRIMARY
            )
            logo_label.pack(pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            logo_frame,
            text="ModelaMath",
            font=("Segoe UI", 20, "bold"),
            text_color=ColorTheme.TEXT_PRIMARY
        )
        title_label.pack()
        
        version_label = ctk.CTkLabel(
            logo_frame,
            text="v2.0 Premium",
            font=("Segoe UI", 10),
            text_color=ColorTheme.TEXT_SECONDARY
        )
        version_label.pack(pady=(5, 0))
        
    def create_navigation_buttons(self):

        self.navigation_buttons = [
            {
                "text": "🏠 Inicio",
                "command": self.abrir_inicio,
                "color": ColorTheme.ACCENT_PRIMARY,
                "description": "Página principal"
            },
            {
                "text": "🔢 Matrices",
                "command": self.abrir_matrices,
                "color":  ColorTheme.ACCENT_PRIMARY,
                "description": "Operaciones con matrices"
            },
            {
                "text": "📊 Polinomios",
                "command": self.abrir_polinomios,
                "color":  ColorTheme.ACCENT_PRIMARY,
                "description": "Cálculo de polinomios"
            },
            {
                "text": "📐 Vectores",
                "command": self.abrir_vectors,
                "color":  ColorTheme.ACCENT_PRIMARY,
                "description": "Operaciones vectoriales"
            },
            {
                "text": "📈 Gráficas 2D",
                "command": self.abrir_graficas_2d,
                "color":  ColorTheme.ACCENT_PRIMARY,
                "description": "Visualización 2D"
            },
            {
                "text": "🌐 Gráficas 3D",
                "command": self.abrir_graficas_3d,
                "color":  ColorTheme.ACCENT_PRIMARY,
                "description": "Visualización 3D"
            },
            {
                "text": "∫ Cálculo",
                "command": self.abrir_calculo,
                "color": ColorTheme.ACCENT_PRIMARY,
                "description": "Derivadas e integrales"
            },
            {
                "text": "🔬 Ec. Diferenciales",
                "command": self.abrir_sistema_ecuaciones_lineales,
                "color":  ColorTheme.ACCENT_PRIMARY,
                "description": "Ecuaciones diferenciales"
            },
            {
                "text": "⚙️ Sistema EDOs",
                "command": self.abrir_sistemaEDO,
                "color":  ColorTheme.ACCENT_PRIMARY,
                "description": "Sistemas de EDOs"
            },
            {
                "text": "📊 Distribuciones",
                "command": self.abrir_distribuciones,
                "color": ColorTheme.ACCENT_PRIMARY,
                "description": "Distribuciones estadísticas"
            },
            {
                "text": "🌱 Agricultura IA",
                "command": self.abrir_sir,
                "color":  ColorTheme.ACCENT_PRIMARY,
                "description": "Agricultura inteligente"
            },
            {
                "text": "ℹ️ Acerca de",
                "command": self.abrir_acerca_de,
                "color":  ColorTheme.ACCENT_PRIMARY,
                "description": "Información de la app"
            }
        ]
        
        self.button_widgets = []
        
        for btn_config in self.navigation_buttons:
            btn_container = ctk.CTkFrame(self.sidebar_scroll, fg_color="transparent")
            btn_container.pack(fill="x", padx=10, pady=5)
            
            btn = ModernButton(
                btn_container,
                text=btn_config["text"],
                command=btn_config["command"],
                fg_color=btn_config["color"],
                hover_color=self.lighten_color(btn_config["color"]),
                font=("Segoe UI", 14, "bold"),
                anchor="w",
                height=55
            )
            btn.pack(fill="x")
            
            self.create_tooltip(btn, btn_config["description"])
            
            self.button_widgets.append(btn)
            
    def create_tooltip(self, widget, text):

        def enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.configure(bg=ColorTheme.CARD_BG)
            
            label = tk.Label(
                tooltip,
                text=text,
                bg=ColorTheme.CARD_BG,
                fg=ColorTheme.TEXT_PRIMARY,
                font=("Segoe UI", 10),
                padx=10,
                pady=5
            )
            label.pack()
            
            x = widget.winfo_rootx() + widget.winfo_width() + 10
            y = widget.winfo_rooty() + widget.winfo_height() // 2
            tooltip.geometry(f"+{x}+{y}")
            
            widget.tooltip = tooltip
            
        def leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
        
    def lighten_color(self, color):

        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        lighter_rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
        return f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"
        
    def create_main_content(self):

        self.main_frame = ctk.CTkFrame(
            self, 
            fg_color=ColorTheme.CARD_BG,
            corner_radius=15
        )
        self.main_frame.grid(row=1, column=1, sticky="nsew", padx=15, pady=15)
        self.main_frame.grid_propagate(True)
        
    def toggle_sidebar(self):

        if self.sidebar_expanded:
            self.sidebar_frame.grid_remove()
            self.sidebar_expanded = False
            self.toggle_btn.configure(text="☰")
        else:
            self.sidebar_frame.grid(row=1, column=0, sticky="ns")
            self.sidebar_expanded = True
            self.toggle_btn.configure(text="✕")
            
    def clear_main_content(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
    def load_initial_page(self):

        self.abrir_inicio()
        
    def abrir_inicio(self):
        self.clear_main_content()
        self.current_page = MenuPage(self.main_frame)
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_matrices(self):
        self.clear_main_content()
        self.current_page = MatricesPage(self.main_frame)
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_polinomios(self):
        self.clear_main_content()
        self.current_page = PolinomiosPage(self.main_frame)
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_vectors(self):
        self.clear_main_content()
        self.current_page = VectoresPage(self.main_frame)
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_graficas_2d(self):
        self.clear_main_content()
        self.current_page = Graficas2DPage(self.main_frame)
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_graficas_3d(self):
        self.clear_main_content()
        self.current_page = Graficas3DPage(self.main_frame)
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_calculo(self):
        self.clear_main_content()
        self.current_page = CalculoPage(self.main_frame)
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_sistema_ecuaciones_lineales(self):
        self.clear_main_content()
        self.current_page = EcuacionesDiferencialesUI(self.main_frame)
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_sistemaEDO(self):
        self.clear_main_content()
        self.current_page = SistemaDiferencialPage(self.main_frame)
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_distribuciones(self):
        self.clear_main_content()
        self.current_page = DistribucionesPage(self.main_frame)
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_sir(self):
        self.clear_main_content()
        self.current_page = AgriculturaApp(self.main_frame)
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_acerca_de(self):
        self.clear_main_content()
        self.current_page = AcercaDePage(self.main_frame)
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)


class ModernSplashScreen(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)
        self.setup_window()
        self.create_content()
        self.start_animation()
        
    def setup_window(self):

        self.geometry("600x400")
        self.overrideredirect(True)
        self.configure(fg_color=ColorTheme.PRIMARY_BG)
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        self.geometry(f"600x400+{x}+{y}")
        
        self.lift()
        self.focus_force()
        
    def create_content(self):

        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=40)

        try:
            logo_image = ctk.CTkImage(Image.open("assets/logo2.png"), size=(120, 120))
            self.logo_label = ctk.CTkLabel(main_container, image=logo_image, text="")
            try:
                self.iconbitmap("assets/logo2.ico")
            except Exception:
                pass
        except:
            self.logo_label = ctk.CTkLabel(
                main_container, 
                text="🧠", 
                font=("Arial", 80), 
                text_color=ColorTheme.ACCENT_PRIMARY
            )
        self.logo_label.pack(pady=(30, 20))

        title_label = ctk.CTkLabel(
            main_container,
            text="ModelaMath",
            font=("Segoe UI", 32, "bold"),
            text_color=ColorTheme.TEXT_PRIMARY
        )
        title_label.pack(pady=(0, 10))

        subtitle_label = ctk.CTkLabel(
            main_container,
            text="Calculadora Científica Avanzada",
            font=("Segoe UI", 16),
            text_color=ColorTheme.TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(0, 30))
        
        self.progress_bar = ctk.CTkProgressBar(
            main_container,
            width=400,
            height=8,
            fg_color=ColorTheme.BORDER_DEFAULT,
            progress_color=ColorTheme.ACCENT_PRIMARY
        )
        self.progress_bar.pack(pady=(0, 20))
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            main_container,
            text="Iniciando aplicación...",
            font=("Segoe UI", 12),
            text_color=ColorTheme.TEXT_MUTED
        )
        self.status_label.pack()
        
    def start_animation(self):
        self.progress = 0
        self.update_progress()
        
    def update_progress(self):

        if self.progress < 1.0:
            self.progress += 0.02
            self.progress_bar.set(self.progress)
    
            if self.progress < 0.3:
                self.status_label.configure(text="Cargando módulos...")
            elif self.progress < 0.6:
                self.status_label.configure(text="Inicializando componentes...")
            elif self.progress < 0.9:
                self.status_label.configure(text="Preparando interfaz...")
            else:
                self.status_label.configure(text="¡Listo!")
                
            self.after(50, self.update_progress)
        else:
            self.after(500, self.close_splash)
            
    def close_splash(self):

        self.master.state("zoomed")
        self.master.deiconify()
        self.destroy()


def main():
    try:
        app = MenuPrincipal()
        app.withdraw() 
        splash = ModernSplashScreen(app)
        app.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")

if __name__ == "__main__":
    main()