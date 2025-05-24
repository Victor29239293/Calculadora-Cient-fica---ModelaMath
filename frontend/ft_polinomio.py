import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
from backend.bk_polinomio import (
    generar_coeficientes,
    evaluar_polinomio,
    derivar_polinomio,
    integrar_polinomio,
    formatear_polinomio
)

class PolinomiosPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")
        
        # Variables de estado
        self.coef_entries = []
        self.grado_var = ctk.StringVar(value="2")
        self.current_polynomial = None
        self.last_evaluation = None
        
        # Configurar colores y tema
        self.setup_colors()
        self.setup_ui()
        
    def setup_colors(self):
        """Define la paleta de colores moderna"""
        self.colors = {
            'bg_primary': '#0A0A0F',
            'bg_secondary': '#1A1A2E',
            'bg_tertiary': '#16213E',
            'bg_card': '#21262D',
            'accent_primary': '#7C3AED',
            'accent_secondary': '#06B6D4',
            'accent_success': '#10B981',
            'accent_warning': '#F59E0B',
            'accent_error': '#EF4444',
            'accent_info': '#3B82F6',
            'text_primary': '#FFFFFF',
            'text_secondary': '#D1D5DB',
            'text_muted': '#6B7280',
            'border': '#374151',
            'gradient_start': '#7C3AED',
            'gradient_end': '#06B6D4',
        }
        
    def setup_ui(self):
        """Configura la interfaz de usuario moderna"""
        # Contenedor principal con scroll
        main_container = ctk.CTkScrollableFrame(self, fg_color=self.colors['bg_primary'], corner_radius=0)
        main_container.pack(fill="both", expand=True)
        
        # Header con gradiente visual
        self.create_header(main_container)
        
        # Panel de configuración principal
        config_panel = ctk.CTkFrame(main_container, fg_color=self.colors['bg_secondary'], corner_radius=20)
        config_panel.pack(pady=(0, 20), padx=20, fill="x")
        
        # Configuración del polinomio
        self.create_polynomial_config(config_panel)
        
        # Panel de coeficientes
        self.create_coefficients_panel(config_panel)
        
        # Panel de operaciones
        self.create_operations_panel(config_panel)
        
        # Panel de resultados y evaluación
        self.create_results_panel(main_container)
        
        # Panel de visualización
        self.create_visualization_panel(main_container)
        
        # Inicializar campos
        self.generar_campos()
        
    def create_header(self, parent):
        """Crea el header moderno con gradiente"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent", height=120)
        header_frame.pack(fill="x", pady=(20, 30), padx=20)
        header_frame.pack_propagate(False)
        
        # Contenedor del título con efecto gradiente
        title_container = ctk.CTkFrame(header_frame, fg_color=self.colors['bg_secondary'], corner_radius=20)
        title_container.pack(fill="x")
        
        # Título principal
        title_label = ctk.CTkLabel(
            title_container,
            text="📈 ANALIZADOR DE POLINOMIOS",
            font=("SF Pro Display", 32, "bold"),
            text_color=self.colors['accent_primary']
        )
        title_label.pack(pady=(25, 10))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            title_container,
            text="Análisis matemático avanzado • Derivadas • Integrales • Evaluación",
            font=("SF Pro Text", 16),
            text_color=self.colors['text_secondary']
        )
        subtitle_label.pack(pady=(0, 25))
        
    def create_polynomial_config(self, parent):
        """Panel de configuración del polinomio"""
        config_frame = ctk.CTkFrame(parent, fg_color=self.colors['bg_tertiary'], corner_radius=15)
        config_frame.pack(pady=20, padx=20, fill="x")
        
        # Título
        config_title = ctk.CTkLabel(
            config_frame,
            text="⚙️ Configuración del Polinomio",
            font=("SF Pro Text", 18, "bold"),
            text_color=self.colors['text_primary']
        )
        config_title.pack(pady=(20, 15))
        
        # Contenedor de controles
        controls_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        controls_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        # Selector de grado
        degree_frame = ctk.CTkFrame(controls_frame, fg_color=self.colors['bg_card'], corner_radius=12)
        degree_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            degree_frame,
            text="Grado del Polinomio",
            font=("SF Pro Text", 14, "bold"),
            text_color=self.colors['text_secondary']
        ).pack(pady=(15, 5), padx=20)
        
        degree_menu = ctk.CTkOptionMenu(
            degree_frame,
            values=["1", "2", "3", "4", "5"],
            variable=self.grado_var,
            font=("SF Pro Text", 14),
            fg_color=self.colors['accent_primary'],
            button_color=self.colors['accent_secondary'],
            button_hover_color=self.colors['accent_info'],
            dropdown_fg_color=self.colors['bg_secondary'],
            width=150,
            height=35,
            command=self.on_degree_change
        )
        degree_menu.pack(pady=(0, 15), padx=20)
        
        # Botón generar
        generate_btn = ctk.CTkButton(
            controls_frame,
            text="🎲 Generar Coeficientes",
            command=self.generar_campos,
            font=("SF Pro Text", 16, "bold"),
            fg_color=self.colors['accent_success'],
            hover_color=self.colors['accent_info'],
            corner_radius=15,
            width=200,
            height=50
        )
        generate_btn.pack(side="left", padx=15)
        
        # Indicador de tipo
        self.tipo_frame = ctk.CTkFrame(controls_frame, fg_color=self.colors['bg_card'], corner_radius=12)
        self.tipo_frame.pack(side="right", padx=(15, 0))
        
        ctk.CTkLabel(
            self.tipo_frame,
            text="Tipo de Función",
            font=("SF Pro Text", 12),
            text_color=self.colors['text_muted']
        ).pack(pady=(10, 0), padx=20)
        
        self.tipo_label = ctk.CTkLabel(
            self.tipo_frame,
            text="Cuadrática",
            font=("SF Pro Text", 16, "bold"),
            text_color=self.colors['accent_secondary']
        )
        self.tipo_label.pack(pady=(0, 15), padx=20)
        
    def create_coefficients_panel(self, parent):
        """Panel de coeficientes con diseño moderno"""
        coef_container = ctk.CTkFrame(parent, fg_color=self.colors['bg_tertiary'], corner_radius=15)
        coef_container.pack(pady=(0, 20), padx=20, fill="x")
        
        # Título
        coef_title = ctk.CTkLabel(
            coef_container,
            text="🔢 Coeficientes del Polinomio",
            font=("SF Pro Text", 18, "bold"),
            text_color=self.colors['text_primary']
        )
        coef_title.pack(pady=(20, 15))
        
        # Frame para los coeficientes
        self.frame_coef = ctk.CTkFrame(coef_container, fg_color=self.colors['bg_card'], corner_radius=12)
        self.frame_coef.pack(pady=(0, 20), padx=20, fill="x")

        
    def create_operations_panel(self, parent):
        """Panel de operaciones con diseño premium"""
        operations_frame = ctk.CTkFrame(parent, fg_color=self.colors['bg_tertiary'], corner_radius=15)
        operations_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        ops_title = ctk.CTkLabel(
            operations_frame,
            text="🧮 Operaciones Matemáticas",
            font=("SF Pro Text", 18, "bold"),
            text_color=self.colors['text_primary']
        )
        ops_title.pack(pady=(20, 15))
        
        # Panel de evaluación
        eval_frame = ctk.CTkFrame(operations_frame, fg_color=self.colors['bg_card'], corner_radius=12)
        eval_frame.pack(pady=(0, 15), padx=20, fill="x")
        
        eval_title = ctk.CTkLabel(
            eval_frame,
            text="📍 Evaluar Polinomio",
            font=("SF Pro Text", 16, "bold"),
            text_color=self.colors['accent_info']
        )
        eval_title.pack(pady=(15, 10))
        
        eval_controls = ctk.CTkFrame(eval_frame, fg_color="transparent")
        eval_controls.pack(pady=(0, 15), padx=20)
        
        ctk.CTkLabel(
            eval_controls,
            text="f(",
            font=("SF Pro Text", 16, "bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left", padx=(0, 5))
        
        self.eval_x = ctk.CTkEntry(
            eval_controls,
            width=100,
            height=40,
            font=("SF Pro Mono", 16),
            fg_color=self.colors['bg_primary'],
            border_color=self.colors['accent_info'],
            text_color=self.colors['text_primary'],
            placeholder_text="x"
        )
        self.eval_x.pack(side="left", padx=5)
        
        ctk.CTkLabel(
            eval_controls,
            text=") =",
            font=("SF Pro Text", 16, "bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left", padx=(5, 15))
        
        eval_btn = ctk.CTkButton(
            eval_controls,
            text="Calcular",
            command=self.evaluar,
            font=("SF Pro Text", 14, "bold"),
            fg_color=self.colors['accent_info'],
            hover_color=self.colors['accent_primary'],
            width=100,
            height=40,
            corner_radius=20
        )
        eval_btn.pack(side="left")
        
        # Botones de operaciones
        operations_buttons = ctk.CTkFrame(operations_frame, fg_color="transparent")
        operations_buttons.pack(pady=(0, 20), padx=20)
        
        operations = [
            ("∂", "Derivar", self.derivar, self.colors['accent_warning']),
            ("∫", "Integrar", self.integrar, self.colors['accent_success']),
            ("📊", "Graficar", self.graficar_original, self.colors['accent_secondary']),
        ]
        
        for i, (icon, text, command, color) in enumerate(operations):
            btn_container = ctk.CTkFrame(operations_buttons, fg_color=color, corner_radius=15)
            btn_container.grid(row=0, column=i, padx=15, pady=10)
            
            btn = ctk.CTkButton(
                btn_container,
                text=f"{icon}\n{text}",
                command=command,
                font=("SF Pro Text", 16, "bold"),
                fg_color=color,  # Usa el color del botón
                hover_color=self.colors['accent_info'],  # O cualquier color de tu paleta
                text_color=self.colors['text_primary'],
                width=100,
                height=50
            )
            btn.pack(padx=3, pady=3)
            
    def create_results_panel(self, parent):
        """Panel de resultados con diseño moderno"""
        results_frame = ctk.CTkFrame(parent, fg_color=self.colors['bg_secondary'], corner_radius=20)
        results_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        results_title = ctk.CTkLabel(
            results_frame,
            text="📋 Resultados",
            font=("SF Pro Text", 18, "bold"),
            text_color=self.colors['text_primary']
        )
        results_title.pack(pady=(20, 15))
        
        # Contenedor de resultados
        results_container = ctk.CTkFrame(results_frame, fg_color=self.colors['bg_tertiary'], corner_radius=15)
        results_container.pack(pady=(0, 20), padx=20, fill="x")
        
        # Status
        self.status_frame = ctk.CTkFrame(results_container, fg_color=self.colors['bg_card'], corner_radius=10)
        self.status_frame.pack(pady=15, padx=20, fill="x")
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="⏳ Listo para analizar",
            font=("SF Pro Text", 14),
            text_color=self.colors['text_secondary']
        )
        self.status_label.pack(pady=10)
        
        # Resultado principal
        self.result_display = ctk.CTkFrame(
            results_container,
            fg_color=self.colors['bg_primary'],
            corner_radius=12,
            height=100
        )
        self.result_display.pack(pady=(0, 15), padx=20, fill="x")
        
    def create_visualization_panel(self, parent):
        """Panel de visualización mejorado"""
        viz_frame = ctk.CTkFrame(parent, fg_color=self.colors['bg_secondary'], corner_radius=20)
        viz_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)
        
        viz_title = ctk.CTkLabel(
            viz_frame,
            text="📈 Visualización Matemática",
            font=("SF Pro Text", 18, "bold"),
            text_color=self.colors['text_primary']
        )
        viz_title.pack(pady=(20, 15))
        
        self.plot_frame = ctk.CTkFrame(viz_frame, fg_color=self.colors['bg_primary'], corner_radius=15)
        self.plot_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)
        
        # Placeholder inicial
        self.placeholder_label = ctk.CTkLabel(
            self.plot_frame,
            text="📊 La gráfica del polinomio aparecerá aquí",
            font=("SF Pro Text", 16),
            text_color=self.colors['text_muted']
        )
        self.placeholder_label.pack(expand=True)
        
        self.canvas = None
        
    def on_degree_change(self, value):
        """Callback cuando cambia el grado"""
        self.update_status("🔄 Actualizando configuración...", self.colors['accent_warning'])
        self.after(100, self.generar_campos)
        
    def update_status(self, message, color=None):
        """Actualiza el status con color"""
        self.status_label.configure(text=message)
        if color:
            self.status_frame.configure(fg_color=color)  # Solo el color base, sin transparencia
            
    def update_result_display(self, text, latex=False):
        """Actualiza el display de resultados"""
        # Limpiar el área de resultados
        for widget in self.result_display.winfo_children():
            widget.destroy()
        if latex:
            self.mostrar_resultado_latex(text)
        else:
            label = ctk.CTkLabel(
                self.result_display,
                text=text,
                font=("SF Pro Mono", 16),
                text_color=self.colors['text_primary'],
                anchor="w",
                justify="left"
            )
            label.pack(fill="both", expand=True, padx=10, pady=10)

    def generar_campos(self):
        """Genera campos de coeficientes con diseño moderno"""
        # Limpiar campos anteriores
        for widget in self.frame_coef.winfo_children():
            widget.destroy()
        self.coef_entries.clear()

        try:
            grado = int(self.grado_var.get())
        except:
            CTkMessagebox(title="Error", message="Grado inválido", icon="cancel")
            return

        # Actualizar tipo
        tipos = {1: "Lineal", 2: "Cuadrática", 3: "Cúbica", 4: "Cuártica", 5: "Quíntica"}
        self.tipo_label.configure(text=tipos.get(grado, f"Grado {grado}"))

        # Título de coeficientes
        coef_title = ctk.CTkLabel(
            self.frame_coef,
            text="Ingresa los coeficientes:",
            font=("SF Pro Text", 14, "bold"),
            text_color=self.colors['text_secondary']
        )
        coef_title.pack(pady=(15, 10))

        # Contenedor de entries
        entries_frame = ctk.CTkFrame(self.frame_coef, fg_color="transparent")
        entries_frame.pack(pady=(0, 15))

        # Generar coeficientes aleatorios
        coefs = generar_coeficientes(grado)
        
        # Crear entries para cada coeficiente
        for i, coef in enumerate(coefs):
            coef_container = ctk.CTkFrame(entries_frame, fg_color=self.colors['bg_primary'], corner_radius=10)
            coef_container.pack(side="left", padx=8)
            
            # Etiqueta del término
            power = grado - i
            if power == 0:
                term_label = "Constante"
            elif power == 1:
                term_label = "x"
            else:
                term_label = f"x^{power}"
                
            ctk.CTkLabel(
                coef_container,
                text=term_label,
                font=("SF Pro Text", 12, "bold"),
                text_color=self.colors['accent_secondary']
            ).pack(pady=(8, 2))
            
            # Entry para coeficiente
            entry = ctk.CTkEntry(
                coef_container,
                width=80,
                height=35,
                font=("SF Pro Mono", 14),
                fg_color=self.colors['bg_secondary'],
                border_color=self.colors['accent_primary'],
                text_color=self.colors['text_primary']
            )
            entry.pack(pady=(0, 8), padx=8)
            entry.insert(0, str(coef))
            self.coef_entries.append(entry)

        # Actualizar ecuación
        # self.update_equation_display()
        self.update_status("✅ Coeficientes generados", self.colors['accent_success'])

    # def update_equation_display(self):
    #     """Actualiza la visualización de la ecuación"""
    #     try:
    #         coefs = self.leer_coeficientes()
    #         if coefs:
    #             equation = self.format_equation(coefs)
    #             self.equation_label.configure(text=f"f(x) = {equation}")
    #     except:
    #         pass

    def format_equation(self, coefs):
        """Formatea la ecuación para mostrar"""
        if not coefs:
            return "0"
            
        grado = len(coefs) - 1
        terms = []
        
        for i, coef in enumerate(coefs):
            if coef == 0:
                continue
                
            power = grado - i
            
            # Formatear coeficiente
            if coef == 1 and power > 0:
                coef_str = ""
            elif coef == -1 and power > 0:
                coef_str = "-"
            else:
                coef_str = str(coef)
            
            # Formatear potencia
            if power == 0:
                term = coef_str if coef_str else "1"
            elif power == 1:
                term = f"{coef_str}x"
            else:
                term = f"{coef_str}x^{power}"
            
            terms.append(term)
        
        if not terms:
            return "0"
        
        # Unir términos
        equation = terms[0]
        for term in terms[1:]:
            if term.startswith('-'):
                equation += f" {term}"
            else:
                equation += f" + {term}"
                
        return equation

    def leer_coeficientes(self):
        """Lee coeficientes con validación"""
        try:
            return [float(entry.get()) for entry in self.coef_entries]
        except:
            CTkMessagebox(title="Error", message="Asegúrate de ingresar números válidos", icon="cancel")
            return None

    def evaluar(self):
        """Evalúa el polinomio en un punto"""
        coefs = self.leer_coeficientes()
        if coefs is None:
            return
            
        try:
            x_val = float(self.eval_x.get())
            resultado = evaluar_polinomio(coefs, x_val)
            
            # Mostrar resultado
            result_text = f"Evaluación en x = {x_val}:\nf({x_val}) = {resultado:.6f}"
            self.update_result_display(result_text)
            self.update_status(f"✅ Evaluado en x = {x_val}", self.colors['accent_success'])
            
            # Graficar con punto de evaluación
            self.graficar_polinomio(coefs, eval_point=(x_val, resultado))
            
        except ValueError:
            self.update_status("❌ Valor de x inválido", self.colors['accent_error'])
            CTkMessagebox(title="Error", message="Ingresa un valor válido para x", icon="cancel")

    def derivar(self):
        """Calcula la derivada"""
        coefs = self.leer_coeficientes()
        if coefs is None:
            return
        derivada = derivar_polinomio(coefs)
        equation = formatear_polinomio(derivada, latex=True)  # Asegúrate que tu función soporte latex
        self.update_result_display(f"f'(x) = {equation}", latex=True)
        self.update_status("✅ Derivada calculada", self.colors['accent_warning'])
        self.graficar_polinomio(derivada, title="Derivada f'(x)")

    def integrar(self):
        """Calcula la integral"""
        coefs = self.leer_coeficientes()
        if coefs is None:
            return
            
        integral = integrar_polinomio(coefs)
        equation = formatear_polinomio(integral, latex=True)  # <-- Usa latex=True
    
        result_text = f"\\int f(x)dx = {equation} + C"  # LaTeX para la integral
    
        self.update_result_display(result_text, latex=True)  # <-- Muestra como LaTeX
        self.update_status("✅ Integral calculada", self.colors['accent_success'])
        
        self.graficar_polinomio(integral, title="Integral ∫f(x)dx")

    def graficar_original(self):
        """Grafica el polinomio original"""
        coefs = self.leer_coeficientes()
        if coefs is None:
            return
            
        self.graficar_polinomio(coefs)
        self.update_status("✅ Gráfica generada", self.colors['accent_secondary'])

    def graficar_polinomio(self, coefs, eval_point=None, title="Polinomio f(x)"):
        """Visualización mejorada del polinomio"""
        # Limpiar frame anterior
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Configurar matplotlib con tema oscuro
        plt.style.use('dark_background')
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 8), facecolor=self.colors['bg_primary'])
        ax.set_facecolor(self.colors['bg_primary'])

        # Generar datos
        x = np.linspace(-10, 10, 1000)
        y = np.polyval(coefs, x)

        # Gráfica principal
        ax.plot(x, y, color='#7C3AED', linewidth=3, label=title, alpha=0.9)

        # Punto de evaluación si existe
        if eval_point:
            ax.plot(eval_point[0], eval_point[1], 'o', color='#10B981', 
                   markersize=12, label=f'f({eval_point[0]}) = {eval_point[1]:.3f}')
            ax.plot([eval_point[0], eval_point[0]], [0, eval_point[1]], 
                   '--', color='#10B981', alpha=0.7, linewidth=2)

        # Ejes y grid
        ax.axhline(0, color='#374151', linewidth=1.5, alpha=0.8)
        ax.axvline(0, color='#374151', linewidth=1.5, alpha=0.8)
        ax.grid(True, alpha=0.3, linestyle='--', color='#4B5563')

        # Estilo
        ax.set_xlabel("x", fontsize=14, color='white', fontweight='bold')
        ax.set_ylabel("f(x)", fontsize=14, color='white', fontweight='bold')
        ax.set_title(title, fontsize=16, color='white', fontweight='bold', pad=20)

        # Leyenda
        ax.legend(frameon=True, facecolor=self.colors['bg_secondary'], 
                 edgecolor='none', fontsize=12)

        # Límites adaptativos
        y_min, y_max = np.min(y), np.max(y)
        y_margin = (y_max - y_min) * 0.1
        ax.set_ylim(y_min - y_margin, y_max + y_margin)

        # Integrar con CustomTkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        self.canvas = canvas
        plt.close(fig)  # Limpiar memoria
    
    def mostrar_resultado_latex(self, latex_str):
        """Muestra el resultado en formato LaTeX usando matplotlib en el área de resultados"""
        # Limpiar el área de resultados
        for widget in self.result_display.winfo_children():
            widget.destroy()
        # Crear figura matplotlib
        fig, ax = plt.subplots(figsize=(7, 1.2), facecolor=self.colors['bg_primary'])
        ax.axis('off')
        ax.text(0.5, 0.5, f"${latex_str}$", fontsize=22, color='white', ha='center', va='center')
        fig.tight_layout(pad=0)
        # Mostrar en el área de resultados
        canvas = FigureCanvasTkAgg(fig, master=self.result_display)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)