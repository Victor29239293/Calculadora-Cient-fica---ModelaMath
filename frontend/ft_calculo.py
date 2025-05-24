import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib as mpl
from backend.bk_calculo import (
    derivar_funcion_pasos,
    integrar_funcion,
    generar_datos_grafica
)
import re

# Paleta de colores moderna
class ColorScheme:
    DARK_BG = "#0B0D15"
    PANEL_BG = "#161B26"
    CARD_BG = "#1E2532"
    SURFACE_BG = "#252D3D"
    ACCENT_PRIMARY = "#6366F1"
    ACCENT_SECONDARY = "#8B5CF6"
    ACCENT_HOVER = "#4F46E5"
    TEXT_PRIMARY = "#F8FAFC"
    TEXT_SECONDARY = "#CBD5E1"
    TEXT_MUTED = "#94A3B8"
    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    ERROR = "#EF4444"
    BORDER = "#334155"
    GRAPH_LINE = "#00D9FF"

class CalculoPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=ColorScheme.DARK_BG)
        
        # Configurar matplotlib con tema oscuro mejorado
        self._setup_matplotlib()
        
        # Crear layout principal
        self._create_layout()
        
        # Variables para canvas
        self.canvas_resultado = None
        self.latex_frame = None

    def _setup_matplotlib(self):
        """Configurar matplotlib con tema oscuro personalizado"""
        plt.style.use('dark_background')
        mpl.rcParams.update({
            'figure.facecolor': ColorScheme.CARD_BG,
            'axes.facecolor': ColorScheme.SURFACE_BG,
            'text.color': ColorScheme.TEXT_PRIMARY,
            'axes.edgecolor': ColorScheme.BORDER,
            'axes.labelcolor': ColorScheme.TEXT_SECONDARY,
            'xtick.color': ColorScheme.TEXT_SECONDARY,
            'ytick.color': ColorScheme.TEXT_SECONDARY,
            'grid.color': ColorScheme.BORDER,
            'grid.alpha': 0.3
        })

    def _create_layout(self):
        """Crear el layout principal de la aplicación"""
        # Scrollable container principal
        self.scrollable = ctk.CTkScrollableFrame(
            self, 
            fg_color=ColorScheme.DARK_BG,
            scrollbar_button_color=ColorScheme.ACCENT_PRIMARY,
            scrollbar_button_hover_color=ColorScheme.ACCENT_HOVER
        )
        self.scrollable.pack(fill="both", expand=True, padx=10, pady=10)

        # Header con gradiente visual
        self._create_header()
        
        # Sección de entrada principal
        self._create_input_section()
        
        # Botones de acción
        self._create_action_buttons()
        
        # Sección de resultados
        self._create_results_section()
        
        # Sección de gráficas
        self._create_graph_section()

    def _create_header(self):
        """Crear header con diseño moderno"""
        header = ctk.CTkFrame(
            self.scrollable, 
            fg_color=ColorScheme.PANEL_BG, 
            height=100, 
            corner_radius=20,
            border_width=1,
            border_color=ColorScheme.BORDER
        )
        header.pack(fill="x", padx=15, pady=(0, 20))
        header.pack_propagate(False)
        
        # Contenedor interno para mejor centrado
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True)
        
        # Título principal con icono
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(expand=True)
        
        ctk.CTkLabel(
            title_frame,
            text="∇ Calculadora de Cálculo Simbólico",
            font=("Segoe UI", 28, "bold"),
            text_color=ColorScheme.ACCENT_PRIMARY
        ).pack(pady=15)
        
        ctk.CTkLabel(
            title_frame,
            text="Derivadas • Integrales • Gráficas",
            font=("Segoe UI", 14),
            text_color=ColorScheme.TEXT_MUTED
        ).pack()

    def _create_input_section(self):
        """Crear sección de entrada mejorada"""
        input_card = ctk.CTkFrame(
            self.scrollable, 
            fg_color=ColorScheme.CARD_BG, 
            corner_radius=16,
            border_width=1,
            border_color=ColorScheme.BORDER
        )
        input_card.pack(fill="x", padx=15, pady=(0, 20))

        # Título de la sección
        section_title = ctk.CTkFrame(input_card, fg_color="transparent")
        section_title.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            section_title,
            text="📝 Definir Función",
            font=("Segoe UI", 18, "bold"),
            text_color=ColorScheme.TEXT_PRIMARY
        ).pack(anchor="w")

        # Campo de función principal
        func_frame = ctk.CTkFrame(input_card, fg_color="transparent")
        func_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            func_frame,
            text="f(x) =",
            font=("Segoe UI", 16, "bold"),
            text_color=ColorScheme.ACCENT_PRIMARY,
            width=60
        ).pack(side="left", padx=(0, 15))
        
        self.entrada = ctk.CTkEntry(
            func_frame,
            placeholder_text="Ejemplo: x**2 + 3*x + sin(x)",
            height=45,
            font=("JetBrains Mono", 14),
            fg_color=ColorScheme.SURFACE_BG,
            border_color=ColorScheme.BORDER,
            placeholder_text_color=ColorScheme.TEXT_MUTED,
            text_color=ColorScheme.TEXT_PRIMARY
        )
        self.entrada.pack(side="left", fill="x", expand=True)

        # Separador visual
        separator = ctk.CTkFrame(
            input_card, 
            fg_color=ColorScheme.BORDER, 
            height=1
        )
        separator.pack(fill="x", padx=40, pady=15)

        # Sección de límites mejorada
        limits_title = ctk.CTkFrame(input_card, fg_color="transparent")
        limits_title.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(
            limits_title,
            text="🎯 Límites de integración (opcional)",
            font=("Segoe UI", 16, "bold"),
            text_color=ColorScheme.TEXT_PRIMARY
        ).pack(anchor="w")

        limits_frame = ctk.CTkFrame(input_card, fg_color="transparent")
        limits_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Límite inferior
        lower_frame = ctk.CTkFrame(limits_frame, fg_color="transparent")
        lower_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            lower_frame,
            text="Límite inferior:",
            font=("Segoe UI", 12),
            text_color=ColorScheme.TEXT_SECONDARY
        ).pack(anchor="w", pady=(0, 5))
        
        self.lim_a = ctk.CTkEntry(
            lower_frame,
            placeholder_text="a",
            height=35,
            font=("JetBrains Mono", 12),
            fg_color=ColorScheme.SURFACE_BG,
            border_color=ColorScheme.BORDER,
            placeholder_text_color=ColorScheme.TEXT_MUTED
        )
        self.lim_a.pack(fill="x")
        
        # Límite superior
        upper_frame = ctk.CTkFrame(limits_frame, fg_color="transparent")
        upper_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(
            upper_frame,
            text="Límite superior:",
            font=("Segoe UI", 12),
            text_color=ColorScheme.TEXT_SECONDARY
        ).pack(anchor="w", pady=(0, 5))
        
        self.lim_b = ctk.CTkEntry(
            upper_frame,
            placeholder_text="b",
            height=35,
            font=("JetBrains Mono", 12),
            fg_color=ColorScheme.SURFACE_BG,
            border_color=ColorScheme.BORDER,
            placeholder_text_color=ColorScheme.TEXT_MUTED
        )
        self.lim_b.pack(fill="x")

    def _create_action_buttons(self):
        """Crear botones de acción con diseño moderno"""
        buttons_card = ctk.CTkFrame(
            self.scrollable,
            fg_color=ColorScheme.CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=ColorScheme.BORDER
        )
        buttons_card.pack(fill="x", padx=15, pady=(0, 20))

        ctk.CTkLabel(
            buttons_card,
            text="⚡ Operaciones",
            font=("Segoe UI", 18, "bold"),
            text_color=ColorScheme.TEXT_PRIMARY
        ).pack(pady=(20, 15))

        buttons_frame = ctk.CTkFrame(buttons_card, fg_color="transparent")
        buttons_frame.pack(pady=(0, 20))

        # Configurar grid
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Botón Derivar
        derivar_btn = ctk.CTkButton(
            buttons_frame,
            text="📈 Derivar",
            command=self.derivar,
            width=160,
            height=50,
            font=("Segoe UI", 14, "bold"),
            fg_color=ColorScheme.ACCENT_PRIMARY,
            hover_color=ColorScheme.ACCENT_HOVER,
            corner_radius=12,
            border_width=1,
            border_color=ColorScheme.ACCENT_SECONDARY
        )
        derivar_btn.grid(row=0, column=0, padx=15, pady=5)

        # Botón Integrar
        integrar_btn = ctk.CTkButton(
            buttons_frame,
            text="∫ Integrar",
            command=self.integrar,
            width=160,
            height=50,
            font=("Segoe UI", 14, "bold"),
            fg_color=ColorScheme.ACCENT_SECONDARY,
            hover_color=ColorScheme.ACCENT_HOVER,
            corner_radius=12,
            border_width=1,
            border_color=ColorScheme.ACCENT_PRIMARY
        )
        integrar_btn.grid(row=0, column=1, padx=15, pady=5)

        # Botón Graficar
        graficar_btn = ctk.CTkButton(
            buttons_frame,
            text="📊 Graficar",
            command=self.graficar,
            width=160,
            height=50,
            font=("Segoe UI", 14, "bold"),
            fg_color=ColorScheme.SUCCESS,
            hover_color="#059669",
            corner_radius=12,
            border_width=1,
            border_color="#10B981"
        )
        graficar_btn.grid(row=0, column=2, padx=15, pady=5)

    def _create_results_section(self):
        """Crear sección de resultados mejorada"""
        self.resultado_frame = ctk.CTkFrame(
            self.scrollable,
            fg_color=ColorScheme.CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=ColorScheme.BORDER
        )
        self.resultado_frame.pack(fill="both", expand=True, padx=15, pady=(0, 20))

        # Header de resultados
        result_header = ctk.CTkFrame(self.resultado_frame, fg_color="transparent")
        result_header.pack(fill="x", padx=20, pady=(20, 10))

        self.resultado_titulo = ctk.CTkLabel(
            result_header,
            text="📋 Resultado",
            font=("Segoe UI", 20, "bold"),
            text_color=ColorScheme.ACCENT_PRIMARY
        )
        self.resultado_titulo.pack(anchor="w")

        # Contenedor de resultados
        self.resultado_contenedor = ctk.CTkFrame(
            self.resultado_frame,
            fg_color=ColorScheme.SURFACE_BG,
            corner_radius=12,
            border_width=1,
            border_color=ColorScheme.BORDER
        )
        self.resultado_contenedor.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Textbox de resultados
        self.resultado = ctk.CTkTextbox(
            self.resultado_contenedor,
            height=130,
            font=("JetBrains Mono", 13),
            wrap="word",
            fg_color=ColorScheme.SURFACE_BG,
            text_color=ColorScheme.TEXT_PRIMARY,
            border_width=0,
            scrollbar_button_color=ColorScheme.ACCENT_PRIMARY,
            scrollbar_button_hover_color=ColorScheme.ACCENT_HOVER
        )
        self.resultado.pack(fill="both", expand=True, padx=15, pady=15)
        self.resultado.configure(state="disabled")

    def _create_graph_section(self):
        """Crear sección de gráficas"""
        self.canvas_frame = ctk.CTkFrame(
            self.scrollable,
            fg_color=ColorScheme.CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=ColorScheme.BORDER
        )
        self.canvas_frame.pack(fill="both", expand=True, padx=15, pady=(0, 20))

    def mostrar(self, texto: str):
        """Mostrar texto en el área de resultados"""
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("end", texto)
        self.resultado.configure(state="disabled")
        
        resultado_final = self.extraer_resultado_final(texto)
        if resultado_final:
            self.mostrar_latex(resultado_final)

    def extraer_resultado_final(self, texto: str):
        """Extraer el resultado final del texto"""
        resultado_match = re.search(r"✅ Resultado: (.+)$", texto)
        if resultado_match:
            return resultado_match.group(1)
        return None

    def derivar(self):
        """Calcular derivada de la función"""
        expr = self.entrada.get().strip()
        if not expr:
            CTkMessagebox(
                title="⚠️ Advertencia",
                message="Por favor, ingresa una función válida.",
                icon="warning"
            )
            return
        
        try:
            self.limpiar_canvas_resultado()
            derivada, pasos = derivar_funcion_pasos(expr)
            self.mostrar(pasos + f"\n\n✅ Resultado: {derivada}")
            self.resultado_titulo.configure(text="📈 Resultado de la Derivada")
        except Exception as e:
            CTkMessagebox(
                title="❌ Error",
                message=f"Error al calcular la derivada:\n{str(e)}",
                icon="cancel"
            )

    def integrar(self):
        """Calcular integral de la función"""
        expr = self.entrada.get().strip()
        if not expr:
            CTkMessagebox(
                title="⚠️ Advertencia", 
                message="Por favor, ingresa una función válida.",
                icon="warning"
            )
            return
        
        a, b = self.lim_a.get().strip(), self.lim_b.get().strip()
        
        try:
            self.limpiar_canvas_resultado()
            resultado, pasos = integrar_funcion(expr, a or None, b or None)
            self.mostrar(pasos + f"\n\n✅ Resultado: {resultado}")
            
            if a and b:
                self.resultado_titulo.configure(text=f"∫ Integral Definida [{a}, {b}]")
            else:
                self.resultado_titulo.configure(text="∫ Integral Indefinida")
        except Exception as e:
            CTkMessagebox(
                title="❌ Error",
                message=f"Error al calcular la integral:\n{str(e)}",
                icon="cancel"
            )

    def graficar(self):
        """Generar gráfica de la función"""
        expr = self.entrada.get().strip()
        if not expr:
            CTkMessagebox(
                title="⚠️ Advertencia",
                message="Por favor, ingresa una función válida.",
                icon="warning"
            )
            return
        
        # Limpiar canvas anterior
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
            
        try:
            xs, ys = generar_datos_grafica(expr)
        except Exception as e:
            CTkMessagebox(
                title="❌ Error",
                message=f"Error al generar la gráfica:\n{str(e)}",
                icon="cancel"
            )
            return

        # Header de la gráfica
        graph_header = ctk.CTkFrame(self.canvas_frame, fg_color="transparent")
        graph_header.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            graph_header,
            text="📊 Gráfica de la Función",
            font=("Segoe UI", 20, "bold"),
            text_color=ColorScheme.ACCENT_PRIMARY
        ).pack(anchor="w")
        
        # Contenedor del canvas
        canvas_container = ctk.CTkFrame(
            self.canvas_frame,
            fg_color=ColorScheme.SURFACE_BG,
            corner_radius=12,
            border_width=1,
            border_color=ColorScheme.BORDER
        )
        canvas_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Crear figura con mejor diseño
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        fig.patch.set_facecolor(ColorScheme.CARD_BG)
        ax.set_facecolor(ColorScheme.SURFACE_BG)
        
        # Plot principal
        ax.plot(xs, ys, color=ColorScheme.GRAPH_LINE, linewidth=3, alpha=0.9)
        
        # Ejes y grid
        ax.axhline(0, color=ColorScheme.TEXT_MUTED, linewidth=1, alpha=0.7)
        ax.axvline(0, color=ColorScheme.TEXT_MUTED, linewidth=1, alpha=0.7)
        ax.grid(True, linestyle="--", color=ColorScheme.BORDER, alpha=0.5)
        
        # Estilo de la gráfica
        ax.set_title(f"f(x) = {expr}", fontsize=16, pad=20, color=ColorScheme.TEXT_PRIMARY, weight="bold")
        ax.set_xlabel("x", fontsize=14, color=ColorScheme.TEXT_SECONDARY, labelpad=10)
        ax.set_ylabel("f(x)", fontsize=14, color=ColorScheme.TEXT_SECONDARY, labelpad=10)
        
        # Personalizar ticks
        ax.tick_params(colors=ColorScheme.TEXT_MUTED, labelsize=10)
        
        # Mejorar layout
        plt.tight_layout(pad=2.0)
        
        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=canvas_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)

    def limpiar_canvas_resultado(self):
        """Limpiar canvas de resultados LaTeX"""
        if self.canvas_resultado:
            self.canvas_resultado.get_tk_widget().destroy()
            self.canvas_resultado = None
        if hasattr(self, "latex_frame") and self.latex_frame is not None:
            self.latex_frame.destroy()
            self.latex_frame = None

    def mostrar_latex(self, expresion_latex, titulo="Resultado"):
        """Mostrar expresión en formato LaTeX con diseño mejorado"""
        self.limpiar_canvas_resultado()

        # Crear frame para LaTeX
        self.latex_frame = ctk.CTkFrame(
            self.resultado_contenedor,
            fg_color=ColorScheme.PANEL_BG,
            corner_radius=10,
            border_width=1,
            border_color=ColorScheme.BORDER
        )
        self.latex_frame.pack(fill="x", padx=15, pady=(15, 0))

        # Título del LaTeX
        latex_title = ctk.CTkLabel(
            self.latex_frame,
            text="🧮 Expresión Matemática",
            font=("Segoe UI", 14, "bold"),
            text_color=ColorScheme.TEXT_SECONDARY
        )
        latex_title.pack(pady=(10, 0))

        # Figura para LaTeX
        fig, ax = plt.subplots(figsize=(8, 2), dpi=100)
        fig.patch.set_facecolor(ColorScheme.PANEL_BG)
        ax.set_facecolor(ColorScheme.PANEL_BG)
        
        # Renderizar LaTeX
        ax.text(
            0.5, 0.5, f"${expresion_latex}$",
            fontsize=20,
            ha="center",
            va="center",
            color=ColorScheme.GRAPH_LINE,
            weight="bold",
            transform=ax.transAxes
        )
        ax.axis("off")
        
        plt.tight_layout()

        # Canvas para LaTeX
        self.canvas_resultado = FigureCanvasTkAgg(fig, master=self.latex_frame)
        self.canvas_resultado.draw()
        self.canvas_resultado.get_tk_widget().pack(fill="both", expand=True, pady=(0, 15))