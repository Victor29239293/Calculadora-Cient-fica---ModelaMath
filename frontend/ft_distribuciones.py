import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from backend.bk_distribucion import GeneradorDistribuciones
import numpy as np
from matplotlib.figure import Figure
 
DARK_BG = "#101117"
PANEL_BG = "#1A1B26"
ACCENT = "#7B68EE"
ACCENT_LIGHT = "#9F92F5"   
TEXT_COLOR = "#E0E0E0"
INPUT_BG = "#141522"
BUTTON_HOVER = "#634BD6"
TABLE_BG = "#0D0F18"
TABLE_HEADER_BG = "#262842"
GRAPH_BG = "#141522"

class DistribucionesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=DARK_BG)
        ctk.set_appearance_mode("dark")

        # Scrollable principal
        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=DARK_BG,
            scrollbar_fg_color=PANEL_BG,
            scrollbar_button_color=ACCENT
        )
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)

        # — Panel de parámetros —
        self.create_params_panel()
        
        # — Panel de resultados —
        self.create_results_panel()
        
        # Inicializar visibilidad de parámetros
        self.cambiar_distribucion("Uniforme")

    def create_params_panel(self):
        """Crear el panel de parámetros con un diseño mejorado"""
        params = ctk.CTkFrame(self.scroll, fg_color=PANEL_BG, corner_radius=15)
        params.pack(fill="x", pady=(0,15))

        # Título con mejor visibilidad
        title_frame = ctk.CTkFrame(params, fg_color=ACCENT, corner_radius=10)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            title_frame,
            text="Generador de Distribuciones & Estimación de Área",
            font=("Helvetica", 16, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=5)

        # Panel para parámetros del LCG
        lcg_frame = ctk.CTkFrame(params, fg_color=PANEL_BG)
        lcg_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(
            lcg_frame,
            text="Parámetros del Generador Congruencial",
            font=("Helvetica", 14, "bold"),
            text_color=ACCENT_LIGHT
        ).pack(anchor="w", pady=(5,10))

        # LCG inputs con grid para mejor alineación
        lcg_grid = ctk.CTkFrame(lcg_frame, fg_color=PANEL_BG)
        lcg_grid.pack(fill="x", padx=10, pady=5)
        
        # Organiza inputs en 2 columnas
        labels_data = [
            ("Semilla (X₀)", "seed", "17"),
            ("Multiplicador (a)", "a", "1103515245"),
            ("Incremento (c)", "c", "12345"),
            ("Módulo (m)", "m", "2147483648"),
            ("Cantidad de puntos (n)", "n", "1000")
        ]
        
        # Crear grid de inputs
        for i, (label, attr, default) in enumerate(labels_data):
            row_num = i // 2
            col_num = i % 2
            
            # Frame para cada par label-input
            input_frame = ctk.CTkFrame(lcg_grid, fg_color=PANEL_BG)
            input_frame.grid(row=row_num, column=col_num, padx=10, pady=5, sticky="ew")
            lcg_grid.grid_columnconfigure(col_num, weight=1)
            
            # Label con mejor estilo
            ctk.CTkLabel(
                input_frame, 
                text=f"{label}:", 
                width=150, 
                text_color=TEXT_COLOR,
                font=("Helvetica", 12)
            ).pack(side="top", anchor="w", pady=(0,2))
            
            # Entry con mejor estilo
            entry = ctk.CTkEntry(
                input_frame, 
                placeholder_text="Valor...",
                fg_color=INPUT_BG,
                border_color=ACCENT,
                text_color=TEXT_COLOR,
                height=30
            )
            entry.insert(0, default)
            entry.pack(side="top", fill="x", pady=(0,2))
            setattr(self, f"{attr}_entry", entry)

        # Sección de distribuciones
        dist_section = ctk.CTkFrame(params, fg_color=PANEL_BG)
        dist_section.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            dist_section,
            text="Configuración de la Distribución",
            font=("Helvetica", 14, "bold"),
            text_color=ACCENT_LIGHT
        ).pack(anchor="w", pady=(5,10))
        
        # Selector de distribución
        dist_row = ctk.CTkFrame(dist_section, fg_color=PANEL_BG)
        dist_row.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            dist_row, 
            text="Tipo de Distribución:", 
            width=150, 
            text_color=TEXT_COLOR,
            font=("Helvetica", 12, "bold")
        ).pack(side="left")
        
        self.dist_var = ctk.StringVar(value="Uniforme")
        self.dist_menu = ctk.CTkOptionMenu(
            dist_row,
            values=["Uniforme", "Poisson", "Exponencial", "Normal", "Binomial"],  # <-- Elimina "Área Curvas"
            variable=self.dist_var,
            width=200,
            command=self.cambiar_distribucion,
            fg_color=INPUT_BG,
            button_color=ACCENT,
            button_hover_color=BUTTON_HOVER,
            dropdown_fg_color=INPUT_BG,
            dropdown_hover_color=BUTTON_HOVER,
            font=("Helvetica", 12)
        )
        self.dist_menu.pack(side="left", padx=10)

        # Parámetros específicos de distribuciones
        self.params_especificos = ctk.CTkFrame(dist_section, fg_color=PANEL_BG)
        self.params_especificos.pack(fill="x", padx=10, pady=10)
        
        # Para Poisson
        self.poisson_frame = ctk.CTkFrame(self.params_especificos, fg_color=PANEL_BG)
        ctk.CTkLabel(
            self.poisson_frame, 
            text="Lambda (λ):", 
            width=150, 
            text_color=TEXT_COLOR,
            font=("Helvetica", 12)
        ).pack(side="left")
        
        self.lambda_entry = ctk.CTkEntry(
            self.poisson_frame, 
            placeholder_text="Lambda",
            fg_color=INPUT_BG,
            border_color=ACCENT,
            text_color=TEXT_COLOR,
            width=120
        )
        self.lambda_entry.insert(0, "4")
        self.lambda_entry.pack(side="left", padx=10)
        
        # Para Exponencial
        self.exp_frame = ctk.CTkFrame(self.params_especificos, fg_color=PANEL_BG)
        ctk.CTkLabel(
            self.exp_frame, 
            text="Lambda (λ):", 
            width=150, 
            text_color=TEXT_COLOR,
            font=("Helvetica", 12)
        ).pack(side="left")
        
        self.exp_lambda_entry = ctk.CTkEntry(
            self.exp_frame, 
            placeholder_text="Lambda",
            fg_color=INPUT_BG,
            border_color=ACCENT,
            text_color=TEXT_COLOR,
            width=120
        )
        self.exp_lambda_entry.insert(0, "1.0")
        self.exp_lambda_entry.pack(side="left", padx=10)
        
        # Para Binomial
        self.bin_frame = ctk.CTkFrame(self.params_especificos, fg_color=PANEL_BG)
        ctk.CTkLabel(
            self.bin_frame, 
            text="n:", 
            width=75, 
            text_color=TEXT_COLOR,
            font=("Helvetica", 12)
        ).pack(side="left")
        
        self.bin_n_entry = ctk.CTkEntry(
            self.bin_frame, 
            placeholder_text="n",
            fg_color=INPUT_BG,
            border_color=ACCENT,
            text_color=TEXT_COLOR,
            width=80
        )
        self.bin_n_entry.insert(0, "10")
        self.bin_n_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(
            self.bin_frame, 
            text="p:", 
            width=75, 
            text_color=TEXT_COLOR,
            font=("Helvetica", 12)
        ).pack(side="left")
        
        self.bin_p_entry = ctk.CTkEntry(
            self.bin_frame, 
            placeholder_text="p",
            fg_color=INPUT_BG,
            border_color=ACCENT,
            text_color=TEXT_COLOR,
            width=80
        )
        self.bin_p_entry.insert(0, "0.5")
        self.bin_p_entry.pack(side="left", padx=5)

        # Botones con mejor diseño y posicionamiento
        self.botones_frame = ctk.CTkFrame(params, fg_color=PANEL_BG)
        self.botones_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # Botón para generar distribución
        self.btn_generar = ctk.CTkButton(
            self.botones_frame,
            text="Generar Distribución",
            command=self.generar_distribucion,
            fg_color=ACCENT,
            hover_color=BUTTON_HOVER,
            font=("Helvetica", 14, "bold"),
            height=38,
            corner_radius=8
        )
        self.btn_generar.pack(side="left", padx=10, fill="x", expand=True)

        # Botón para ejecutar estimación de área
        self.btn_area = ctk.CTkButton(
            self.botones_frame,
            text="Estimar Área Monte Carlo",
            command=self.estimar_area_montecarlo,
            fg_color=ACCENT,
            hover_color=BUTTON_HOVER,
            font=("Helvetica", 14, "bold"),
            height=38,
            corner_radius=8
        )
        # No se empaqueta hasta seleccionar "Área Curvas"

    def create_results_panel(self):
        """Crear el panel de resultados con mejor diseño"""
        self.resultado_frame = ctk.CTkFrame(self.scroll, fg_color=PANEL_BG, corner_radius=15)
        self.resultado_frame.pack(fill="both", expand=True, pady=10)

        # Título de resultados
        self.result_title = ctk.CTkLabel(
            self.resultado_frame,
            text="Resultados",
            font=("Helvetica", 16, "bold"),
            text_color=ACCENT_LIGHT,
        )
        self.result_title.pack(anchor="w", padx=15, pady=(15, 10))

        # Marco para organizar resultados y gráficos horizontalmente
        self.content_frame = ctk.CTkFrame(self.resultado_frame, fg_color=PANEL_BG)
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Cuadro de texto para resultados numéricos con mejor estilo
        self.texto_resultado = ctk.CTkTextbox(
            self.content_frame,
            corner_radius=8,
            font=("Consolas", 12),
            fg_color=TABLE_BG,
            text_color=TEXT_COLOR,
            border_width=1,
            border_color="#303446",
        )
        self.texto_resultado.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=5)

        # Marco para gráficas
        self.graphs_container = ctk.CTkFrame(self.content_frame, fg_color=PANEL_BG)
        self.graphs_container.pack(side="right", fill="both", expand=True, pady=5)
        
        # Principal canvas para gráfica de distribución
        self.canvas_frame = ctk.CTkFrame(self.graphs_container, fg_color=GRAPH_BG, corner_radius=8)
        self.canvas_frame.pack(fill="both", expand=True, pady=(0, 5))
        self.canvas = None
        
        # Canvas adicional para monte carlo (oculto inicialmente)
        self.montecarlo_frame = ctk.CTkFrame(self.graphs_container, fg_color=GRAPH_BG, corner_radius=8)
        self.montecarlo_canvas = None

    def cambiar_distribucion(self, distribucion):
        """Actualiza la UI según la distribución seleccionada"""
        # Ocultar todos los frames de parámetros
        self.poisson_frame.pack_forget()
        self.exp_frame.pack_forget()
        self.bin_frame.pack_forget()
        self.btn_generar.pack_forget()
        self.btn_area.pack_forget()
        
        # Mostrar solo los elementos relevantes
        if distribucion == "Poisson":
            self.poisson_frame.pack(fill="x")
            self.btn_generar.pack(side="left", padx=10, fill="x", expand=True)
            self.result_title.configure(text="Resultados: Distribución Poisson")
        elif distribucion == "Exponencial":
            self.exp_frame.pack(fill="x")
            self.btn_generar.pack(side="left", padx=10, fill="x", expand=True)
            self.result_title.configure(text="Resultados: Distribución Exponencial")
        elif distribucion == "Binomial":
            self.bin_frame.pack(fill="x")
            self.btn_generar.pack(side="left", padx=10, fill="x", expand=True)
            self.result_title.configure(text="Resultados: Distribución Binomial")
        elif distribucion == "Normal":
            self.btn_generar.pack(side="left", padx=10, fill="x", expand=True)
            self.result_title.configure(text="Resultados: Distribución Normal")
        else:  # Uniforme
            self.btn_generar.pack(side="left", padx=10, fill="x", expand=True)
            self.result_title.configure(text="Resultados: Distribución Uniforme")
        
        # Limpiar contenido
        self.texto_resultado.delete("0.0", "end")
        
        # Limpiar gráficas
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        if self.montecarlo_canvas:
            self.montecarlo_canvas.get_tk_widget().destroy()
            self.montecarlo_canvas = None

        # <-- AGREGA ESTA LÍNEA para mostrar SIEMPRE el marco de Monte Carlo
        self.montecarlo_frame.pack(fill="both", expand=True, pady=(5, 0))

    def leer_parametros(self):
        """Lee los parámetros LCG y valida que sean correctos"""
        try:
            seed = int(self.seed_entry.get())
            a = int(self.a_entry.get())
            c = int(self.c_entry.get())
            m = int(self.m_entry.get())
            n = int(self.n_entry.get())
            
            # Validación básica
            if m <= 0:
                raise ValueError("El módulo (m) debe ser positivo")
            if n <= 0:
                raise ValueError("La cantidad de números debe ser positiva")
            
            return GeneradorDistribuciones(seed, a, c, m, n)
        except ValueError as e:
            CTkMessagebox(
                title="Error en parámetros",
                message=f"Todos los valores deben ser enteros válidos: {e}",
                icon="cancel",
                option_1="OK"
            )
            return None

    def formatear_tabla(self, tabla, distribucion):
        """Formatea los datos de la tabla de manera estética"""
        # Cabecera con mejor estilo
        self.texto_resultado.delete("0.0", "end")
        self.texto_resultado.insert("end", f"Distribución: {distribucion}\n\n")
        
        # Formato de cabecera
        self.texto_resultado.insert("end", f"{'n°':<5}{'Xn':<15}{'Un':<15}{'f(Un)':<15}\n")
        self.texto_resultado.insert("end", "="*50 + "\n")
        
        # Datos con formato mejorado
        for fila in tabla:
            if isinstance(fila['f(Un)'], float):
                valor_f = f"{fila['f(Un)']:.8f}"
            elif isinstance(fila['f(Un)'], int):
                valor_f = str(fila['f(Un)'])
            else:
                valor_f = str(fila['f(Un)'])
                
            self.texto_resultado.insert(
                "end",
                f"{fila['n']:<5}{fila['Xn']:<15}{fila['Un']:<15.8f}{valor_f:<15}\n"
            )

    def crear_grafico_distribucion(self, transformados, distribucion, parametros=None):
        """Crea un gráfico adecuado para cada tipo de distribución"""
        # Limpiar gráfico anterior
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        # Preparar figura con estilo mejorado
        fig = Figure(figsize=(6, 5), facecolor=GRAPH_BG)
        ax = fig.add_subplot(111)
        
        # Configurar título según la distribución
        if distribucion == "Uniforme":
            titulo = "Distribución Uniforme"
            x_label = "Valor"
            y_label = "Frecuencia"
            # Histograma para uniformes
            ax.hist(transformados, bins=20, color=ACCENT, alpha=0.7, edgecolor='black')
            
        elif distribucion == "Poisson":
            lam = parametros['lam']
            titulo = f"Distribución Poisson (λ={lam})"
            x_label = "Valor"
            y_label = "Frecuencia"
            # Gráfico para valores discretos
            unique_vals = sorted(list(set(transformados)))
            counts = [transformados.count(val) for val in unique_vals]
            ax.bar(unique_vals, counts, color=ACCENT, alpha=0.7, edgecolor='black', width=0.4)
            
            # Añadir línea de valor esperado
            ax.axvline(x=lam, color='red', linestyle='--', 
                      label=f"Valor esperado (λ={lam})")
            ax.legend()
            
        elif distribucion == "Exponencial":
            lambd = parametros['lambd']
            titulo = f"Distribución Exponencial (λ={lambd})"
            x_label = "Valor"
            y_label = "Frecuencia"
            # Histograma para exponenciales
            ax.hist(transformados, bins=20, color=ACCENT, alpha=0.7, edgecolor='black')
            
            # Añadir línea de valor esperado
            media = 1/lambd
            ax.axvline(x=media, color='red', linestyle='--', 
                      label=f"Valor esperado (1/λ={media:.4f})")
            ax.legend()
            
        elif distribucion == "Normal":
            titulo = "Distribución Normal (μ=0, σ=1)"
            x_label = "Valor"
            y_label = "Frecuencia"
            # Histograma para normales
            ax.hist(transformados, bins=20, color=ACCENT, alpha=0.7, edgecolor='black')
            
            # Añadir línea de la media
            ax.axvline(x=0, color='red', linestyle='--', 
                      label="Valor esperado (μ=0)")
            ax.legend()
            
        elif distribucion == "Binomial":
            n_bin = parametros['n']
            p_bin = parametros['p']
            titulo = f"Distribución Binomial (n={n_bin}, p={p_bin})"
            x_label = "Valor"
            y_label = "Frecuencia"
            # Gráfico para valores discretos
            unique_vals = sorted(list(set(transformados)))
            counts = [transformados.count(val) for val in unique_vals]
            ax.bar(unique_vals, counts, color=ACCENT, alpha=0.7, edgecolor='black', width=0.4)
            
            # Añadir línea del valor esperado
            media = n_bin * p_bin
            ax.axvline(x=media, color='red', linestyle='--', 
                      label=f"Valor esperado (np={media})")
            ax.legend()
        
        # Estilo común
        ax.set_title(titulo, color=TEXT_COLOR, fontsize=14, pad=10)
        ax.set_xlabel(x_label, color=TEXT_COLOR)
        ax.set_ylabel(y_label, color=TEXT_COLOR)
        ax.tick_params(colors=TEXT_COLOR)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.set_facecolor(GRAPH_BG)
        
        # Ajustar los bordes
        fig.tight_layout(pad=3.0)
        
        # Mostrar gráfico
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Mostrar el gráfico de Monte Carlo en el canvas secundario
        self.mostrar_grafico_montecarlo()

    def generar_distribucion(self):
        """Genera la distribución seleccionada con los parámetros especificados"""
        try:
            generador = self.leer_parametros()
            if not generador:
                return
                
            # Generar números congruenciales
            valores, uniformes = generador.generar_congruencial()
            
            # Aplicar transformación según la distribución seleccionada
            distribucion = self.dist_var.get()
            parametros = {}
            
            if distribucion == "Uniforme":
                transformados = uniformes
                
            elif distribucion == "Poisson":
                lam = float(self.lambda_entry.get())
                parametros['lam'] = lam
                transformados = generador.aplicar_poisson(uniformes, lam=lam)
                
            elif distribucion == "Exponencial":
                lambd = float(self.exp_lambda_entry.get())
                parametros['lambd'] = lambd
                transformados = generador.aplicar_exponencial(uniformes, lambd=lambd)
                
            elif distribucion == "Normal":
                transformados = generador.aplicar_normal(uniformes)
                
            elif distribucion == "Binomial":
                n_bin = int(self.bin_n_entry.get())
                p_bin = float(self.bin_p_entry.get())
                parametros['n'] = n_bin
                parametros['p'] = p_bin
                transformados = generador.aplicar_binomial(uniformes, n=n_bin, p=p_bin)
            
            # Construir tabla de resultados
            tabla = generador.construir_tabla(valores, uniformes, transformados)
            
            # Mostrar tabla formateda
            self.formatear_tabla(tabla, distribucion)
            
            # Crear gráfico adecuado
            self.crear_grafico_distribucion(transformados, distribucion, parametros)
        except Exception as e:
            CTkMessagebox(
                title="Error en Generación",
                message=f"Ocurrió un error: {e}",
                icon="cancel",
                option_1="OK"
            )

    def estimar_area_montecarlo(self):
        """Realiza estimación de área entre curvas usando Monte Carlo"""
        try:
            generador = self.leer_parametros()
            if not generador:
                return
            
            # Generar puntos uniformes usando el generador congruencial
            _, uniformes_x = generador.generar_congruencial()
            # Reiniciar semilla y generar otra secuencia para Y
            generador.semilla = (generador.semilla + 1) % generador.m
            _, uniformes_y = generador.generar_congruencial()
            
            # Asegurar misma longitud
            n = min(len(uniformes_x), len(uniformes_y))
            x_vals = uniformes_x[:n]
            y_vals = uniformes_y[:n]
            
            # Curvas
            y_x2 = np.array([x**2 for x in x_vals])
            y_sqrt = np.array([np.sqrt(x) for x in x_vals])
            
            # Determinar puntos interiores
            interiores_ambas = []
            for i in range(n):
                dentro = y_vals[i] >= y_x2[i] and y_vals[i] <= y_sqrt[i]
                interiores_ambas.append(dentro)
            
            area_ambas = sum(interiores_ambas) / n
            # Valor teórico: ∫[0,1] (√x - x²) dx = 1/3
            valor_teorico = 1/3
            error_porcentual = abs((area_ambas - valor_teorico) / valor_teorico) * 100
            
            # Texto de resultados con formato mejorado
            self.texto_resultado.delete("0.0", "end")
            self.texto_resultado.insert("end", "ESTIMACIÓN DE ÁREA POR MONTE CARLO\n")
            self.texto_resultado.insert("end", "="*50 + "\n\n")
            self.texto_resultado.insert("end", "Área entre las curvas f(x)=x² y f(x)=√x\n\n")
            self.texto_resultado.insert("end", f"• Total de puntos generados: {n}\n")
            self.texto_resultado.insert("end", f"• Puntos entre las curvas: {sum(interiores_ambas)}\n")
            self.texto_resultado.insert("end", f"• Área estimada: {area_ambas:.8f}\n")
            self.texto_resultado.insert("end", f"• Área teórica: {valor_teorico:.8f}\n")
            self.texto_resultado.insert("end", f"• Error porcentual: {error_porcentual:.4f}%\n\n")
            
            self.texto_resultado.insert("end", f"{'n°':<5}{'x':<12}{'y':<12}{'x²':<12}{'√x':<12}{'Dentro':<8}\n")
            self.texto_resultado.insert("end", "-"*50 + "\n")
            
            for i in range(min(20, n)):  # Mostrar solo los primeros 20 puntos
                self.texto_resultado.insert(
                    "end",
                    f"{i+1:<5}{x_vals[i]:<12.6f}{y_vals[i]:<12.6f}{y_x2[i]:<12.6f}{y_sqrt[i]:<12.6f}{'Sí' if interiores_ambas[i] else 'No':<8}\n"
                )
            
            if n > 20:
                self.texto_resultado.insert("end", "...\n")
            
            # Limpiar gráficos anteriores
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            if self.montecarlo_canvas:
                self.montecarlo_canvas.get_tk_widget().destroy()
            
            # Crear el gráfico de puntos (primer gráfico)
            fig1 = Figure(figsize=(6,4), facecolor=GRAPH_BG)
            ax1 = fig1.add_subplot(111)
            
            # Crear curvas con puntos ordenados para mejor visualización
            x_ordenado = np.linspace(0, 1, 100)
            y_x2_ordenado = x_ordenado ** 2
            y_sqrt_ordenado = np.sqrt(x_ordenado)
            
            # Sombrear el área entre las curvas
            ax1.fill_between(x_ordenado, y_x2_ordenado, y_sqrt_ordenado, 
                           color=ACCENT, alpha=0.15, label="Área teórica")
            
            # Dibujar las curvas
            ax1.plot(x_ordenado, y_x2_ordenado, label="f(x)=x²", linewidth=2, color="#FF5E5B")
            ax1.plot(x_ordenado, y_sqrt_ordenado, linestyle='--', linewidth=2, label="f(x)=√x", color="#22BABB")
            
            # Convertir listas booleanas a arrays para indexación
            interiores_ambas = np.array(interiores_ambas)
            x_vals = np.array(x_vals)
            y_vals = np.array(y_vals)
            
            # Graficar puntos dentro y fuera
            ax1.scatter(x_vals[interiores_ambas], y_vals[interiores_ambas], s=20, color="#4DE897", label="Dentro")
            ax1.scatter(x_vals[~interiores_ambas], y_vals[~interiores_ambas], s=15, color="#FF5E5B", alpha=0.5, label="Fuera")
            
            # Configuración general del gráfico
            ax1.set_xlim(0,1)
            ax1.set_ylim(0,1)
            ax1.set_xticks(np.arange(0,1.1,0.2))
            ax1.set_yticks(np.arange(0,1.1,0.2))
            ax1.set_title("Estimación Monte Carlo - Puntos", color=TEXT_COLOR, fontsize=14, pad=10)
            ax1.set_xlabel("x", color=TEXT_COLOR)
            ax1.set_ylabel("y", color=TEXT_COLOR)
            ax1.tick_params(colors=TEXT_COLOR)
            ax1.legend(frameon=True, loc="upper right")
            ax1.grid(True, linestyle=":", alpha=0.4)
            ax1.set_facecolor(GRAPH_BG)
            
            # Ajustar los bordes
            fig1.tight_layout(pad=3.0)
            
            # Mostrar en canvas principal
            self.canvas = FigureCanvasTkAgg(fig1, master=self.canvas_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Segundo gráfico: Convergencia de la estimación
            fig2 = Figure(figsize=(6,3), facecolor=GRAPH_BG)
            ax2 = fig2.add_subplot(111)
            
            # Calcular la convergencia del área estimada
            estimaciones = []
            for i in range(1, n+1):
                if i % max(1, n//100) == 0:  # Tomar menos puntos para eficiencia
                    estimaciones.append(sum(interiores_ambas[:i]) / i)
            
            puntos_x = np.linspace(1, n, len(estimaciones))
            
            # Graficar la convergencia
            ax2.plot(puntos_x, estimaciones, color=ACCENT, linewidth=1.5)
            ax2.axhline(y=valor_teorico, color="#4DE897", linestyle='-', label="Valor teórico (1/3)")
            
            # Configuración del gráfico de convergencia
            ax2.set_title("Convergencia de la Estimación", color=TEXT_COLOR, fontsize=14)
            ax2.set_xlabel("Número de puntos", color=TEXT_COLOR)
            ax2.set_ylabel("Área estimada", color=TEXT_COLOR)
            ax2.tick_params(colors=TEXT_COLOR)
            ax2.legend(frameon=True)
            ax2.grid(True, linestyle=":", alpha=0.4)
            ax2.set_facecolor(GRAPH_BG)
            
            # Ajustar los bordes
            fig2.tight_layout(pad=3.0)
            
            # Mostrar en canvas secundario
            self.montecarlo_canvas = FigureCanvasTkAgg(fig2, master=self.montecarlo_frame)
            self.montecarlo_canvas.draw()
            self.montecarlo_canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as e:
            CTkMessagebox(
                title="Error en Generación",
                message=f"Ocurrió un error: {e}",
                icon="cancel",
                option_1="OK"
            )

    def mostrar_grafico_montecarlo(self, n_puntos=2000, n_repeticiones=300):
        # Limpiar canvas anterior si existe
        if self.montecarlo_canvas:
            self.montecarlo_canvas.get_tk_widget().destroy()
            self.montecarlo_canvas = None

        try:
            n = int(self.n_entry.get())  # <--- CORREGIDO AQUÍ
            x_vals = np.random.rand(n)
            y_vals = np.random.rand(n)
            y_x2 = x_vals ** 2
            y_sqrt = np.sqrt(x_vals)

            interiores_ambas = np.logical_and(y_vals >= y_x2, y_vals <= y_sqrt)
            area_ambas = np.sum(interiores_ambas) / n

            self.texto_resultado.delete("0.0", "end")
            self.texto_resultado.insert("end", f"Resumen estimaci\u00f3n Monte Carlo:\n")
            self.texto_resultado.insert("end", f"- Total de puntos: {n}\n")
            self.texto_resultado.insert("end", f"- Puntos entre x\u00b2 y \u221ax: {np.sum(interiores_ambas)}\n")
            self.texto_resultado.insert("end", f"- \u00c1rea estimada (entre): {area_ambas:.5f}\n\n")

            self.texto_resultado.insert("end", f"{'n°':<5}{'x':<10}{'y':<10}{'Dentro (x² < y < √x)':<25}\n")
            self.texto_resultado.insert("end", "="*50 + "\n")
            for i in range(n):
                self.texto_resultado.insert("end", f"{i+1:<5}{x_vals[i]:<10.4f}{y_vals[i]:<10.4f}{int(interiores_ambas[i]):<25}\n")

            if hasattr(self, "canvas_montecarlo") and self.canvas_montecarlo is not None:
                self.canvas_montecarlo.get_tk_widget().destroy()

            fig, ax = plt.subplots(figsize=(6, 5))
            ax.plot(np.sort(x_vals), np.sort(y_x2), label="f(x)=x²", linewidth=2)
            ax.plot(np.sort(x_vals), np.sort(y_sqrt), label="f(x)=√x", linestyle="--", linewidth=2)
            ax.scatter(x_vals[interiores_ambas], y_vals[interiores_ambas], s=15, label="Dentro ambas")
            ax.scatter(x_vals[~interiores_ambas], y_vals[~interiores_ambas], s=15, label="Fuera")
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.legend(frameon=True, loc="upper right")
            ax.grid(True, linestyle=":", alpha=0.6)
            ax.set_title("Monte Carlo - Área entre x² y √x", fontsize=12)

            self.canvas_montecarlo = FigureCanvasTkAgg(fig, master=self.montecarlo_frame)
            self.canvas_montecarlo.draw()
            self.canvas_montecarlo.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            CTkMessagebox(
                title="Error en Generación",
                message=f"Ocurrió un error: {e}",
                icon="cancel",
                option_1="OK"
            )