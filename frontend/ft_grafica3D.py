import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import StringVar, DoubleVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from backend.bk_grafica3D import generar_malla, evaluar_funcion_3d

class Graficas3DPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=["#f8f9fa", "#0d1117"])  # Tema claro/oscuro
        
        # Configurar el estilo de matplotlib para modo oscuro
        plt.style.use('dark_background')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header principal con degradado visual
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
        
        # Sección de configuración avanzada
        self.create_advanced_settings_section()
        
        # Botón de graficado mejorado
        self.create_graph_button()
        
        # Área de visualización
        self.create_visualization_area()
        
    def create_header(self):
        """Crear header principal con diseño mejorado"""
        header_frame = ctk.CTkFrame(
            self,
            height=80,
            fg_color=["#6366f1", "#4338ca"],
            corner_radius=0
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Título principal
        title_label = ctk.CTkLabel(
            header_frame,
            text="🌐 Visualizador de Funciones 3D",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        )
        title_label.pack(expand=True)
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Crea visualizaciones interactivas de funciones matemáticas",
            font=("Segoe UI", 12),
            text_color=["#e0e7ff", "#c7d2fe"]
        )
        subtitle_label.pack(pady=(0, 10))
        
    def create_function_input_section(self):
        """Sección de entrada de función mejorada"""
        # Frame principal de entrada
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
            text="📝 Definición de Función",
            font=("Segoe UI", 18, "bold"),
            text_color=["#1f2937", "#f9fafb"]
        )
        section_title.pack(pady=(20, 10))
        
        # Frame para entrada de función
        func_frame = ctk.CTkFrame(input_section, fg_color="transparent")
        func_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            func_frame,
            text="Función f(x,y):",
            font=("Segoe UI", 14, "bold"),
            text_color=["#374151", "#d1d5db"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.entrada_funcion = ctk.CTkEntry(
            func_frame,
            placeholder_text="Ejemplo: sin(x)*cos(y), x**2 + y**2, exp(-x**2-y**2)",
            width=500,
            height=40,
            font=("Consolas", 12),
            corner_radius=8,
            border_width=2,
            border_color=["#d1d5db", "#4b5563"]
        )
        self.entrada_funcion.pack(fill="x", pady=(0, 10))
        
        # Ejemplos rápidos
        examples_frame = ctk.CTkFrame(func_frame, fg_color="transparent")
        examples_frame.pack(fill="x")
        
        ctk.CTkLabel(
            examples_frame,
            text="Ejemplos rápidos:",
            font=("Segoe UI", 11),
            text_color=["#6b7280", "#9ca3af"]
        ).pack(anchor="w")
        
        examples_container = ctk.CTkFrame(examples_frame, fg_color="transparent")
        examples_container.pack(fill="x", pady=(5, 0))
        
        examples = [
            ("🌊 Ondas", "sin(x)*cos(y)"),
            ("🏔️ Montaña", "exp(-x**2-y**2)"),
            ("🌀 Paraboloide", "x**2 + y**2")
        ]
        
        for i, (name, func) in enumerate(examples):
            btn = ctk.CTkButton(
                examples_container,
                text=name,
                width=120,
                height=28,
                font=("Segoe UI", 10),
                fg_color=["#f3f4f6", "#374151"],
                text_color=["#374151", "#d1d5db"],
                hover_color=["#e5e7eb", "#4b5563"],
                command=lambda f=func: self.entrada_funcion.delete(0, "end") or self.entrada_funcion.insert(0, f)
            )
            btn.pack(side="left", padx=(0, 8))
        
        # Rangos de variables
        self.create_range_inputs(input_section)
        
    def create_range_inputs(self, parent):
        """Crear inputs para rangos de X e Y"""
        ranges_frame = ctk.CTkFrame(parent, fg_color="transparent")
        ranges_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            ranges_frame,
            text="📏 Rangos de Variables",
            font=("Segoe UI", 14, "bold"),
            text_color=["#374151", "#d1d5db"]
        ).pack(anchor="w", pady=(0, 10))
        
        # Grid para rangos
        ranges_grid = ctk.CTkFrame(ranges_frame, fg_color="transparent")
        ranges_grid.pack(fill="x")
        
        # Configurar grid
        ranges_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Labels
        ctk.CTkLabel(ranges_grid, text="X mínimo", font=("Segoe UI", 11)).grid(
            row=0, column=0, padx=5, pady=(0, 5), sticky="w"
        )
        ctk.CTkLabel(ranges_grid, text="X máximo", font=("Segoe UI", 11)).grid(
            row=0, column=1, padx=5, pady=(0, 5), sticky="w"
        )
        ctk.CTkLabel(ranges_grid, text="Y mínimo", font=("Segoe UI", 11)).grid(
            row=0, column=2, padx=5, pady=(0, 5), sticky="w"
        )
        ctk.CTkLabel(ranges_grid, text="Y máximo", font=("Segoe UI", 11)).grid(
            row=0, column=3, padx=5, pady=(0, 5), sticky="w"
        )
        
        # Entradas
        self.x_min = ctk.CTkEntry(
            ranges_grid, placeholder_text="-5", width=100, height=35,
            corner_radius=6
        )
        self.x_min.grid(row=1, column=0, padx=5, sticky="ew")
        
        self.x_max = ctk.CTkEntry(
            ranges_grid, placeholder_text="5", width=100, height=35,
            corner_radius=6
        )
        self.x_max.grid(row=1, column=1, padx=5, sticky="ew")
        
        self.y_min = ctk.CTkEntry(
            ranges_grid, placeholder_text="-5", width=100, height=35,
            corner_radius=6
        )
        self.y_min.grid(row=1, column=2, padx=5, sticky="ew")
        
        self.y_max = ctk.CTkEntry(
            ranges_grid, placeholder_text="5", width=100, height=35,
            corner_radius=6
        )
        self.y_max.grid(row=1, column=3, padx=5, sticky="ew")
        
    def create_advanced_settings_section(self):
        """Crear sección de configuración avanzada"""
        settings_section = ctk.CTkFrame(
            self.main_container,
            fg_color=["#ffffff", "#1f2937"],
            corner_radius=12,
            border_width=1,
            border_color=["#e5e7eb", "#374151"]
        )
        settings_section.pack(fill="x", pady=(0, 20))
        
        # Título expansible
        header_frame = ctk.CTkFrame(settings_section, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)
        
        self.settings_expanded = ctk.BooleanVar(value=False)
        
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
        
        # Panel de configuración (inicialmente oculto)
        self.settings_panel = ctk.CTkFrame(settings_section, fg_color="transparent")
        
        self.create_settings_content()
        
    def create_settings_content(self):
        """Crear contenido de configuración avanzada"""
        # Grid principal para configuraciones
        config_grid = ctk.CTkFrame(self.settings_panel, fg_color="transparent")
        config_grid.pack(fill="x", padx=20, pady=(0, 20))
        
        config_grid.grid_columnconfigure((0, 1), weight=1)
        
        # Columna izquierda - Visual
        visual_frame = ctk.CTkFrame(
            config_grid,
            fg_color=["#f8fafc", "#111827"],
            corner_radius=8
        )
        visual_frame.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="new")
        
        ctk.CTkLabel(
            visual_frame,
            text="🎨 Apariencia Visual",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(15, 10))
        
        # Colormap
        cmap_frame = ctk.CTkFrame(visual_frame, fg_color="transparent")
        cmap_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(cmap_frame, text="Esquema de colores:", anchor="w").pack(fill="x")
        self.cmap_var = StringVar(value="plasma")
        ctk.CTkOptionMenu(
            cmap_frame,
            values=["plasma", "viridis", "coolwarm", "magma", "cividis", "rainbow"],
            variable=self.cmap_var,
            width=180,
            height=30
        ).pack(fill="x", pady=(3, 10))
        
        # Resolución
        res_frame = ctk.CTkFrame(visual_frame, fg_color="transparent")
        res_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(res_frame, text="Resolución de malla:", anchor="w").pack(fill="x")
        
        res_value_frame = ctk.CTkFrame(res_frame, fg_color="transparent")
        res_value_frame.pack(fill="x", pady=(3, 0))
        
        self.resol_var = DoubleVar(value=100)
        self.res_label = ctk.CTkLabel(res_value_frame, text="100 puntos")
        self.res_label.pack(side="right")
        
        res_slider = ctk.CTkSlider(
            res_value_frame,
            from_=50,
            to=300,
            number_of_steps=25,
            variable=self.resol_var,
            width=120,
            command=self.update_resolution_label
        )
        res_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Columna derecha - Cámara
        camera_frame = ctk.CTkFrame(
            config_grid,
            fg_color=["#f8fafc", "#111827"],
            corner_radius=8
        )
        camera_frame.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="new")
        
        ctk.CTkLabel(
            camera_frame,
            text="📷 Vista de Cámara",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(15, 10))
        
        # Elevación
        elev_frame = ctk.CTkFrame(camera_frame, fg_color="transparent")
        elev_frame.pack(fill="x", padx=15, pady=5)
        
        elev_label_frame = ctk.CTkFrame(elev_frame, fg_color="transparent")
        elev_label_frame.pack(fill="x")
        
        ctk.CTkLabel(elev_label_frame, text="Elevación:", anchor="w").pack(side="left")
        self.elev_var = DoubleVar(value=35)
        self.elev_label = ctk.CTkLabel(elev_label_frame, text="35°")
        self.elev_label.pack(side="right")
        
        ctk.CTkSlider(
            elev_frame,
            from_=-90,
            to=90,
            variable=self.elev_var,
            width=160,
            command=self.update_elevation_label
        ).pack(fill="x", pady=(3, 0))
        
        # Azimut
        azim_frame = ctk.CTkFrame(camera_frame, fg_color="transparent")
        azim_frame.pack(fill="x", padx=15, pady=(10, 15))
        
        azim_label_frame = ctk.CTkFrame(azim_frame, fg_color="transparent")
        azim_label_frame.pack(fill="x")
        
        ctk.CTkLabel(azim_label_frame, text="Azimut:", anchor="w").pack(side="left")
        self.azim_var = DoubleVar(value=135)
        self.azim_label = ctk.CTkLabel(azim_label_frame, text="135°")
        self.azim_label.pack(side="right")
        
        ctk.CTkSlider(
            azim_frame,
            from_=-180,
            to=180,
            variable=self.azim_var,
            width=160,
            command=self.update_azimuth_label
        ).pack(fill="x", pady=(3, 0))
        
        # Botones de vista predefinida
        preset_frame = ctk.CTkFrame(camera_frame, fg_color="transparent")
        preset_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        ctk.CTkLabel(preset_frame, text="Vistas predefinidas:", anchor="w").pack(fill="x")
        
        preset_buttons = ctk.CTkFrame(preset_frame, fg_color="transparent")
        preset_buttons.pack(fill="x", pady=(5, 0))
        
        presets = [
            ("Frontal", 0, 0),
            ("Lateral", 0, 90),
            ("Superior", 90, 0),
            ("Isométrica", 35, 45)
        ]
        
        for i, (name, elev, azim) in enumerate(presets):
            btn = ctk.CTkButton(
                preset_buttons,
                text=name,
                width=70,
                height=25,
                font=("Segoe UI", 9),
                fg_color=["#e5e7eb", "#4b5563"],
                text_color=["#374151", "#d1d5db"],
                hover_color=["#d1d5db", "#6b7280"],
                command=lambda e=elev, a=azim: self.set_camera_preset(e, a)
            )
            btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky="ew")
            
        preset_buttons.grid_columnconfigure((0, 1), weight=1)
        
    def create_graph_button(self):
        """Crear botón de graficado mejorado"""
        button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        button_frame.pack(pady=20)
        
        self.graph_button = ctk.CTkButton(
            button_frame,
            text="🚀 Generar Visualización 3D",
            command=self.graficar_3d,
            height=50,
            width=280,
            font=("Segoe UI", 16, "bold"),
            fg_color=["#4f46e5", "#6366f1"],
            hover_color=["#4338ca", "#4f46e5"],
            corner_radius=25,
            border_width=0
        )
        self.graph_button.pack()
        
        # Indicador de estado
        self.status_label = ctk.CTkLabel(
            button_frame,
            text="Listo para graficar",
            font=("Segoe UI", 11),
            text_color=["#6b7280", "#9ca3af"]
        )
        self.status_label.pack(pady=(8, 0))
        
    def create_visualization_area(self):
        """Crear área de visualización mejorada"""
        viz_section = ctk.CTkFrame(
            self.main_container,
            fg_color=["#ffffff", "#1f2937"],
            corner_radius=12,
            border_width=1,
            border_color=["#e5e7eb", "#374151"]
        )
        viz_section.pack(fill="both", expand=True, pady=(0, 20))
        
        # Header de visualización
        viz_header = ctk.CTkFrame(viz_section, fg_color="transparent", height=50)
        viz_header.pack(fill="x", padx=20, pady=(15, 10))
        viz_header.pack_propagate(False)
        
        ctk.CTkLabel(
            viz_header,
            text="📊 Visualización",
            font=("Segoe UI", 18, "bold"),
            text_color=["#1f2937", "#f9fafb"]
        ).pack(side="left", expand=True)
        
        # Área del canvas
        self.canvas_frame = ctk.CTkFrame(
            viz_section,
            fg_color=["#f8fafc", "#111827"],
            corner_radius=8
        )
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Mensaje inicial
        self.placeholder_label = ctk.CTkLabel(
            self.canvas_frame,
            text="🎯 Ingresa una función y presiona 'Generar Visualización 3D'\npara ver tu gráfica aquí",
            font=("Segoe UI", 14),
            text_color=["#6b7280", "#9ca3af"]
        )
        self.placeholder_label.grid(row=0, column=0)
        
    def toggle_advanced_settings(self):
        """Alternar visibilidad de configuración avanzada"""
        if self.settings_expanded.get():
            self.settings_panel.pack_forget()
            self.settings_expanded.set(False)
            # Actualizar texto del botón
            for widget in self.settings_panel.master.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    for subwidget in widget.winfo_children():
                        if isinstance(subwidget, ctk.CTkButton) and "Configuración" in subwidget.cget("text"):
                            subwidget.configure(text="⚙️ Configuración Avanzada ▼")
        else:
            self.settings_panel.pack(fill="x")
            self.settings_expanded.set(True)
            # Actualizar texto del botón
            for widget in self.settings_panel.master.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    for subwidget in widget.winfo_children():
                        if isinstance(subwidget, ctk.CTkButton) and "Configuración" in subwidget.cget("text"):
                            subwidget.configure(text="⚙️ Configuración Avanzada ▲")
    
    def update_resolution_label(self, value):
        """Actualizar etiqueta de resolución"""
        self.res_label.configure(text=f"{int(value)} puntos")
        
    def update_elevation_label(self, value):
        """Actualizar etiqueta de elevación"""
        self.elev_label.configure(text=f"{int(value)}°")
        
    def update_azimuth_label(self, value):
        """Actualizar etiqueta de azimut"""
        self.azim_label.configure(text=f"{int(value)}°")
        
    def set_camera_preset(self, elev, azim):
        """Establecer vista de cámara predefinida"""
        self.elev_var.set(elev)
        self.azim_var.set(azim)
        self.update_elevation_label(elev)
        self.update_azimuth_label(azim)
        
    def graficar_3d(self):
        """Generar gráfica 3D mejorada"""
        # Limpiar canvas anterior
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
            
        # Actualizar estado
        self.status_label.configure(text="Generando visualización...")
        self.graph_button.configure(state="disabled", text="⏳ Generando...")
        self.update()
        
        try:
            # Obtener valores con valores por defecto
            x0 = float(self.x_min.get()) if self.x_min.get() else -5.0
            x1 = float(self.x_max.get()) if self.x_max.get() else 5.0
            y0 = float(self.y_min.get()) if self.y_min.get() else -5.0
            y1 = float(self.y_max.get()) if self.y_max.get() else 5.0
            
            if not self.entrada_funcion.get():
                raise ValueError("Por favor, ingresa una función válida")
                
            num = int(self.resol_var.get())
            cmap = self.cmap_var.get()
            elev = float(self.elev_var.get())
            azim = float(self.azim_var.get())
            
            # Generar datos
            X, Y = generar_malla(x0, x1, y0, y1, num)
            Z = evaluar_funcion_3d(self.entrada_funcion.get(), X, Y)
            
            # Crear figura mejorada
            fig = plt.figure(figsize=(8, 5), dpi=100)
            fig.patch.set_facecolor('#111827')
            
            ax = fig.add_subplot(111, projection='3d')
            ax.set_facecolor('#111827')
            
            # Superficie con mejor configuración
            superficie = ax.plot_surface(
                X, Y, Z,
                cmap=cmap,
                alpha=0.9,
                edgecolor='white',
                linewidth=0.1,
                antialiased=True
            )
            
            # Mejorar etilado
            ax.set_title(
                f"f(x, y) = {self.entrada_funcion.get()}",
                fontsize=16,
                fontweight='bold',
                color='white',
                pad=20
            )
            ax.set_xlabel("X", fontsize=12, color='white')
            ax.set_ylabel("Y", fontsize=12, color='white')
            ax.set_zlabel("Z", fontsize=12, color='white')
            
            # Configurar vista
            ax.view_init(elev=elev, azim=azim)
            
            # Personalizar ejes
            ax.tick_params(colors='white', labelsize=10)
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            ax.grid(True, alpha=0.3)
            
            # Colorbar mejorada
            cbar = fig.colorbar(superficie, ax=ax, shrink=0.6, aspect=15, pad=0.1)
            cbar.ax.tick_params(colors='white', labelsize=10)
            
            # Layout ajustado
            fig.tight_layout()
            fig.subplots_adjust(left=0.05, right=0.9, top=0.95, bottom=0.05)
            
            # Insertar en canvas
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            widget = canvas.get_tk_widget()
            widget.configure(bg='#111827')
            widget.grid(row=0, column=0, sticky="nsew")
            
            # Actualizar estado de éxito
            self.status_label.configure(
                text="✅ Visualización generada exitosamente",
                text_color=["#10b981", "#34d399"]
            )
            
        except Exception as e:
            # Mostrar mensaje de error mejorado
            CTkMessagebox(
                title="❌ Error en la Visualización",
                message=f"No se pudo generar la gráfica:\n\n{str(e)}\n\nVerifica que la función sea válida.",
                icon="cancel"
            )
            
            # Restaurar placeholder
            self.placeholder_label = ctk.CTkLabel(
                self.canvas_frame,
                text="❌ Error al generar la visualización\nVerifica tu función e intenta nuevamente",
                font=("Segoe UI", 14),
                text_color=["#ef4444", "#f87171"]
            )
            self.placeholder_label.grid(row=0, column=0)
            
            self.status_label.configure(
                text="❌ Error en la generación",
                text_color=["#ef4444", "#f87171"]
            )
            
        finally:
            # Restaurar botón
            self.graph_button.configure(state="normal", text="🚀 Generar Visualización 3D")