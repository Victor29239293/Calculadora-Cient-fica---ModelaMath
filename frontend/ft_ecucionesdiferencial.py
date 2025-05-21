import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
from typing import List, Dict, Any, Tuple, Optional
import logging
from PIL import Image, ImageTk
import os
import math
import io

from backend.Ecuaciones_Diferenciales.bk_ecuaciones_Diferenciales import (
    euler_method, heun_method, rk4_method,
    taylor2_method, analytic_solver
)
from backend.Ecuaciones_Diferenciales.gestor_resultado import ResultadosEDOManager
from backend.Ecuaciones_Diferenciales.minimo_cuadrado import MinimosCuadrados
from backend.Ecuaciones_Diferenciales.graficasEDO import mostrar_grafica
from frontend.utils.utils_labels import guardar_resultado_metodo


def latex_to_image(latex_str, fontsize=18, dpi=120, color="black", bg="white"):
    """Renderiza una cadena LaTeX a una imagen PIL y retorna el objeto PhotoImage para Tkinter."""
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, f" Soolucion Analitica${latex_str}$", fontsize=fontsize, color=color)
    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, dpi=dpi, transparent=False, facecolor=bg)
    plt.close(fig)
    buf.seek(0)
    pil_img = Image.open(buf)
    return ImageTk.PhotoImage(pil_img)


class EcuacionesDiferencialesUI(ctk.CTkFrame):
    """
    Interfaz de usuario para resolver EDOs con métodos numéricos, Taylor, solución analítica,
    ajuste por mínimos cuadrados y comparación de métodos.
    """
    NUMERIC_METHODS = ["euler", "heun", "rk4"]
    EXAMPLES: Dict[str, List[str]] = {
        "euler": ["x + y", "x*y", "x**2 - y"],
        "heun":  ["sin(x) + y", "x - y", "x*y + 1"],
        "rk4":   ["y/x", "x**2 + y**2", "exp(x) - y"]
    }
    METHOD_COLORS = {
        "EULER": "#3498db",     # Azul
        "HEUN": "#2ecc71",      # Verde
        "RK4": "#e74c3c",       # Rojo
        "TAYLOR2": "#9b59b6",   # Morado
        "ANALYTIC": "#f39c12"   # Naranja
    }
    DEFAULT_COLOR = "#101117"   # Gris para métodos no especificados

    def __init__(self, master):
        super().__init__(master)
        
        # Configuración de temas y apariencia
        ctk.set_appearance_mode("dark")  # Modo oscuro para una apariencia moderna
        ctk.set_default_color_theme("blue")
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("EDO_UI")

        self.canvases: Dict[str, Any] = {}
        self.current_tab = ""
        self.chk_vars: List[Tuple[str, ctk.BooleanVar]] = []
        
        # Gestor de resultados para mantener historial de cálculos
        self.results_manager = ResultadosEDOManager()
        
        # Configuración de estilos gráficos
        plt.style.use('dark_background')
        
        # Configurar layout principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content
        
        # Header con logo y título
        self._create_header()
        
        # Crear tabview mejorado
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=15, pady=(5, 15))
        
        self._configure_styles()
        self._create_tabs()
        self.after(200, self._watch_tab_change)

    def _create_fancy_inputs(self, parent: ctk.CTkFrame, method: str) -> None:
        """Crear entradas de formulario con mejor diseño"""
        form_fields = ctk.CTkFrame(parent, fg_color="transparent")
        form_fields.pack(fill="x", padx=20, pady=10)
        
        # Entrada para la función
        field_frame = ctk.CTkFrame(form_fields, fg_color="transparent")
        field_frame.pack(fill="x", pady=(0, 10))
        
        func_label = ctk.CTkLabel(
            field_frame, 
            text="y'=f(x,y)",
            width=60,
            font=ctk.CTkFont(size=13)
        )
        func_label.pack(side="left", padx=(5, 10))
        
        entry_f = ctk.CTkEntry(field_frame, placeholder_text="Ingrese la función")
        entry_f.pack(side="left", fill="x", expand=True)
        setattr(self, f"entry_f_{method}", entry_f)
        
        # Panel para parámetros iniciales
        params_frame = ctk.CTkFrame(form_fields, fg_color=("gray80", "gray16"), corner_radius=6)
        params_frame.pack(fill="x", pady=(0, 5))
        
        params_title = ctk.CTkLabel(
            params_frame,
            text="Parámetros Iniciales",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        params_title.pack(anchor="w", padx=10, pady=(5, 0))
        
        # Grid para parámetros con dos columnas
        params_grid = ctk.CTkFrame(params_frame, fg_color="transparent")
        params_grid.pack(fill="x", padx=10, pady=(0, 5))
        params_grid.grid_columnconfigure(0, weight=1)
        params_grid.grid_columnconfigure(1, weight=1)
        
        # x0, y0
        self._create_param_entry(params_grid, "x₀", f"entry_x0_{method}", 0, 0, "Valor inicial x")
        self._create_param_entry(params_grid, "y₀", f"entry_y0_{method}", 0, 1, "Valor inicial y")
        
        # h, n
        self._create_param_entry(params_grid, "h", f"entry_h_{method}", 1, 0, "Tamaño de paso")
        self._create_param_entry(params_grid, "n", f"entry_n_{method}", 1, 1, "Número de pasos")

    def _create_param_entry(self, parent, label, attr_name, row, col, placeholder):
        """Crear una entrada de parámetro individual"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        lbl = ctk.CTkLabel(frame, text=label, width=30)
        lbl.pack(side="left", padx=(5, 5))
        
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
        entry.pack(side="left", fill="x", expand=True)
        setattr(self, attr_name, entry)

    def _create_header(self) -> None:
        """Crear header con logo y título"""
        header_frame = ctk.CTkFrame(self, fg_color=("gray85", "gray20"), corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        
        # Título con fuente grande y elegante
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Solucionador de Ecuaciones Diferenciales",
            font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"),text_color="#6c63ff"
        )
        title_label.pack(pady=10)
        
        # Subtítulo descriptivo
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Métodos numéricos, analíticos y aproximaciones",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=("gray40", "gray70")
        )
        subtitle.pack(pady=(0, 10))
        
    def _configure_styles(self) -> None:
        """Configurar estilos para elementos ttk"""
        style = ttk.Style()
        
        # Estilo para las tablas de resultados
        style.configure(
            "EDO.Treeview", 
            rowheight=28,
            background="#2d3436",
            foreground="#ecf0f1",
            fieldbackground="#2d3436"
        )
        style.map("EDO.Treeview", 
            background=[('selected', '#16a085')],
            foreground=[('selected', '#ecf0f1')]
        )
        
        # Estilo para los encabezados de tabla
        style.configure(
            "EDO.Treeview.Heading",
            background="#34495e",
            foreground="#ecf0f1",
            relief="flat"
        )
        style.map("EDO.Treeview.Heading",
            background=[('active', '#2c3e50')],
            foreground=[('active', '#ffffff')]
        )

    def _create_tabs(self) -> None:
        """Crear todas las pestañas de la aplicación"""
        # Métodos numéricos
        for m in self.NUMERIC_METHODS:
            self._add_numeric_tab(m)
        # Taylor
        self._add_taylor_tab()
        # Analítica
        self._add_analytic_tab()
        # Mínimos cuadrados
        self._add_minimos_tab()
        # Comparativa
        self._add_comparative_tab()

    def _add_numeric_tab(self, method: str) -> None:
        """Crear pestaña para método numérico específico"""
        self.tabview.add(method.capitalize())
        tab = self.tabview.tab(method.capitalize())
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        # Scroll en todo el contenido
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True)
        scroll_frame.grid_columnconfigure(0, weight=1)
        scroll_frame.grid_columnconfigure(1, weight=1)
        scroll_frame.grid_rowconfigure(0, weight=1)

        # Ahora usa scroll_frame en vez de tab para tus frames hijos
        # Ejemplo:
        form_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        form_frame.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)
        
        results_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        results_frame.pack(side="right", fill="both", expand=True, padx=(10, 5), pady=10)

        # Header de pestaña
        header_frame = ctk.CTkFrame(form_frame, fg_color=("gray85", "gray20"), corner_radius=10)
        header_frame.pack(fill="x")
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text=f"Parámetros {method.capitalize()}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=10, pady=10)
        
        # Ícono del método
        icon_path = os.path.join(os.path.dirname(__file__), f"icons/{method}.png")
        if os.path.isfile(icon_path):
            img = Image.open(icon_path)
            img = img.resize((24, 24), Image.ANTIALIAS)
            icon = ImageTk.PhotoImage(img)
            
            icon_label = ctk.CTkLabel(
                header_frame,
                image=icon,
                text="",
                width=24,
                height=24,
                corner_radius=12
            )
            icon_label.image = icon  # Guardar referencia para evitar recolección de basura
            icon_label.pack(side="left", padx=(10, 5))
        
        # Separador
        separator = ctk.CTkFrame(form_frame, height=2, fg_color=("gray70", "gray30"))
        separator.pack(fill="x", padx=20, pady=10)
        
        # Entradas
        self._create_fancy_inputs(form_frame, method)
        
        # Ejemplos agrupados
        example_frame = ctk.CTkFrame(form_frame, fg_color=("gray85", "gray17"), corner_radius=6)
        example_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        example_label = ctk.CTkLabel(example_frame, text="Ejemplos:", font=ctk.CTkFont(weight="bold"))
        example_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        var = ctk.StringVar(value=self.EXAMPLES[method][0])
        setattr(self, f"example_var_{method}", var)
        menu = ctk.CTkOptionMenu(
            example_frame, 
            variable=var, 
            values=self.EXAMPLES[method],
            width=200,
            dynamic_resizing=False
        )
        menu.pack(padx=10, pady=5)
        
        cargar_btn = ctk.CTkButton(
            example_frame, 
            text="Cargar Ejemplo",
            command=lambda m=method: self._load_example(m),
            fg_color="#16a085",
            hover_color="#1abc9c"
        )
        cargar_btn.pack(padx=10, pady=(5, 10), fill="x")

        # Botón aplicar
        btn = ctk.CTkButton(
            form_frame, 
            text=f"Aplicar {method.capitalize()}",
            command=lambda m=method: self._run_numeric(m),
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self._get_method_color(method.upper()),
            hover_color=self._darken_color(self._get_method_color(method.upper()))
        )
        btn.pack(pady=20, padx=20, fill="x")

        # Panel derecho - Resultados
        # results_frame = ctk.CTkFrame(tab, corner_radius=10)
        # results_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 5), pady=10)
        
        results_title = ctk.CTkLabel(
            results_frame, 
            text="Resultados",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        results_title.pack(pady=(15, 10))
        
        # Resultados
        tree_frame = ctk.CTkFrame(results_frame)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        # Encabezado de tabla
        table_title = ctk.CTkLabel(
            tree_frame,
            text="Tabla de Valores",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        table_title.pack(anchor="w", pady=(5, 5))
        
        setattr(self, f"tree_{method}", self._create_treeview(tree_frame))
        
        # Gráfica
        plot_label = ctk.CTkLabel(
            results_frame,
            text="Gráfica de Solución",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        plot_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Frame para gráfica SOLO para Euler con scroll
        if method == "euler":
            plot_frame = ctk.CTkScrollableFrame(results_frame, fg_color=("gray80", "gray20"))
        else:
            plot_frame = ctk.CTkFrame(results_frame, fg_color=("gray80", "gray20"))
        plot_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        setattr(self, f"plot_frame_{method}", plot_frame)
        
        self.canvases[method] = None

    def _add_taylor_tab(self) -> None:
        """Crear pestaña para el método de Taylor con scroll en toda la página"""
        tab = self.tabview.add("Taylor2")

        # 1) Configuramos la grilla de la pestaña principal para que el scrollable ocupe todo el espacio
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        # 2) Creamos el scrollable que contendrá ambos paneles
        scrollable = ctk.CTkScrollableFrame(
            tab,
            corner_radius=10,
            scrollbar_fg_color="gray40",
            scrollbar_button_color="gray60"
        )
        scrollable.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Hacemos que dentro del scrollable haya dos columnas de igual peso
        scrollable.grid_columnconfigure(0, weight=1)
        scrollable.grid_columnconfigure(1, weight=1)

        # — Panel izquierdo — (configuración)
        form_frame = ctk.CTkFrame(scrollable, corner_radius=10)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        # Título y descripción
        ctk.CTkLabel(
            form_frame,
            text="Método de Taylor (2° Orden)",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        ctk.CTkLabel(
            form_frame,
            text=(
                "El método de Taylor de segundo orden utiliza la expansión "
                "en serie de Taylor para obtener una aproximación más precisa "
                "incluyendo el término de segunda derivada."
            ),
            font=ctk.CTkFont(size=12),
            wraplength=260,
            justify="center"
        ).pack(pady=(0, 15), padx=10)

        # Separador
        ctk.CTkFrame(form_frame, height=2, fg_color=("gray70","gray30")).pack(fill="x", padx=10, pady=10)

        # Campos del formulario
        fields = [
            ("f(x,y)", "entry_f_taylor", "Función principal"),
            ("f'(x,y)", "entry_df_taylor", "Primera derivada"),
            ("x₀",      "entry_x0_t2",    "Valor inicial de x"),
            ("y₀",      "entry_y0_t2",    "Valor inicial de y"),
            ("xf",      "entry_xf_t2",    "Valor final de x"),
            ("n pasos","entry_n_t2",     "Número de pasos"),
        ]
        for label_text, attr, placeholder in fields:
            row = ctk.CTkFrame(form_frame, fg_color="transparent")
            row.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(row, text=label_text, width=60, font=ctk.CTkFont(size=13)).pack(side="left")
            entry = ctk.CTkEntry(row, placeholder_text=placeholder)
            entry.pack(side="left", fill="x", expand=True)
            setattr(self, attr, entry)

        # Botón de ejecución
        ctk.CTkButton(
            form_frame,
            text="Aplicar Taylor 2° Orden",
            command=self._run_taylor2,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self._get_method_color("TAYLOR2"),
            hover_color=self._darken_color(self._get_method_color("TAYLOR2"))
        ).pack(fill="x", padx=10, pady=(15,20))

        # — Panel derecho — (resultados y gráfica)
        results_frame = ctk.CTkFrame(scrollable, corner_radius=10)
        results_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

        # Título resultados
        ctk.CTkLabel(
            results_frame,
            text="Resultados",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15,10))

        # Tabla
        table_container = ctk.CTkFrame(results_frame)
        table_container.pack(fill="both", expand=True, padx=10, pady=5)
        ctk.CTkLabel(
            table_container,
            text="Tabla de Valores",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", pady=(0,5))
        self.tree_taylor2 = self._create_treeview(table_container)

        # Gráfica
        ctk.CTkLabel(
            results_frame,
            text="Gráfica de Solución",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=10, pady=(15,5))
        plot_frame = ctk.CTkFrame(results_frame, fg_color=("gray80","gray20"))
        plot_frame.pack(fill="both", expand=True, padx=10, pady=(0,15))
        setattr(self, "plot_frame_taylor2", plot_frame)
        self.canvases["taylor2"] = None


    def _add_analytic_tab(self) -> None:
        """Crear pestaña para solución analítica"""
        tab = self.tabview.add("Analítica")
        
        # División en paneles
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        
        # Panel principal
        # Panel principal con scroll vertical
        main_frame = ctk.CTkScrollableFrame(tab, corner_radius=10)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=10)
        
        title = ctk.CTkLabel(
            main_frame, 
            text="Solución Analítica",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(15, 5))
        
        # Descripción del método
        desc = "Resuelve la ecuación diferencial analíticamente usando técnicas simbólicas. "\
               "Proporciona una solución exacta cuando es posible."
        desc_label = ctk.CTkLabel(
            main_frame,
            text=desc,
            font=ctk.CTkFont(size=12),
            wraplength=400,
            justify="center"
        )
        desc_label.pack(pady=(0, 15), padx=20)
        
        # Panel de entradas
        input_frame = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray17"), corner_radius=8)
        input_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        input_title = ctk.CTkLabel(
            input_frame,
            text="Ecuación Diferencial",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        input_title.pack(pady=(10, 5))
        
        # Formulario de entradas
        form_fields = ctk.CTkFrame(input_frame, fg_color="transparent")
        form_fields.pack(fill="x", padx=20, pady=10)
        form_fields.grid_columnconfigure(0, weight=1)
        form_fields.grid_columnconfigure(1, weight=1)

        inputs = [
            ("Ecuación (y''...)", "entry_ecuacion", "Ejemplo: y'' + 4*y' + 4*y = 0"),
            ("x₀ (opcional)", "entry_x0_a", "Valor inicial de x"),
            ("y₀ (opcional)", "entry_y0_a", "Valor inicial de y"),
            ("y'(x₀) (opcional)", "entry_dy0_a", "Derivada inicial")
        ]

        for i, (label, attr, placeholder) in enumerate(inputs):
            row, col = divmod(i, 2)
            field_frame = ctk.CTkFrame(form_fields, fg_color="transparent")
            field_frame.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
            field_label = ctk.CTkLabel(
                field_frame, 
                text=label,
                width=90,
                anchor="w",
                font=ctk.CTkFont(size=12)
            )
            field_label.pack(side="left", padx=(5, 5))
            entry = ctk.CTkEntry(field_frame, placeholder_text=placeholder, width=140)
            entry.pack(side="left", fill="x", expand=True)
            setattr(self, attr, entry)
        # Panel de botones
        btn_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        solve_btn = ctk.CTkButton(
            btn_frame, 
            text="Resolver Analíticamente",
            command=self._run_analytic,
            height=35,
            fg_color=self._get_method_color("ANALYTIC"),
            hover_color=self._darken_color(self._get_method_color("ANALYTIC"))
        )
        solve_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        clear_btn = ctk.CTkButton(
            btn_frame, 
            text="Limpiar",
            command=self._clear_analytic,
            height=35,
            fg_color="#7f8c8d",
            hover_color="#95a5a6"
        )
        clear_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Panel de resultados con borde
        result_container = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray17"), corner_radius=8)
        result_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        result_title = ctk.CTkLabel(
            result_container,
            text="Resultados",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        result_title.pack(pady=(10, 5))
        
        # La solución se mostrará aquí
        self.result_scroll = ctk.CTkScrollableFrame(result_container, fg_color="transparent")
        self.result_scroll.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        self.solution_label = ctk.CTkLabel(
            self.result_scroll, 
            text="",
            wraplength=550,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        self.solution_label.pack(pady=5, padx=10, anchor="w")

    def _add_minimos_tab(self) -> None:
        """Crear pestaña para mínimos cuadrados"""
        tab = self.tabview.add("Mínimos Cuadrados")
        
        # División en paneles
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        
        # Panel principal
        main_frame = ctk.CTkScrollableFrame(tab, corner_radius=10)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=10)

        
        title = ctk.CTkLabel(
            main_frame, 
            text="Ajuste por Mínimos Cuadrados",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(15, 5))
        
        # Descripción del método
        desc = "Ajusta los resultados de un método numérico mediante regresión lineal "\
               "para determinar una aproximación lineal de la solución."
        desc_label = ctk.CTkLabel(
            main_frame,
            text=desc,
            font=ctk.CTkFont(size=12),
            wraplength=400,
            justify="center"
        )
        desc_label.pack(pady=(0, 15), padx=20)
        
        # Panel de entradas
        input_frame = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray17"), corner_radius=8)
        input_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        input_title = ctk.CTkLabel(
            input_frame,
            text="Seleccionar Método",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        input_title.pack(pady=(10, 5))
        
        # Selector de método
        method_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        method_frame.pack(fill="x", padx=20, pady=10)
        
        self.var_min = ctk.StringVar()
        self.menu_min = ctk.CTkOptionMenu(
            method_frame, 
            variable=self.var_min, 
            values=[],
            width=200,
            dynamic_resizing=False
        )
        self.menu_min.pack(side="left", padx=(0, 10))
        
        fit_btn = ctk.CTkButton(
            method_frame, 
            text="Realizar Ajuste Lineal",
            command=self._run_minimos,
            height=30,
            fg_color="#2980b9",
            hover_color="#3498db"
        )
        fit_btn.pack(side="left", fill="x", expand=True)
        
        # Panel de resultados
        result_frame = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray17"), corner_radius=8)
        result_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        result_title = ctk.CTkLabel(
            result_frame,
            text="Resultados del Ajuste",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        result_title.pack(pady=(10, 5))
        
        # Resultados numéricos
        self.result_min = ctk.CTkTextbox(result_frame, height=80, corner_radius=5)
        self.result_min.pack(fill="x", padx=15, pady=10)
        
        # Gráfica del ajuste
        plot_title = ctk.CTkLabel(
            result_frame,
            text="Gráfica del Ajuste",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        plot_title.pack(anchor="w", padx=15, pady=(10, 5))

        # Cambia esta línea:
        # self.frame_plot_min = ctk.CTkFrame(result_frame, fg_color=("gray80", "gray20"))
        # Por esta:
        self.frame_plot_min = ctk.CTkFrame(result_frame, fg_color=("gray80", "gray20"))
        self.frame_plot_min.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        

    def _get_method_description(self, method: str) -> str:
        """Devuelve una breve descripción del método numérico."""
        descs = {
            "euler": "Método de Euler: Aproxima la solución de EDOs usando incrementos lineales.",
            "heun": "Método de Heun: Promedia la pendiente inicial y final para mayor precisión.",
            "rk4": "Runge-Kutta 4° orden: Método clásico de alta precisión para EDOs.",
        }
        return descs.get(method.lower(), "Método numérico para EDOs.")
    
    def _get_method_color(self, method: str) -> str:
        """Devuelve el color asociado a un método."""
        return self.METHOD_COLORS.get(method.upper(), self.DEFAULT_COLOR)
    
    def _darken_color(self, hex_color: str, factor: float = 0.8) -> str:
        """
        Devuelve una versión más oscura del color hexadecimal dado.
        factor < 1 oscurece, factor > 1 aclara.
        """
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        dark_rgb = tuple(max(0, int(c * factor)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*dark_rgb)

    def _create_treeview(self, parent):
        """
        Crea y retorna un ttk.Treeview con estilos personalizados para mostrar resultados numéricos.
        """
        columns = ("x", "y")
        tree = ttk.Treeview(parent, columns=columns, show="headings", style="EDO.Treeview")
        tree.heading("x", text="x")
        tree.heading("y", text="y")
        tree.column("x", anchor="center", width=80)
        tree.column("y", anchor="center", width=120)
        tree.pack(fill="both", expand=True)
        return tree

    def _run_taylor2(self):
        """Ejecuta el método de Taylor de segundo orden y muestra los resultados."""
        try:
            f_str = self.entry_f_taylor.get()
            df_str = self.entry_df_taylor.get()
            x0 = float(self.entry_x0_t2.get())
            y0 = float(self.entry_y0_t2.get())
            xf = float(self.entry_xf_t2.get())
            n = int(self.entry_n_t2.get())

            # Llama al método de backend
            xs, ys = taylor2_method(f_str, df_str, x0, y0, xf, n)

            # Limpia la tabla
            for item in self.tree_taylor2.get_children():
                self.tree_taylor2.delete(item)
            # Inserta los resultados
            for x, y in zip(xs, ys):
                self.tree_taylor2.insert("", "end", values=(f"{x:.6g}", f"{y:.6g}"))

            # --- Agrega este bloque para graficar ---
            plot_frame = getattr(self, "plot_frame_taylor2")
            for widget in plot_frame.winfo_children():
                widget.destroy()
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(xs, ys, marker="o", color=self._get_method_color("TAYLOR2"))
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title("Solución por Taylor 2° Orden")
            ax.grid(True)
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            # --- Fin del bloque de graficado ---

        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error en Taylor 2° Orden:\n{e}", icon="cancel")

    def _run_analytic(self):
        """Resuelve la ecuación diferencial analíticamente y muestra el resultado."""
        try:
            eq_str = self.entry_ecuacion.get()
            x0 = self.entry_x0_a.get()
            y0 = self.entry_y0_a.get()
            dy0 = self.entry_dy0_a.get()

            # Prepara condiciones iniciales si están presentes
            condiciones = []
            if x0:
                condiciones.append(float(x0))
                if y0:
                    condiciones.append(float(y0))
                if dy0:
                    condiciones.append(float(dy0))

            # Llama al backend
            sol = analytic_solver(eq_str, condiciones if condiciones else None)

            # Manejo de error del backend
            if isinstance(sol, dict) and not sol.get("exito", True):
                self.solution_label.configure(text=f"Error: {sol['mensaje']}")
                return

            # Formatea el resultado de manera bonita
            try:
                latex_str = sp.latex(sol.rhs if hasattr(sol, "rhs") else sol)
            except Exception:
                latex_str = str(sol)

            # Limpia el área de resultados (solo widgets previos, no la gráfica)
            for widget in self.result_scroll.winfo_children():
                widget.destroy()

            # Renderiza el resultado como imagen
            try:
                img = latex_to_image(latex_str, fontsize=18)
                img_label = ctk.CTkLabel(self.result_scroll, image=img, text="")
                img_label.image = img  # Guarda referencia para evitar que se borre
                img_label.pack(anchor="w", padx=10, pady=10)
            except Exception as e:
                # Si falla, muestra el resultado como texto plano
                result_label = ctk.CTkLabel(self.result_scroll, text=f"Solución: {latex_str}", font=ctk.CTkFont(size=14))
                result_label.pack(anchor="w", padx=10, pady=10)

            # Graficar la solución analítica si es posible
            try:
                # Elimina solo la gráfica previa (si existe)
                for widget in self.result_scroll.winfo_children():
                    if isinstance(widget, FigureCanvasTkAgg):
                        widget.get_tk_widget().destroy()

                x = sp.symbols('x')
                expr = sol.rhs if hasattr(sol, "rhs") else sol

                # Verifica si hay constantes arbitrarias en la expresión
                constantes = [s for s in expr.free_symbols if str(s).startswith("C")]
                if constantes:
                    error_label = ctk.CTkLabel(
                        self.result_scroll,
                        text="No se puede graficar la solución general (contiene constantes arbitrarias).",
                        font=ctk.CTkFont(size=12)
                    )
                    error_label.pack(anchor="w", padx=10, pady=5)
                else:
                    import numpy as np
                    x_vals = np.linspace(-5, 5, 200)
                    f_lambdified = sp.lambdify(x, expr, modules=["numpy"])
                    y_vals = f_lambdified(x_vals)

                    fig, ax = plt.subplots(figsize=(6, 3))
                    ax.plot(x_vals, y_vals, label="Solución Analítica", color="#f39c12")
                    ax.set_xlabel("x")
                    ax.set_ylabel("y(x)")
                    ax.set_title("Gráfica de la Solución Analítica")
                    ax.grid(True)
                    ax.legend()
                    fig.tight_layout()

                    canvas = FigureCanvasTkAgg(fig, master=self.result_scroll)
                    canvas.draw()
                    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            except Exception as e:
                error_label = ctk.CTkLabel(self.result_scroll, text=f"No se pudo graficar la solución: {e}", font=ctk.CTkFont(size=12))
                error_label.pack(anchor="w", padx=10, pady=5)

        except Exception as e:
            for widget in self.result_scroll.winfo_children():
                widget.destroy()
            error_label = ctk.CTkLabel(self.result_scroll, text=f"Error: {e}", font=ctk.CTkFont(size=14, weight="bold"))
            error_label.pack(anchor="w", padx=10, pady=10)

    def _clear_analytic(self):
        """Limpia los campos y el resultado de la pestaña analítica."""
        self.entry_ecuacion.delete(0, "end")
        self.entry_x0_a.delete(0, "end")
        self.entry_y0_a.delete(0, "end")
        self.entry_dy0_a.delete(0, "end")
        self.solution_label.configure(text="")

    def _run_minimos(self):
        """Ejecuta el ajuste por mínimos cuadrados y muestra los resultados."""
        try:
            metodo = self.var_min.get()
            if not metodo:
                CTkMessagebox(title="Error", message="Selecciona un método numérico para ajustar.", icon="cancel")
                return

            # Obtiene los datos del método seleccionado
            tree = getattr(self, f"tree_{metodo}", None)
            if tree is None:
                CTkMessagebox(title="Error", message="No hay resultados para ajustar.", icon="cancel")
                return

            xs, ys = [], []
            for item in tree.get_children():
                x, y = tree.item(item, "values")
                xs.append(float(x))
                ys.append(float(y))

            if not xs or not ys:
                CTkMessagebox(title="Error", message="No hay datos para ajustar.", icon="cancel")
                return

            # Realiza el ajuste lineal
            minimos = MinimosCuadrados()
            resultado = minimos.ajustar_lineal(xs, ys)
            pendiente = resultado["a"]
            intercepto = resultado["b"]

            self.result_min.delete("0.0", "end")
            self.result_min.insert("end", f"Ecuación de ajuste:\ny = {pendiente:.4f}x + {intercepto:.4f}\n")

            # Si tienes una función para graficar, pásale los datos del resultado:
            fig = minimos.graficar_ajuste(resultado["xs"], resultado["ys_originales"], resultado["ys_ajustados"])
            for widget in self.frame_plot_min.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(fig, master=self.frame_plot_min)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error en mínimos cuadrados:\n{e}", icon="cancel")

    def _add_comparative_tab(self) -> None:
        """Crear pestaña para comparar métodos numéricos."""
        self.tabview.add("Comparativa")
        tab = self.tabview.tab("Comparativa")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(tab, corner_radius=10)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=10)

        title = ctk.CTkLabel(
            main_frame,
            text="Comparar Métodos Numéricos",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(15, 5))

        desc = "Selecciona uno o más métodos numéricos para comparar sus soluciones en una misma gráfica."
        desc_label = ctk.CTkLabel(
            main_frame,
            text=desc,
            font=ctk.CTkFont(size=12),
            wraplength=500,
            justify="center"
        )
        desc_label.pack(pady=(0, 15), padx=20)

        # Menú de selección múltiple
        self.comp_methods_vars = {}
        menu_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        menu_frame.pack(pady=(0, 10))
        for m in self.NUMERIC_METHODS:
            var = ctk.BooleanVar(value=True if m == "euler" else False)
            chk = ctk.CTkCheckBox(menu_frame, text=m.capitalize(), variable=var)
            chk.pack(side="left", padx=10)
            self.comp_methods_vars[m] = var

        # Botón para comparar
        btn = ctk.CTkButton(
            main_frame,
            text="Comparar Métodos",
            command=self._run_comparative,
            fg_color="#f39c12",
            hover_color="#e67e22"
        )
        btn.pack(pady=10)

        # Frame para la gráfica comparativa
        self.frame_plot_comp = ctk.CTkFrame(main_frame, fg_color=("gray80", "gray20"))
        self.frame_plot_comp.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _watch_tab_change(self):
        """Detecta el cambio de pestaña y actualiza menús o gráficos si es necesario."""
        # Ejemplo: actualizar el menú de métodos disponibles para mínimos cuadrados
        if hasattr(self, "menu_min"):
            disponibles = []
            for m in self.NUMERIC_METHODS:
                tree = getattr(self, f"tree_{m}", None)
                if tree is not None and len(tree.get_children()) > 0:
                    disponibles.append(m)
            self.menu_min.configure(values=disponibles)
            if disponibles and not self.var_min.get():
                self.var_min.set(disponibles[0])
        # Puedes agregar aquí más lógica si necesitas reaccionar a cambios de pestaña
        self.after(500, self._watch_tab_change)

    def _run_numeric(self, method: str):
        """Ejecuta el método numérico seleccionado y muestra los resultados."""
        try:
            # Obtiene los parámetros de entrada
            f_str = getattr(self, f"entry_f_{method}").get()
            x0 = float(getattr(self, f"entry_x0_{method}").get())
            y0 = float(getattr(self, f"entry_y0_{method}").get())
            h = float(getattr(self, f"entry_h_{method}").get())
            n = int(getattr(self, f"entry_n_{method}").get())

            # Llama al método correspondiente del backend
            if method == "euler":
                xs, ys = euler_method(f_str, x0, y0, h, n)
            elif method == "heun":
                xs, ys = heun_method(f_str, x0, y0, h, n)
            elif method == "rk4":
                xs, ys = rk4_method(f_str, x0, y0, h, n)
            else:
                CTkMessagebox(title="Error", message="Método no soportado.", icon="cancel")
                return

            # Limpia la tabla
            tree = getattr(self, f"tree_{method}")
            for item in tree.get_children():
                tree.delete(item)
            # Inserta los resultados
            for x, y in zip(xs, ys):
                tree.insert("", "end", values=(f"{x:.6g}", f"{y:.6g}"))

            # Graficar resultados
            plot_frame = getattr(self, f"plot_frame_{method}")
            for widget in plot_frame.winfo_children():
                widget.destroy()
            fig, ax = plt.subplots(figsize=(7, 4))  # Proporción más natural
            ax.plot(xs, ys, marker="o", color=self._get_method_color(method.upper()))
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title(f"Solución por {method.capitalize()}")
            ax.grid(True)
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error en {method.capitalize()}:\n{e}", icon="cancel")

    def _load_example(self, method: str):
        """Carga un ejemplo predefinido en los campos de entrada del método numérico."""
        example = getattr(self, f"example_var_{method}").get()
        getattr(self, f"entry_f_{method}").delete(0, "end")
        getattr(self, f"entry_f_{method}").insert(0, example)
        # Puedes poner valores por defecto para los otros campos si lo deseas
        getattr(self, f"entry_x0_{method}").delete(0, "end")
        getattr(self, f"entry_x0_{method}").insert(0, "0")
        getattr(self, f"entry_y0_{method}").delete(0, "end")
        getattr(self, f"entry_y0_{method}").insert(0, "1")
        getattr(self, f"entry_h_{method}").delete(0, "end")
        getattr(self, f"entry_h_{method}").insert(0, "0.1")
        getattr(self, f"entry_n_{method}").delete(0, "end")
        getattr(self, f"entry_n_{method}").insert(0, "10")

    def _run_comparative(self):
        """Grafica la comparación de los métodos seleccionados."""
        import numpy as np
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        # Limpia el frame de la gráfica
        for widget in self.frame_plot_comp.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 5))
        plotted = False

        for m, var in self.comp_methods_vars.items():
            if var.get():
                tree = getattr(self, f"tree_{m}", None)
                if tree is not None and len(tree.get_children()) > 0:
                    xs, ys = [], []
                    for item in tree.get_children():
                        x, y = tree.item(item, "values")
                        xs.append(float(x))
                        ys.append(float(y))
                    if xs and ys:
                        ax.plot(xs, ys, marker="o", label=m.capitalize(), color=self._get_method_color(m.upper()))
                        plotted = True

        if not plotted:
            ax.text(0.5, 0.5, "No hay datos para comparar.\nEjecuta primero los métodos numéricos.", 
                    ha="center", va="center", fontsize=14, color="red", transform=ax.transAxes)
        else:
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title("Comparativa de Métodos Numéricos")
            ax.grid(True)
            ax.legend()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_plot_comp)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

