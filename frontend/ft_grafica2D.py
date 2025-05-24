import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import StringVar, IntVar, BooleanVar, DoubleVar
from tkinter.filedialog import asksaveasfilename
from backend.bk_grafico2D import generar_eje_x, evaluar_funcion
import numpy as np
from scipy.optimize import fsolve
from scipy.signal import find_peaks

class Graficas2DPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=["#f8f9fa", "#0d1117"])
        
        # Configurar matplotlib para modo oscuro
        plt.style.use('dark_background')
        
        # Variable para almacenar la figura actual
        self.current_figure = None
        self.current_canvas = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Header principal
        self.create_header()
        
        # Container principal con scroll
        self.main_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=["#c0c0c0", "#404040"],
            scrollbar_button_hover_color=["#a0a0a0", "#606060"]
        )
        self.main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Sección de entrada de función
        self.create_function_input_section()
        
        # Sección de configuración visual
        self.create_visual_settings_section()
        
        # Sección de configuración avanzada
        self.create_advanced_settings_section()
        
        # Botones principales
        self.create_action_buttons()
        
        # Área de visualización
        self.create_visualization_area()
        
    def create_header(self):
        """Crear header principal con diseño atractivo"""
        header_frame = ctk.CTkFrame(
            self,
            height=90,
            fg_color=["#3b82f6", "#2563eb"],
            corner_radius=0
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Título principal
        title_label = ctk.CTkLabel(
            header_frame,
            text="📈 Graficador de Funciones 2D",
            font=("Segoe UI", 30, "bold"),
            text_color="white"
        )
        title_label.pack(expand=True)
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Visualiza y analiza funciones matemáticas con precisión profesional",
            font=("Segoe UI", 12),
            text_color=["#dbeafe", "#bfdbfe"]
        )
        subtitle_label.pack(pady=(0, 15))
        
    def create_function_input_section(self):
        """Sección de entrada de función"""
        input_section = ctk.CTkFrame(
            self.main_container,
            fg_color=["#ffffff", "#1f2937"],
            corner_radius=12,
            border_width=1,
            border_color=["#e5e7eb", "#374151"]
        )
        input_section.pack(fill="x", pady=(0, 20))
        
        # Título de sección
        section_title = ctk.CTkLabel(
            input_section,
            text="🔢 Definición de Función",
            font=("Segoe UI", 18, "bold"),
            text_color=["#1f2937", "#f9fafb"]
        )
        section_title.pack(pady=(20, 15))
        
        # Frame para entrada de función
        func_input_frame = ctk.CTkFrame(input_section, fg_color="transparent")
        func_input_frame.pack(fill="x", padx=25, pady=(0, 15))
        
        ctk.CTkLabel(
            func_input_frame,
            text="Función f(x):",
            font=("Segoe UI", 14, "bold"),
            text_color=["#374151", "#d1d5db"]
        ).pack(anchor="w", pady=(0, 8))
        
        self.entrada_funcion = ctk.CTkEntry(
            func_input_frame,
            placeholder_text="Ejemplo: sin(x), x**2, exp(x), log(x), tan(x)",
            width=600,
            height=45,
            font=("Consolas", 13),
            corner_radius=8,
            border_width=2,
            border_color=["#d1d5db", "#4b5563"]
        )
        self.entrada_funcion.pack(fill="x", pady=(0, 15))
        
        # Ejemplos rápidos
        self.create_function_examples(func_input_frame)
        
        # Rangos de X
        self.create_range_inputs(input_section)
        
    def create_function_examples(self, parent):
        """Crear botones de ejemplos de funciones"""
        examples_frame = ctk.CTkFrame(parent, fg_color="transparent")
        examples_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            examples_frame,
            text="Funciones populares:",
            font=("Segoe UI", 11),
            text_color=["#6b7280", "#9ca3af"]
        ).pack(anchor="w", pady=(0, 8))
        
        examples_container = ctk.CTkFrame(examples_frame, fg_color="transparent")
        examples_container.pack(fill="x")
        
        examples = [
            ("📐 Seno", "sin(x)"),
            ("📏 Coseno", "cos(x)"),
            ("📊 Cuadrática", "x**2"),
            ("📈 Exponencial", "exp(x)"),
            ("📉 Logaritmo", "log(x)"),
            ("🌊 Compuesta", "sin(x)*exp(-x/5)"),
            ("🔄 Tangente", "tan(x)"),
            ("💫 Polinómica", "x**3 - 2*x**2 + x")
        ]
        
        for i, (name, func) in enumerate(examples):
            btn = ctk.CTkButton(
                examples_container,
                text=name,
                width=130,
                height=30,
                font=("Segoe UI", 10),
                fg_color=["#f1f5f9", "#374151"],
                text_color=["#475569", "#d1d5db"],
                hover_color=["#e2e8f0", "#4b5563"],
                command=lambda f=func: self.set_function_example(f)
            )
            btn.grid(row=i//4, column=i%4, padx=4, pady=2, sticky="ew")
            
        # Configurar grid para que se expanda
        for i in range(4):
            examples_container.grid_columnconfigure(i, weight=1)
            
    def create_range_inputs(self, parent):
        """Crear inputs para rangos de X"""
        range_frame = ctk.CTkFrame(parent, fg_color="transparent")
        range_frame.pack(fill="x", padx=25, pady=(0, 20))
        
        ctk.CTkLabel(
            range_frame,
            text="📏 Rango de Visualización",
            font=("Segoe UI", 14, "bold"),
            text_color=["#374151", "#d1d5db"]
        ).pack(anchor="w", pady=(0, 10))
        
        # Grid para rangos
        range_grid = ctk.CTkFrame(range_frame, fg_color="transparent")
        range_grid.pack(fill="x")
        
        range_grid.grid_columnconfigure((0, 1), weight=1)
        
        # X mínimo
        x_min_frame = ctk.CTkFrame(range_grid, fg_color="transparent")
        x_min_frame.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        ctk.CTkLabel(x_min_frame, text="X mínimo:", font=("Segoe UI", 11)).pack(anchor="w")
        self.rango_inicio = ctk.CTkEntry(
            x_min_frame,
            placeholder_text="-10",
            height=35,
            corner_radius=6
        )
        self.rango_inicio.pack(fill="x", pady=(3, 0))
        
        # X máximo
        x_max_frame = ctk.CTkFrame(range_grid, fg_color="transparent")
        x_max_frame.grid(row=0, column=1, padx=(10, 0), sticky="ew")
        
        ctk.CTkLabel(x_max_frame, text="X máximo:", font=("Segoe UI", 11)).pack(anchor="w")
        self.rango_fin = ctk.CTkEntry(
            x_max_frame,
            placeholder_text="10",
            height=35,
            corner_radius=6
        )
        self.rango_fin.pack(fill="x", pady=(3, 0))
        
        # Rangos predefinidos
        preset_frame = ctk.CTkFrame(range_frame, fg_color="transparent")
        preset_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(
            preset_frame,
            text="Rangos comunes:",
            font=("Segoe UI", 10),
            text_color=["#6b7280", "#9ca3af"]
        ).pack(anchor="w", pady=(0, 5))
        
        preset_buttons = ctk.CTkFrame(preset_frame, fg_color="transparent")
        preset_buttons.pack(fill="x")
        
        presets = [
            ("[-π, π]", -3.14159, 3.14159),
            ("[-10, 10]", -10, 10),
            ("[0, 2π]", 0, 6.28318),
            ("[-5, 5]", -5, 5)
        ]
        
        for i, (name, start, end) in enumerate(presets):
            btn = ctk.CTkButton(
                preset_buttons,
                text=name,
                width=80,
                height=25,
                font=("Segoe UI", 9),
                fg_color=["#e5e7eb", "#4b5563"],
                text_color=["#374151", "#d1d5db"],
                hover_color=["#d1d5db", "#6b7280"],
                command=lambda s=start, e=end: self.set_range_preset(s, e)
            )
            btn.pack(side="left", padx=(0, 5))
            
    def create_visual_settings_section(self):
        """Crear sección de configuración visual"""
        visual_section = ctk.CTkFrame(
            self.main_container,
            fg_color=["#ffffff", "#1f2937"],
            corner_radius=12,
            border_width=1,
            border_color=["#e5e7eb", "#374151"]
        )
        visual_section.pack(fill="x", pady=(0, 20))
        
        # Header con toggle
        header_frame = ctk.CTkFrame(visual_section, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)
        
        self.visual_expanded = ctk.BooleanVar(value=True)
        
        toggle_btn = ctk.CTkButton(
            header_frame,
            text="🎨 Configuración Visual ▼",
            font=("Segoe UI", 16, "bold"),
            fg_color="transparent",
            text_color=["#374151", "#d1d5db"],
            hover_color=["#f3f4f6", "#374151"],
            command=self.toggle_visual_settings
        )
        toggle_btn.pack(anchor="w")
        
        # Panel de configuración visual
        self.visual_panel = ctk.CTkFrame(visual_section, fg_color="transparent")
        self.visual_panel.pack(fill="x", padx=20, pady=(0, 20))
        
        self.create_visual_content()
        
    def create_visual_content(self):
        """Crear contenido de configuración visual"""
        # Grid principal
        visual_grid = ctk.CTkFrame(self.visual_panel, fg_color="transparent")
        visual_grid.pack(fill="x")
        
        visual_grid.grid_columnconfigure((0, 1), weight=1)
        
        # Columna izquierda - Estilo de línea
        style_frame = ctk.CTkFrame(
            visual_grid,
            fg_color=["#f8fafc", "#111827"],
            corner_radius=8
        )
        style_frame.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="new")
        
        ctk.CTkLabel(
            style_frame,
            text="📏 Estilo de Línea",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(15, 10))
        
        # Color
        color_frame = ctk.CTkFrame(style_frame, fg_color="transparent")
        color_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(color_frame, text="Color:", anchor="w").pack(fill="x")
        self.color_var = StringVar(value="cyan")
        ctk.CTkOptionMenu(
            color_frame,
            values=["cyan", "red", "green", "blue", "magenta", "yellow", "orange", "purple"],
            variable=self.color_var,
            width=150,
            height=30
        ).pack(fill="x", pady=(3, 10))
        
        # Estilo de línea
        linestyle_frame = ctk.CTkFrame(style_frame, fg_color="transparent")
        linestyle_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(linestyle_frame, text="Estilo:", anchor="w").pack(fill="x")
        self.style_var = StringVar(value="-")
        style_options = [
            ("Sólida (-)", "-"),
            ("Punteada (--)", "--"),
            ("Punto-raya (-·)", "-."),
            ("Puntos (:)", ":")
        ]
        
        for name, value in style_options:
            radio = ctk.CTkRadioButton(
                linestyle_frame,
                text=name,
                variable=self.style_var,
                value=value,
                font=("Segoe UI", 10)
            )
            radio.pack(anchor="w", pady=2)
            
        # Grosor de línea
        width_frame = ctk.CTkFrame(style_frame, fg_color="transparent")
        width_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        width_label_frame = ctk.CTkFrame(width_frame, fg_color="transparent")
        width_label_frame.pack(fill="x")
        
        ctk.CTkLabel(width_label_frame, text="Grosor:", anchor="w").pack(side="left")
        self.width_var = DoubleVar(value=2.0)
        self.width_label = ctk.CTkLabel(width_label_frame, text="2.0")
        self.width_label.pack(side="right")
        
        ctk.CTkSlider(
            width_frame,
            from_=0.5,
            to=5.0,
            variable=self.width_var,
            width=120,
            command=self.update_width_label
        ).pack(fill="x", pady=(3, 0))
        
        # Columna derecha - Configuración del gráfico
        graph_frame = ctk.CTkFrame(
            visual_grid,
            fg_color=["#f8fafc", "#111827"],
            corner_radius=8
        )
        graph_frame.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="new")
        
        ctk.CTkLabel(
            graph_frame,
            text="📊 Configuración del Gráfico",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(15, 10))
        
        # Opciones de visualización
        options_frame = ctk.CTkFrame(graph_frame, fg_color="transparent")
        options_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Grid
        self.grid_var = BooleanVar(value=True)
        grid_check = ctk.CTkCheckBox(
            options_frame,
            text="Mostrar cuadrícula",
            variable=self.grid_var,
            font=("Segoe UI", 11)
        )
        grid_check.pack(anchor="w", pady=2)
        
        # Leyenda
        self.legend_var = BooleanVar(value=True)
        legend_check = ctk.CTkCheckBox(
            options_frame,
            text="Mostrar leyenda",
            variable=self.legend_var,
            font=("Segoe UI", 11)
        )
        legend_check.pack(anchor="w", pady=2)
        
        # Etiquetas de ejes
        self.labels_var = BooleanVar(value=True)
        labels_check = ctk.CTkCheckBox(
            options_frame,
            text="Etiquetas de ejes",
            variable=self.labels_var,
            font=("Segoe UI", 11)
        )
        labels_check.pack(anchor="w", pady=2)
        
        # Título personalizado
        title_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(title_frame, text="Título personalizado:", anchor="w").pack(fill="x")
        self.custom_title = ctk.CTkEntry(
            title_frame,
            placeholder_text="Opcional - Título del gráfico",
            height=30
        )
        self.custom_title.pack(fill="x", pady=(3, 0))
        
    def create_advanced_settings_section(self):
        """Crear sección de configuración avanzada"""
        advanced_section = ctk.CTkFrame(
            self.main_container,
            fg_color=["#ffffff", "#1f2937"],
            corner_radius=12,
            border_width=1,
            border_color=["#e5e7eb", "#374151"]
        )
        advanced_section.pack(fill="x", pady=(0, 20))
        
        # Header
        header_frame = ctk.CTkFrame(advanced_section, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)
        
        self.advanced_expanded = ctk.BooleanVar(value=False)
        
        toggle_btn = ctk.CTkButton(
            header_frame,
            text="⚙️ Configuración Avanzada ▼",
            font=("Segoe UI", 16, "bold"),
            fg_color="transparent",
            text_color=["#374151", "#d1d5db"],
            hover_color=["#f3f4f6", "#374151"],
            command=self.toggle_advanced_settings
        )
        toggle_btn.pack(anchor="w")
        
        # Panel avanzado
        self.advanced_panel = ctk.CTkFrame(advanced_section, fg_color="transparent")
        
        self.create_advanced_content()
        
    def create_advanced_content(self):
        """Crear contenido de configuración avanzada"""
        content_frame = ctk.CTkFrame(self.advanced_panel, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        content_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Resolución
        resolution_frame = ctk.CTkFrame(
            content_frame,
            fg_color=["#f8fafc", "#111827"],
            corner_radius=8
        )
        resolution_frame.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="new")
        
        ctk.CTkLabel(
            resolution_frame,
            text="🎯 Precisión de Cálculo",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(15, 10))
        
        res_frame = ctk.CTkFrame(resolution_frame, fg_color="transparent")
        res_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        res_label_frame = ctk.CTkFrame(res_frame, fg_color="transparent")
        res_label_frame.pack(fill="x")
        
        ctk.CTkLabel(res_label_frame, text="Número de puntos:", anchor="w").pack(side="left")
        self.resol_var = IntVar(value=1000)
        self.res_label = ctk.CTkLabel(res_label_frame, text="1000")
        self.res_label.pack(side="right")
        
        ctk.CTkSlider(
            res_frame,
            from_=100,
            to=5000,
            number_of_steps=49,
            variable=self.resol_var,
            width=180,
            command=self.update_resolution_label
        ).pack(fill="x", pady=(5, 0))
        
        # Análisis
        analysis_frame = ctk.CTkFrame(
            content_frame,
            fg_color=["#f8fafc", "#111827"],
            corner_radius=8
        )
        analysis_frame.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="new")
        
        ctk.CTkLabel(
            analysis_frame,
            text="📐 Herramientas de Análisis",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(15, 10))
        
        analysis_options = ctk.CTkFrame(analysis_frame, fg_color="transparent")
        analysis_options.pack(fill="x", padx=15, pady=(0, 15))
        
        # Derivada
        self.derivative_var = BooleanVar(value=False)
        derivative_check = ctk.CTkCheckBox(
            analysis_options,
            text="Mostrar derivada",
            variable=self.derivative_var,
            font=("Segoe UI", 11)
        )
        derivative_check.pack(anchor="w", pady=2)
        
        # Ceros
        self.zeros_var = BooleanVar(value=False)
        zeros_check = ctk.CTkCheckBox(
            analysis_options,
            text="Marcar ceros",
            variable=self.zeros_var,
            font=("Segoe UI", 11)
        )
        zeros_check.pack(anchor="w", pady=2)
        
        # Máximos y mínimos
        self.extrema_var = BooleanVar(value=False)
        extrema_check = ctk.CTkCheckBox(
            analysis_options,
            text="Marcar extremos",
            variable=self.extrema_var,
            font=("Segoe UI", 11)
        )
        extrema_check.pack(anchor="w", pady=2)
        
    def create_action_buttons(self):
        """Crear botones de acción principales"""
        button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        button_frame.pack(pady=20)
        
        # Botón principal de graficado
        self.graph_button = ctk.CTkButton(
            button_frame,
            text="🚀 Generar Gráfica",
            command=self.graficar_funcion,
            height=50,
            width=200,
            font=("Segoe UI", 16, "bold"),
            fg_color=["#3b82f6", "#2563eb"],
            hover_color=["#2563eb", "#1d4ed8"],
            corner_radius=25
        )
        self.graph_button.pack(side="left", padx=(0, 15))
        
        # Botón de guardar
        self.save_button = ctk.CTkButton(
            button_frame,
            text="💾 Guardar Imagen",
            command=self.guardar_imagen,
            height=50,
            width=160,
            font=("Segoe UI", 14, "bold"),
            fg_color=["#10b981", "#059669"],
            hover_color=["#059669", "#047857"],
            corner_radius=25,
            state="disabled"
        )
        self.save_button.pack(side="left")
        
        # Estado
        self.status_label = ctk.CTkLabel(
            button_frame,
            text="Listo para graficar",
            font=("Segoe UI", 11),
            text_color=["#6b7280", "#9ca3af"]
        )
        self.status_label.pack(pady=(8, 0))
        
    def create_visualization_area(self):
        """Crear área de visualización"""
        viz_section = ctk.CTkFrame(
            self.main_container,
            fg_color=["#ffffff", "#1f2937"],
            corner_radius=12,
            border_width=1,
            border_color=["#e5e7eb", "#374151"]
        )
        viz_section.pack(fill="both", expand=True, pady=(0, 20))
        
        # Header
        viz_header = ctk.CTkFrame(viz_section, fg_color="transparent", height=50)
        viz_header.pack(fill="x", padx=20, pady=(15, 10))
        viz_header.pack_propagate(False)
        
        ctk.CTkLabel(
            viz_header,
            text="📊 Visualización",
            font=("Segoe UI", 18, "bold"),
            text_color=["#1f2937", "#f9fafb"]
        ).pack(side="left", expand=True)
        
        # Canvas frame
        self.canvas_frame = ctk.CTkFrame(
            viz_section,
            fg_color=["#f8fafc", "#111827"],
            corner_radius=8
        )
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Placeholder
        self.placeholder_label = ctk.CTkLabel(
            self.canvas_frame,
            text="🎯 Define una función y presiona 'Generar Gráfica'\npara visualizar tu función aquí",
            font=("Segoe UI", 14),
            text_color=["#6b7280", "#9ca3af"]
        )
        self.placeholder_label.grid(row=0, column=0)
        
    # Métodos de utilidad
    def set_function_example(self, func):
        """Establecer ejemplo de función"""
        self.entrada_funcion.delete(0, "end")
        self.entrada_funcion.insert(0, func)
        
    def set_range_preset(self, start, end):
        """Establecer rango predefinido"""
        self.rango_inicio.delete(0, "end")
        self.rango_inicio.insert(0, str(start))
        self.rango_fin.delete(0, "end")
        self.rango_fin.insert(0, str(end))
        
    def toggle_visual_settings(self):
        """Alternar configuración visual"""
        if self.visual_expanded.get():
            self.visual_panel.pack_forget()
            self.visual_expanded.set(False)
        else:
            self.visual_panel.pack(fill="x", padx=20, pady=(0, 20))
            self.visual_expanded.set(True)
            
    def toggle_advanced_settings(self):
        """Alternar configuración avanzada"""
        if self.advanced_expanded.get():
            self.advanced_panel.pack_forget()
            self.advanced_expanded.set(False)
        else:
            self.advanced_panel.pack(fill="x")
            self.advanced_expanded.set(True)
            
    def update_width_label(self, value):
        """Actualizar etiqueta de grosor"""
        self.width_label.configure(text=f"{float(value):.1f}")
        
    def update_resolution_label(self, value):
        """Actualizar etiqueta de resolución"""
        self.res_label.configure(text=str(int(value)))
        
    def safe_eval_function(self, x_vals, func_str):
        """Evaluar función de manera segura"""
        try:
            # Reemplazar funciones matemáticas comunes
            safe_dict = {
                'x': x_vals,
                'sin': np.sin,
                'cos': np.cos,
                'tan': np.tan,
                'exp': np.exp,
                'log': np.log,
                'ln': np.log,
                'sqrt': np.sqrt,
                'abs': np.abs,
                'pi': np.pi,
                'e': np.e,
                'arcsin': np.arcsin,
                'arccos': np.arccos,
                'arctan': np.arctan,
                'sinh': np.sinh,
                'cosh': np.cosh,
                'tanh': np.tanh,
                '__builtins__': {}
            }
            
            # Evaluar la función
            y_vals = eval(func_str, safe_dict)
            
            # Manejar valores infinitos o NaN
            y_vals = np.array(y_vals, dtype=float)
            y_vals[np.isinf(y_vals)] = np.nan
            y_vals[np.isnan(y_vals)] = np.nan
            
            return y_vals
            
        except Exception as e:
            raise ValueError(f"Error al evaluar la función: {str(e)}")
    
    def calculate_derivative(self, x_vals, y_vals):
        """Calcular derivada numérica"""
        try:
            dx = x_vals[1] - x_vals[0]
            dy_dx = np.gradient(y_vals, dx)
            return dy_dx
        except:
            return np.zeros_like(x_vals)
    
    def find_zeros(self, x_vals, y_vals):
        """Encontrar ceros de la función"""
        zeros = []
        try:
            for i in range(len(y_vals)-1):
                if not (np.isnan(y_vals[i]) or np.isnan(y_vals[i+1])):
                    if y_vals[i] * y_vals[i+1] < 0:  # Cambio de signo
                        # Interpolación lineal para aproximar el cero
                        x_zero = x_vals[i] - y_vals[i] * (x_vals[i+1] - x_vals[i]) / (y_vals[i+1] - y_vals[i])
                        zeros.append(x_zero)
        except:
            pass
        return zeros[:10]  # Limitar a 10 ceros para evitar saturación
    
    def find_extrema(self, x_vals, y_vals):
        """Encontrar máximos y mínimos locales"""
        try:
            # Filtrar valores NaN
            valid_indices = ~np.isnan(y_vals)
            if np.sum(valid_indices) < 3:
                return [], []
            
            valid_y = y_vals[valid_indices]
            valid_x = x_vals[valid_indices]
            
            # Encontrar picos (máximos)
            peaks, _ = find_peaks(valid_y, height=None, distance=len(valid_y)//20)
            # Encontrar valles (mínimos)
            valleys, _ = find_peaks(-valid_y, height=None, distance=len(valid_y)//20)
            
            maxima = [(valid_x[i], valid_y[i]) for i in peaks[:5]]  # Limitar a 5
            minima = [(valid_x[i], valid_y[i]) for i in valleys[:5]]  # Limitar a 5
            
            return maxima, minima
        except:
            return [], []
        
    def graficar_funcion(self):
        """Generar gráfica con configuración mejorada"""
        # Limpiar canvas
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
            
        # Actualizar estado
        self.status_label.configure(text="Generando gráfica...")
        self.graph_button.configure(state="disabled", text="⏳ Generando...")
        self.update()
        
        try:
            # Obtener valores
            inicio = float(self.rango_inicio.get()) if self.rango_inicio.get() else -10.0
            fin = float(self.rango_fin.get()) if self.rango_fin.get() else 10.0
            funcion_str = self.entrada_funcion.get()
            
            if not funcion_str:
                raise ValueError("Por favor, ingresa una función válida")
                
            if inicio >= fin:
                raise ValueError("El rango inicial debe ser menor que el final")
                
            resol = self.resol_var.get()
            color = self.color_var.get()
            style = self.style_var.get()
            width = self.width_var.get()
            show_grid = self.grid_var.get()
            show_legend = self.legend_var.get()
            show_labels = self.labels_var.get()
            custom_title = self.custom_title.get()
            
            # Generar datos
            x_vals = np.linspace(inicio, fin, resol)
            y_vals = self.safe_eval_function(x_vals, funcion_str)
            
            # Crear figura
            self.current_figure = plt.figure(figsize=(5, 3), facecolor='#1a1a1a')  # <-- Cambia el tamaño aquí
            ax = self.current_figure.add_subplot(111, facecolor='#1a1a1a')
            
            # Graficar función principal
            ax.plot(x_vals, y_vals, 
                   color=color, 
                   linestyle=style, 
                   linewidth=width,
                   label=f'f(x) = {funcion_str}',
                   alpha=0.9)
            
            # Análisis avanzado
            if self.derivative_var.get():
                try:
                    dy_dx = self.calculate_derivative(x_vals, y_vals)
                    ax.plot(x_vals, dy_dx, 
                           color='orange', 
                           linestyle='--', 
                           linewidth=width*0.8,
                           label=f"f'(x)",
                           alpha=0.7)
                except:
                    pass
            
            if self.zeros_var.get():
                zeros = self.find_zeros(x_vals, y_vals)
                for zero in zeros:
                    ax.axvline(x=zero, color='red', linestyle=':', alpha=0.7, linewidth=1)
                    ax.plot(zero, 0, 'ro', markersize=6, label='Ceros' if zero == zeros[0] else "")
            
            if self.extrema_var.get():
                maxima, minima = self.find_extrema(x_vals, y_vals)
                for i, (x_max, y_max) in enumerate(maxima):
                    ax.plot(x_max, y_max, 'g^', markersize=8, 
                           label='Máximos' if i == 0 else "")
                for i, (x_min, y_min) in enumerate(minima):
                    ax.plot(x_min, y_min, 'rv', markersize=8, 
                           label='Mínimos' if i == 0 else "")
            
            # Configurar apariencia
            ax.set_facecolor('#1a1a1a')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            
            if show_grid:
                ax.grid(True, alpha=0.3, color='gray', linestyle='-', linewidth=0.5)
                
            if show_labels:
                ax.set_xlabel('x', color='white', fontsize=12)
                ax.set_ylabel('f(x)', color='white', fontsize=12)
                
            # Título
            title_text = custom_title if custom_title else f'Gráfica de f(x) = {funcion_str}'
            ax.set_title(title_text, color='white', fontsize=14, fontweight='bold', pad=20)
            
            if show_legend:
                legend = ax.legend(facecolor='#2a2a2a', edgecolor='white')
                legend.get_frame().set_alpha(0.8)
                for text in legend.get_texts():
                    text.set_color('white')
            
            # Ajustar límites del gráfico
            y_min, y_max = np.nanpercentile(y_vals, [5, 95])
            if not np.isnan(y_min) and not np.isnan(y_max):
                y_range = y_max - y_min
                if y_range > 0:
                    ax.set_ylim(y_min - y_range*0.1, y_max + y_range*0.1)
            
            ax.set_xlim(inicio, fin)
            
            # Ajustar layout
            self.current_figure.tight_layout()
            
            # Mostrar en canvas
            self.current_canvas = FigureCanvasTkAgg(self.current_figure, self.canvas_frame)
            self.current_canvas.draw()
            self.current_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            
            # Habilitar botón de guardar
            self.save_button.configure(state="normal")
            
            # Actualizar estado
            self.status_label.configure(text="✅ Gráfica generada exitosamente")
            
        except ValueError as ve:
            CTkMessagebox(
                title="Error de Entrada",
                message=str(ve),
                icon="warning"
            )
            self.status_label.configure(text=f"❌ Error: {str(ve)}")
            
        except Exception as e:
            CTkMessagebox(
                title="Error Inesperado",
                message=f"Ocurrió un error inesperado: {str(e)}",
                icon="cancel"
            )
            self.status_label.configure(text=f"❌ Error inesperado")
            
        finally:
            # Restaurar botón
            self.graph_button.configure(state="normal", text="🚀 Generar Gráfica")
    
    def guardar_imagen(self):
        """Guardar la gráfica actual como imagen"""
        if self.current_figure is None:
            CTkMessagebox(
                title="Sin Gráfica",
                message="No hay ninguna gráfica para guardar. Primero genera una gráfica.",
                icon="warning"
            )
            return
            
        try:
            # Abrir diálogo de guardado
            filename = asksaveasfilename(
                title="Guardar Gráfica",
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("PDF files", "*.pdf"),
                    ("SVG files", "*.svg"),
                    ("JPG files", "*.jpg"),
                    ("All files", "*.*")
                ]
            )
            
            if filename:
                # Guardar con alta resolución
                self.current_figure.savefig(
                    filename,
                    dpi=300,
                    bbox_inches='tight',
                    facecolor='#1a1a1a',
                    edgecolor='none',
                    pad_inches=0.2
                )
                
                CTkMessagebox(
                    title="Guardado Exitoso",
                    message=f"Gráfica guardada como:\n{filename}",
                    icon="check"
                )
                
                self.status_label.configure(text="💾 Imagen guardada exitosamente")
                
        except Exception as e:
            CTkMessagebox(
                title="Error al Guardar",
                message=f"No se pudo guardar la imagen:\n{str(e)}",
                icon="cancel"
            )
            self.status_label.configure(text="❌ Error al guardar imagen")
    
    def limpiar_grafica(self):
        """Limpiar la gráfica actual"""
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
            
        self.placeholder_label = ctk.CTkLabel(
            self.canvas_frame,
            text="🎯 Define una función y presiona 'Generar Gráfica'\npara visualizar tu función aquí",
            font=("Segoe UI", 14),
            text_color=["#6b7280", "#9ca3af"]
        )
        self.placeholder_label.grid(row=0, column=0)
        
        self.current_figure = None
        self.current_canvas = None
        self.save_button.configure(state="disabled")
        self.status_label.configure(text="Gráfica limpiada")

# # Ejemplo de uso
# if __name__ == "__main__":
#     root = ctk.CTk()
#     root.title("Graficador de Funciones 2D")
#     root.geometry("1400x900")
    
#     # Configurar tema
#     ctk.set_appearance_mode("dark")
#     ctk.set_default_color_theme("blue")
    
#     app = Graficas2DPage(root)
#     app.pack(fill="both", expand=True)
    
#     root.mainloop()