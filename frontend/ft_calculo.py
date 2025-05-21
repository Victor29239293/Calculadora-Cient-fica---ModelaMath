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
DARK_BG = "#101117"
PANEL_BG = "#1A1B26"
ACCENT = "#7B68EE"
class CalculoPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#1f1f1f")
        
        # Scrollable principal
        self.scrollable = ctk.CTkScrollableFrame(self, fg_color="#1f1f1f")
        self.scrollable.pack(fill="both", expand=True)

        # Configuración de estilo para matplotlib
        plt.style.use('dark_background')
        mpl.rcParams['text.color'] = '#f0f0f0'
        mpl.rcParams['axes.edgecolor'] = '#555555'
        mpl.rcParams['axes.labelcolor'] = '#f0f0f0'
        mpl.rcParams['xtick.color'] = '#dddddd'
        mpl.rcParams['ytick.color'] = '#dddddd'

        # Cabecera con título
        header = ctk.CTkFrame(self.scrollable, fg_color="#23272a", height=80, corner_radius=15)
        header.pack(fill="x", padx=20, pady=15)
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="📚 Módulo de Cálculo Simbólico",
            font=("Segoe UI", 26, "bold"),
            text_color="#6c63ff"
        ).pack(pady=20)

        # Frame para la entrada
        frame = ctk.CTkFrame(self.scrollable, fg_color="#23272a", corner_radius=12)
        frame.pack(pady=10, padx=20, fill="x")

        # Entrada principal con icono
        entrada_frame = ctk.CTkFrame(frame, fg_color="transparent")
        entrada_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=12, sticky="ew")
        
        ctk.CTkLabel(
            entrada_frame, 
            text="f(x) =", 
            font=("Segoe UI", 16, "bold"),
            text_color="#6c63ff"
        ).pack(side="left", padx=(5, 0))
        
        self.entrada = ctk.CTkEntry(
            entrada_frame,
            placeholder_text="Ejemplo: x**2 + 3*x",
            width=480,
            height=35,
            font=("Consolas", 14)
        )
        self.entrada.pack(side="left", padx=10, fill="x", expand=True)

        # Límites de integración
        limites_frame = ctk.CTkFrame(frame, fg_color="transparent")
        limites_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 12), sticky="ew")
        
        ctk.CTkLabel(limites_frame, text="Límites:", font=("Segoe UI", 14)).pack(side="left", padx=(5, 10))
        
        self.lim_a = ctk.CTkEntry(limites_frame, placeholder_text="a (inferior)", width=180, font=("Consolas", 13))
        self.lim_a.pack(side="left", padx=10)
        
        self.lim_b = ctk.CTkEntry(limites_frame, placeholder_text="b (superior)", width=180, font=("Consolas", 13))
        self.lim_b.pack(side="left", padx=10)
        
        # Frame para los botones
        btns = ctk.CTkFrame(self.scrollable, fg_color="transparent")
        btns.pack(pady=15)

        # Botones con estilo mejorado
        derivar_btn = ctk.CTkButton(
            btns, 
            text="📈 Derivar", 
            command=self.derivar, 
            width=150,
            height=40,
            font=("Segoe UI", 14, "bold"),
            fg_color="#6c63ff",
            hover_color="#5a52d5"
        )
        derivar_btn.grid(row=0, column=0, padx=10)
        
        integrar_btn = ctk.CTkButton(
            btns, 
            text="∫ Integrar", 
            command=self.integrar, 
            width=150,
            height=40,
            font=("Segoe UI", 14, "bold"),
            fg_color="#6c63ff",
            hover_color="#5a52d5"
        )
        integrar_btn.grid(row=0, column=1, padx=10)
        
        graficar_btn = ctk.CTkButton(
            btns, 
            text="📊 Graficar", 
            command=self.graficar, 
            width=150,
            height=40,
            font=("Segoe UI", 14, "bold"),
            fg_color="#6c63ff",
            hover_color="#5a52d5"
        )
        graficar_btn.grid(row=0, column=2, padx=10)

        # Frame para el resultado
        self.resultado_frame = ctk.CTkFrame(self.scrollable, fg_color="#292d32", corner_radius=15)
        self.resultado_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Título del resultado
        self.resultado_titulo = ctk.CTkLabel(
            self.resultado_frame,
            text="Resultado",
            font=("Segoe UI", 18, "bold"),
            text_color="#6c63ff"
        )
        self.resultado_titulo.pack(pady=(10, 0))
        
        # Contenedor de resultado
        self.resultado_contenedor = ctk.CTkFrame(self.resultado_frame, fg_color="#1e1e1e", corner_radius=8)
        self.resultado_contenedor.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Área de texto para mostrar resultados
        self.resultado = ctk.CTkTextbox(
            self.resultado_contenedor,
            height=200,
            font=("Consolas", 14),
            wrap="word",
            fg_color="#1e1e1e",
            text_color="#f0f0f0"
        )
        self.resultado.pack(fill="both", expand=True, padx=10, pady=10)
        self.resultado.configure(state="disabled")

        # Área para gráficas
        self.canvas_frame = ctk.CTkFrame(self.scrollable, fg_color="#292d32", corner_radius=15)
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Variables para el canvas
        self.canvas_resultado = None
        self.fig_latex = None
        self.ax_latex = None

    def mostrar(self, texto: str):
        """Muestra texto en el área de resultados"""
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("end", texto)
        self.resultado.configure(state="disabled")
        
        # Extraer el resultado final para mostrar en LaTeX
        resultado_final = self.extraer_resultado_final(texto)
        if resultado_final:
            self.mostrar_latex(resultado_final)

    def extraer_resultado_final(self, texto: str):
        """Extrae el resultado final de los pasos"""
        # Buscar el resultado final
        resultado_match = re.search(r"✅ Resultado: (.+)$", texto)
        if resultado_match:
            return resultado_match.group(1)
        return None

    def derivar(self):
        expr = self.entrada.get().strip()
        if not expr:
            CTkMessagebox(title="Error", message="Ingresa una función.", icon="warning")
            return
        try:
            self.limpiar_canvas_resultado()
            derivada, pasos = derivar_funcion_pasos(expr)
            self.mostrar(pasos + f"\n\n✅ Resultado: {derivada}")
            self.resultado_titulo.configure(text="Resultado de la Derivada")
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

    def integrar(self):
        expr = self.entrada.get().strip()
        if not expr:
            CTkMessagebox(title="Error", message="Ingresa una función.", icon="warning")
            return
        a, b = self.lim_a.get().strip(), self.lim_b.get().strip()
        try:
            self.limpiar_canvas_resultado()
            resultado, pasos = integrar_funcion(expr, a or None, b or None)
            self.mostrar(pasos + f"\n\n✅ Resultado: {resultado}")
            
            # Actualizar título según el tipo de integración
            if a and b:
                self.resultado_titulo.configure(text=f"Integral Definida de {a} a {b}")
            else:
                self.resultado_titulo.configure(text="Integral Indefinida")
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

    def graficar(self):
        expr = self.entrada.get().strip()
        if not expr:
            CTkMessagebox(title="Error", message="Ingresa una función.", icon="warning")
            return
        
        # Limpiar área de gráfica
        for w in self.canvas_frame.winfo_children():
            w.destroy()
            
        try:
            xs, ys = generar_datos_grafica(expr)
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")
            return
            
        # Crear gráfica con estilo mejorado
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100, facecolor="#292d32")
        ax.set_facecolor("#1e1e1e")
        
        # Graficar función con estilo profesional
        ax.plot(xs, ys, color="#00ffff", linewidth=2.5)
        
        # Ejes y grid mejorados
        ax.axhline(0, color="#666666", linewidth=0.8)
        ax.axvline(0, color="#666666", linewidth=0.8)
        ax.grid(True, linestyle=":", color="#444444", alpha=0.7)
        
        # Título y etiquetas
        ax.set_title(f"f(x) = {expr}", fontsize=14, pad=10)
        ax.set_xlabel("x", fontsize=12, labelpad=8)
        ax.set_ylabel("f(x)", fontsize=12, labelpad=8)
        
        # Añadir la gráfica al contenedor
        title_label = ctk.CTkLabel(
            self.canvas_frame, 
            text="Gráfica de la Función",
            font=("Segoe UI", 18, "bold"),
            text_color="#6c63ff"
        )
        title_label.pack(pady=(10, 0))
        
        canvas_container = ctk.CTkFrame(self.canvas_frame, fg_color="#1e1e1e", corner_radius=8)
        canvas_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        canvas = FigureCanvasTkAgg(fig, master=canvas_container)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True, padx=10, pady=10)

    def limpiar_canvas_resultado(self):
        """Limpia el canvas de resultados LaTeX y el frame de LaTeX"""
        if self.canvas_resultado:
            self.canvas_resultado.get_tk_widget().destroy()
            self.canvas_resultado = None
        if hasattr(self, "latex_frame") and self.latex_frame is not None:
            self.latex_frame.destroy()
            self.latex_frame = None

    def mostrar_latex(self, expresion_latex, titulo="Resultado"):
        """Muestra una expresión en formato LaTeX"""
        self.limpiar_canvas_resultado()

        # Destruir el frame anterior si existe
        if hasattr(self, "latex_frame") and self.latex_frame is not None:
            self.latex_frame.destroy()
            self.latex_frame = None

        # Crear contenedor para la expresión LaTeX
        self.latex_frame = ctk.CTkFrame(self.resultado_contenedor, fg_color="#292d32", corner_radius=8)
        self.latex_frame.pack(fill="x", padx=10, pady=(10, 0))

        # Figura para mostrar LaTeX
        fig, ax = plt.subplots(figsize=(6, 1.6), dpi=100, facecolor="#292d32")
        ax.set_facecolor("#292d32")
        
        # Mostrar la expresión en formato LaTeX con estilo mejorado
        ax.text(0.5, 0.5, f"${expresion_latex}$", 
                fontsize=22, 
                ha="center", 
                va="center", 
                color="#00ffff", 
                weight="bold")
        ax.axis("off")

        # Añadir la figura al contenedor
        self.canvas_resultado = FigureCanvasTkAgg(fig, master=self.latex_frame)
        self.canvas_resultado.draw()
        self.canvas_resultado.get_tk_widget().pack(fill="both", expand=True, pady=10)