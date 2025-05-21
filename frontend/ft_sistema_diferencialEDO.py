# UI/sistema_diferencial_page.py
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from backend.bk_sistema_diferencial import solve_system, eigen_decomposition

# Definir colores y estilos
DARK_BG = "#101117"      # Fondo principal más oscuro y elegante
PANEL_BG = "#1A1B26"     # Color de paneles
ACCENT = "#7B68EE"       # Color para acentos (violeta)
TEXT_COLOR = "#E0E0E0"   # Color de texto claro
SUBTITLE_COLOR = "#A0A0A0"  # Color para subtítulos

class SistemaDiferencialPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=DARK_BG)
        
        # Configurar colores para customtkinter
        ctk.set_appearance_mode("dark")
        
        # Crear un ScrollableFrame para contener toda la interfaz
        self.main_scrollable = ctk.CTkScrollableFrame(self,fg_color=DARK_BG, 
                                                     scrollbar_fg_color=PANEL_BG,
                                                     scrollbar_button_color=ACCENT,
                                                     scrollbar_button_hover_color="#634BD6")
        self.main_scrollable.pack(fill="both", expand=True)
        
        # Contenedor principal con margen
        container = ctk.CTkFrame(self.main_scrollable, fg_color=DARK_BG)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Encabezado elegante
        header_frame = ctk.CTkFrame(container, fg_color=DARK_BG, height=60)
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            header_frame, 
            text="ANÁLISIS DE SISTEMAS DIFERENCIALES", 
            font=("Helvetica", 26, "bold"),
            text_color="#6c63ff"

        ).pack(side="left", padx=10)
        
        # Icono decorativo
        ctk.CTkLabel(
            header_frame,
            text="🌀",
            font=("Arial", 26),
            text_color=ACCENT
        ).pack(side="right", padx=10)
        
         # Ejemplos
        example_frame = ctk.CTkFrame(container, fg_color=DARK_BG)
        example_frame.pack(fill="x", pady=(0,10))
        ctk.CTkLabel(
            example_frame, text="Ejemplos:",
            font=("Helvetica",14,"bold"), text_color=TEXT_COLOR
        ).pack(side="left", padx=(0,10))
        self.example_var = ctk.StringVar(value="Selecciona ejemplo")
        ctk.CTkOptionMenu(
            example_frame,
            values=["Selecciona ejemplo","Lineal simple","Oscilador armónico"],
            variable=self.example_var,
            command=self._load_example,
            width=200, height=35,
            fg_color="#0D0F18", button_color=ACCENT,
            button_hover_color="#634BD6",
            dropdown_fg_color="#0D0F18", text_color=TEXT_COLOR
        ).pack(side="left")

        
        
        # Panel de configuración
        input_container = ctk.CTkFrame(container, fg_color=DARK_BG)
        input_container.pack(fill="x", pady=10)
        
        # Panel de ecuaciones - con estilo
        self._create_equation_panel(input_container)
        
        # Panel de parámetros - en la misma fila
        self._create_parameters_panel(input_container)
        
        # Separador visual
        separator = ctk.CTkFrame(container, height=2, fg_color=ACCENT)
        separator.pack(fill="x", pady=15, padx=40)
        
        # Panel de resultados - diseño de dos columnas
        results_frame = ctk.CTkFrame(container, fg_color=DARK_BG)
        results_frame.pack(fill="both", expand=True, pady=10)
        results_frame.columnconfigure(0, weight=3)  # Da más espacio a la columna de la gráfica
        results_frame.columnconfigure(1, weight=2)
        results_frame.rowconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)  # Añadimos una segunda fila
        
        # Gráfica con panel decorativo - AMPLIADA
        plot_panel = ctk.CTkFrame(results_frame, fg_color=PANEL_BG, corner_radius=10)
        plot_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5, rowspan=2)  # Ahora abarca dos filas
        
        plot_header = ctk.CTkFrame(plot_panel, fg_color=PANEL_BG, height=40)
        plot_header.pack(fill="x", padx=10, pady=(10, 0))
        ctk.CTkLabel(
            plot_header, 
            text="Visualización Gráfica", 
            font=("Helvetica", 16, "bold"),
            text_color=TEXT_COLOR
        ).pack(side="left")
        
        self.plot_frame = ctk.CTkFrame(plot_panel, fg_color=PANEL_BG)
        self.plot_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Panel de resultados numéricos
        results_panel = ctk.CTkFrame(results_frame, fg_color=PANEL_BG, corner_radius=10)
        results_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(5, 5))
        
        results_header = ctk.CTkFrame(results_panel, fg_color=PANEL_BG, height=40)
        results_header.pack(fill="x", padx=10, pady=(10, 0))
        ctk.CTkLabel(
            results_header, 
            text="Resultados Numéricos", 
            font=("Helvetica", 16, "bold"),
            text_color=TEXT_COLOR
        ).pack(side="left")
        
        # Tabla de resultados con scroll independiente
        table_container = ctk.CTkFrame(results_panel, fg_color=PANEL_BG)
        table_container.pack(fill="both", expand=True, padx=15, pady=(5, 10))
        
        self.tabla_texto = ctk.CTkTextbox(
            table_container, 
            height=200, 
            corner_radius=5, 
            font=("Consolas", 12),
            fg_color="#0D0F18",
            text_color=TEXT_COLOR,
            border_width=1,
            border_color="#303446"
        )
        self.tabla_texto.pack(fill="both", expand=True, pady=5)
        self.tabla_texto.configure(wrap="none")
        
        # Panel de autovalores/vectores - Movido a la segunda fila
        eigen_panel = ctk.CTkFrame(results_frame, fg_color=PANEL_BG, corner_radius=10, height=100)
        eigen_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(5, 5))
        
        eigen_header = ctk.CTkFrame(eigen_panel, fg_color=PANEL_BG, height=40)
        eigen_header.pack(fill="x", padx=10, pady=(10, 0))
        ctk.CTkLabel(
            eigen_header, 
            text="Análisis de Autovalores y Autovectores", 
            font=("Helvetica", 16, "bold"),
            text_color=TEXT_COLOR
        ).pack(side="left")
        
        self.detalles_texto = ctk.CTkTextbox(
            eigen_panel, 
            height=80, 
            corner_radius=5, 
            font=("Consolas", 12),
            fg_color="#0D0F18",
            text_color=TEXT_COLOR,
            border_width=1,
            border_color="#303446"
        )
        self.detalles_texto.pack(fill="both", expand=True, padx=15, pady=15)
        self.detalles_texto.configure(wrap="none")
        
        # Indicador de scroll para ayudar al usuario
        scroll_hint = ctk.CTkLabel(
            container,
            text="⬇️ Desplaza hacia abajo para ver todos los resultados ⬇️",
            font=("Helvetica", 12),
            text_color=ACCENT
        )
        scroll_hint.pack(pady=(5, 0))
    def _load_example(self, choice: str):
        """Carga presets según el ejemplo seleccionado"""
        presets = {
            "Lineal simple": {
                "f1": "-x + 2*y",
                "f2": "-2*x - y",
                "x0": "1", "y0": "0",
                "T": "10", "h": "0.1",
                "method": "Analítico"
            },
            "Oscilador armónico": {
                "f1": "y",
                "f2": "-x",
                "x0": "0", "y0": "1",
                "T": "20", "h": "0.05",
                "method": "Runge-Kutta 4"
            }
        }
        if choice in presets:
            p = presets[choice]
            self.f1_entry.delete(0, "end"); self.f1_entry.insert(0, p["f1"])
            self.f2_entry.delete(0, "end"); self.f2_entry.insert(0, p["f2"])
            self.x0_entry.delete(0, "end"); self.x0_entry.insert(0, p["x0"])
            self.y0_entry.delete(0, "end"); self.y0_entry.insert(0, p["y0"])
            self.T_entry.delete(0, "end"); self.T_entry.insert(0, p["T"])
            self.h_entry.delete(0, "end"); self.h_entry.insert(0, p["h"])
            self.metodo_var.set(p["method"])  
    def _create_equation_panel(self, parent):
        equation_frame = ctk.CTkFrame(parent, fg_color=PANEL_BG, corner_radius=10)
        equation_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Título del panel
        title_frame = ctk.CTkFrame(equation_frame, fg_color=PANEL_BG, height=40)
        title_frame.pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkLabel(
            title_frame, 
            text="Ecuaciones del Sistema", 
            font=("Helvetica", 16, "bold"),
            text_color=TEXT_COLOR
        ).pack(side="left")
        
        # Panel para las ecuaciones
        eq_content = ctk.CTkFrame(equation_frame, fg_color=PANEL_BG)
        eq_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Ecuación 1
        eq1_frame = ctk.CTkFrame(eq_content, fg_color=PANEL_BG, height=40)
        eq1_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            eq1_frame, 
            text="dx/dt  =", 
            font=("Helvetica", 14),
            text_color=TEXT_COLOR,
            width=60
        ).pack(side="left", padx=(5, 10))
        
        self.f1_entry = ctk.CTkEntry(
            eq1_frame, 
            height=35, 
            corner_radius=5,
            fg_color="#0D0F18",
            text_color=TEXT_COLOR,
            border_color=ACCENT,
            border_width=1
        )
        self.f1_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Ecuación 2
        eq2_frame = ctk.CTkFrame(eq_content, fg_color=PANEL_BG, height=40)
        eq2_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            eq2_frame, 
            text="dy/dt  =", 
            font=("Helvetica", 14),
            text_color=TEXT_COLOR,
            width=60
        ).pack(side="left", padx=(5, 10))
        
        self.f2_entry = ctk.CTkEntry(
            eq2_frame, 
            height=35, 
            corner_radius=5,
            fg_color="#0D0F18",
            text_color=TEXT_COLOR,
            border_color=ACCENT,
            border_width=1
        )
        self.f2_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Condiciones iniciales
        cond_frame = ctk.CTkFrame(eq_content, fg_color=PANEL_BG)
        cond_frame.pack(fill="x", pady=(15, 5))
        
        ctk.CTkLabel(
            cond_frame, 
            text="Condiciones Iniciales:", 
            font=("Helvetica", 14, "bold"),
            text_color=SUBTITLE_COLOR
        ).pack(side="left", padx=5)
        
        # Valores iniciales en una fila
        init_frame = ctk.CTkFrame(eq_content, fg_color=PANEL_BG)
        init_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            init_frame, 
            text="x(0) =", 
            font=("Helvetica", 14),
            text_color=TEXT_COLOR,
            width=60
        ).pack(side="left", padx=5)
        
        self.x0_entry = ctk.CTkEntry(
            init_frame, 
            height=35, 
            width=80, 
            corner_radius=5,
            fg_color="#0D0F18",
            text_color=TEXT_COLOR,
            border_color=ACCENT,
            border_width=1
        )
        self.x0_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(
            init_frame, 
            text="y(0) =", 
            font=("Helvetica", 14),
            text_color=TEXT_COLOR,
            width=60
        ).pack(side="left", padx=5)
        
        self.y0_entry = ctk.CTkEntry(
            init_frame, 
            height=35, 
            width=80, 
            corner_radius=5,
            fg_color="#0D0F18",
            text_color=TEXT_COLOR,
            border_color=ACCENT,
            border_width=1
        )
        self.y0_entry.pack(side="left", padx=5)

    def _create_parameters_panel(self, parent):
        param_frame = ctk.CTkFrame(parent, fg_color=PANEL_BG, corner_radius=10)
        param_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Título del panel
        title_frame = ctk.CTkFrame(param_frame, fg_color=PANEL_BG, height=40)
        title_frame.pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkLabel(
            title_frame, 
            text="Parámetros de Resolución", 
            font=("Helvetica", 16, "bold"),
            text_color=TEXT_COLOR
        ).pack(side="left")
        
        # Panel para los parámetros
        param_content = ctk.CTkFrame(param_frame, fg_color=PANEL_BG)
        param_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Parámetros de tiempo
        time_frame = ctk.CTkFrame(param_content, fg_color=PANEL_BG)
        time_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            time_frame, 
            text="Tiempo Total T =", 
            font=("Helvetica", 14),
            text_color=TEXT_COLOR,
            width=120
        ).pack(side="left", padx=(5, 10))
        
        self.T_entry = ctk.CTkEntry(
            time_frame, 
            height=35, 
            width=100, 
            corner_radius=5,
            fg_color="#0D0F18",
            text_color=TEXT_COLOR,
            border_color=ACCENT,
            border_width=1
        )
        self.T_entry.pack(side="left", padx=5)
        
        # Paso de integración
        step_frame = ctk.CTkFrame(param_content, fg_color=PANEL_BG)
        step_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            step_frame, 
            text="Paso h =", 
            font=("Helvetica", 14),
            text_color=TEXT_COLOR,
            width=120
        ).pack(side="left", padx=(5, 10))
        
        self.h_entry = ctk.CTkEntry(
            step_frame, 
            height=35, 
            width=100, 
            corner_radius=5,
            fg_color="#0D0F18",
            text_color=TEXT_COLOR,
            border_color=ACCENT,
            border_width=1
        )
        self.h_entry.pack(side="left", padx=5)
        
        # Método de resolución
        method_frame = ctk.CTkFrame(param_content, fg_color=PANEL_BG)
        method_frame.pack(fill="x", pady=(15, 5))
        
        ctk.CTkLabel(
            method_frame, 
            text="Método de Resolución:", 
            font=("Helvetica", 14, "bold"),
            text_color=SUBTITLE_COLOR
        ).pack(side="left", padx=5)
        
        # Selector de método
        method_selector = ctk.CTkFrame(param_content, fg_color=PANEL_BG)
        method_selector.pack(fill="x", pady=5)
        
        self.metodo_var = ctk.StringVar(value="Euler")
        ctk.CTkOptionMenu(
            method_selector, 
            values=["Euler", "Runge-Kutta 4", "Analítico"], 
            variable=self.metodo_var,
            width=180,
            height=35,
            corner_radius=5,
            fg_color="#0D0F18",
            button_color=ACCENT,
            button_hover_color="#634BD6",
            dropdown_fg_color="#0D0F18",
            dropdown_hover_color="#1D1F2F",
            dropdown_text_color=TEXT_COLOR,
            text_color=TEXT_COLOR
        ).pack(side="left", padx=5)
        
        # Botón de acción
        action_frame = ctk.CTkFrame(param_content, fg_color=PANEL_BG)
        action_frame.pack(fill="x", pady=(20, 5))
        
        ctk.CTkButton(
            action_frame, 
            text="RESOLVER SISTEMA", 
            command=self.resolver,
            height=40,
            corner_radius=5,
            fg_color=ACCENT,
            hover_color="#634BD6",
            font=("Helvetica", 14, "bold")
        ).pack(fill="x", padx=5)

    def resolver(self):
        try:
            f1 = self.f1_entry.get().strip()
            f2 = self.f2_entry.get().strip()
            x0, y0 = float(self.x0_entry.get()), float(self.y0_entry.get())
            T, h = float(self.T_entry.get()), float(self.h_entry.get())
            metodo = self.metodo_var.get()

            t, x_vals, y_vals = solve_system(f1, f2, x0, y0, T, h, metodo)
            self._plot(t, x_vals, y_vals)
            self._mostrar_tabla(t, x_vals, y_vals)

            vals, vecs = eigen_decomposition(f1, f2)
            self._mostrar_detalles(vals, vecs)
            
            # Desplazar automáticamente hacia la gráfica y resultados
            self.after(300, lambda: self._scroll_to_results())
            
        except Exception as e:
            CTkMessagebox(
                title="Error", 
                message=str(e), 
                icon="cancel", 
                option_1="Entendido"
            )

    def _plot(self, t, x_vals, y_vals):
        # Limpiar plot anterior
        for w in self.plot_frame.winfo_children(): w.destroy()
        
        # Crear figura con estilo moderno - TAMAÑO AUMENTADO
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 6), facecolor=PANEL_BG)  # Tamaño aumentado
        
        # Graficar con colores elegantes y marcadores más visibles
        ax.plot(t, x_vals, label="x(t)", marker="o", color="#00BFFF", markersize=6, linewidth=2.5)
        ax.plot(t, y_vals, label="y(t)", marker="s", color="#FF69B4", markersize=6, linewidth=2.5)
        
        # Personalizar gráfica con mejores etiquetas
        ax.set_title("Evolución Temporal del Sistema", color=TEXT_COLOR, fontsize=14)
        ax.set_xlabel("Tiempo (t)", color=TEXT_COLOR, fontsize=12)
        ax.set_ylabel("Valores", color=TEXT_COLOR, fontsize=12)
        ax.tick_params(colors=TEXT_COLOR, labelsize=10)  # Etiquetas de ejes más grandes
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Personalizar leyenda con mejor tamaño
        legend = ax.legend(frameon=True, fontsize=12)
        frame = legend.get_frame()
        frame.set_facecolor('#1D1F2F')
        frame.set_edgecolor(ACCENT)
        
        # Ajustar apariencia global
        plt.tight_layout()
        
        # Mostrar en canvas
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
        
        # Guardar referencias
        self.canvas = canvas
        self.fig = fig
        
        # Asegurar que el scroll se actualice después de mostrar la gráfica
        self.after(100, self._update_scroll)

    def _update_scroll(self):
        """Actualiza el área scrollable para reflejar el nuevo contenido"""
        self.main_scrollable.update()
        self.update()
        
    def _scroll_to_results(self):
  
        self.main_scrollable._parent_canvas.yview_moveto(0.3)
        
    def _mostrar_tabla(self, t, x, y):
        self.tabla_texto.delete("0.0", "end")
        
        # Encabezado con formato
        self.tabla_texto.insert("end", f"{'t':<10}{'x(t)':<15}{'y(t)':<15}\n")
        self.tabla_texto.insert("end", '─'*40 + "\n")
        
        # Datos con formato consistente
        for i in range(len(t)):
            self.tabla_texto.insert("end", f"{t[i]:<10.4f}{x[i]:<15.6f}{y[i]:<15.6f}\n")
        
        # Agregar un botón para exportar datos si hay muchos puntos
        if len(t) > 10:
            self.tabla_texto.insert("end", "\n📋 Los datos pueden desplazarse con la barra de scroll ➡️\n")

    def _mostrar_detalles(self, vals, vecs):
        self.detalles_texto.delete("0.0", "end")
        
        # Titulo informativo
        self.detalles_texto.insert("end", "Análisis de Estabilidad del Sistema:\n")
        self.detalles_texto.insert("end", '─'*50 + "\n")
        
        # Mostrar autovalores y autovectores con formato mejorado
        for i, val in enumerate(vals):
            v = vecs[:,i]
            tipo = ""
            if isinstance(val, complex):
                tipo = "complejo"
            elif val > 0:
                tipo = "inestable"
            elif val < 0:
                tipo = "estable"
            else:
                tipo = "crítico"
                
            self.detalles_texto.insert("end", f"λ{i+1} = {val:.6f} ({tipo}), ")
            self.detalles_texto.insert("end", f"autovector = [{v[0]:.4f}, {v[1]:.4f}]\n")