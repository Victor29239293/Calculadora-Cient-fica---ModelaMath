import customtkinter as ctk
import numpy as np
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from backend.bk_vector import (
    generar_vector_aleatorio,
    sumar,
    restar,
    producto_punto,
    producto_cruzado,
    magnitud
)

class VectoresPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.current_operation = None
        self.animation_running = False
        self.setup_colors()

        # Frame principal con scroll
        self.scrollable = ctk.CTkScrollableFrame(self, fg_color=self.colors['bg_primary'])
        self.scrollable.pack(fill="both", expand=True)

        self.setup_ui()
        
    def setup_colors(self):
        """Define la paleta de colores moderna"""
        self.colors = {
            'bg_primary': '#0F0F23',
            'bg_secondary': '#1A1A2E',
            'bg_tertiary': '#16213E',
            'accent_primary': '#6C63FF',
            'accent_secondary': '#00D4FF',
            'accent_success': '#00FF88',
            'accent_warning': '#FFB800',
            'accent_error': '#FF4757',
            'text_primary': '#FFFFFF',
            'text_secondary': '#A0A0A0',
            'text_muted': '#6B7280',
        }
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        main_container = ctk.CTkFrame(self.scrollable, fg_color=self.colors['bg_primary'], corner_radius=0)
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header moderno con gradiente
        self.create_header(main_container)
        
        # Panel de control principal
        control_panel = ctk.CTkFrame(main_container, fg_color=self.colors['bg_secondary'], corner_radius=20)
        control_panel.pack(pady=(0, 20), padx=20, fill="x")
        
        # Configuración de vectores
        self.create_vector_config(control_panel)
        
        # Entrada de vectores con diseño moderno
        self.create_vector_inputs(control_panel)
        
        # Botones de operaciones con estilo premium
        self.create_operation_buttons(control_panel)
        
        # Panel de resultados
        self.create_results_panel(main_container)
        
        # Panel de visualización
        self.create_visualization_panel(main_container)
        
    def create_header(self, parent):
        """Crea el header moderno con animaciones"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent", height=100)
        header_frame.pack(fill="x", pady=(20, 30), padx=20)
        header_frame.pack_propagate(False)
        
        # Título principal con efecto
        title_frame = ctk.CTkFrame(header_frame, fg_color=self.colors['bg_secondary'], corner_radius=15)
        title_frame.pack(fill="x", pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🧮 CALCULADORA VECTORIAL",
            font=("SF Pro Display", 32, "bold"),
            text_color=self.colors['accent_primary']
        )
        title_label.pack(pady=20)
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Operaciones avanzadas con vectores en 2D y 3D",
            font=("SF Pro Text", 16),
            text_color=self.colors['text_secondary']
        )
        subtitle_label.pack(pady=(0, 20))
        
    def create_vector_config(self, parent):
        """Panel de configuración de vectores"""
        config_frame = ctk.CTkFrame(parent, fg_color=self.colors['bg_tertiary'], corner_radius=15)
        config_frame.pack(pady=20, padx=20, fill="x")
        
        config_title = ctk.CTkLabel(
            config_frame,
            text="⚙️ Configuración",
            font=("SF Pro Text", 18, "bold"),
            text_color=self.colors['text_primary']
        )
        config_title.pack(pady=(15, 10))
        
        config_content = ctk.CTkFrame(config_frame, fg_color="transparent")
        config_content.pack(pady=(0, 15), padx=20, fill="x")
        
        # Dimensión
        dim_frame = ctk.CTkFrame(config_content, fg_color=self.colors['bg_primary'], corner_radius=10)
        dim_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(dim_frame, text="Dimensión:", font=("SF Pro Text", 14), 
                    text_color=self.colors['text_secondary']).pack(pady=(10, 5), padx=15)
        
        self.dim_var = ctk.IntVar(value=3)
        dim_entry = ctk.CTkEntry(
            dim_frame,
            textvariable=self.dim_var,
            width=80,
            height=35,
            font=("SF Pro Text", 14),
            fg_color=self.colors['bg_secondary'],
            border_color=self.colors['accent_primary'],
            text_color=self.colors['text_primary']
        )
        dim_entry.pack(pady=(0, 15), padx=15)
        
        # Botón generar con animación
        generate_btn = ctk.CTkButton(
            config_content,
            text="🎲 Generar Aleatorio",
            command=self.generar_vectores,
            width=200,
            height=50,
            font=("SF Pro Text", 16, "bold"),
            fg_color=self.colors['accent_primary'],
            hover_color=self.colors['accent_secondary'],
            corner_radius=25
        )
        generate_btn.pack(side="left", padx=15)
        
    def create_vector_inputs(self, parent):
        """Entradas de vectores con diseño moderno"""
        input_frame = ctk.CTkFrame(parent, fg_color=self.colors['bg_tertiary'], corner_radius=15)
        input_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        input_title = ctk.CTkLabel(
            input_frame,
            text="📝 Vectores de Entrada",
            font=("SF Pro Text", 18, "bold"),
            text_color=self.colors['text_primary']
        )
        input_title.pack(pady=(15, 20))
        
        vectors_container = ctk.CTkFrame(input_frame, fg_color="transparent")
        vectors_container.pack(pady=(0, 20), padx=20, fill="x")
        
        # Vector A
        vector_a_frame = ctk.CTkFrame(vectors_container, fg_color=self.colors['bg_primary'], corner_radius=12)
        vector_a_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(vector_a_frame, text="Vector A", font=("SF Pro Text", 16, "bold"), 
                    text_color=self.colors['accent_primary']).pack(pady=(15, 5))
        
        self.vector_a = ctk.CTkEntry(
            vector_a_frame,
            placeholder_text="[1, 2, 3]",
            width=300,
            height=45,
            font=("SF Pro Mono", 14),
            fg_color=self.colors['bg_secondary'],
            border_color=self.colors['accent_primary'],
            text_color=self.colors['text_primary'],
            placeholder_text_color=self.colors['text_muted']
        )
        self.vector_a.pack(pady=(0, 15), padx=15)
        
        # Vector B
        vector_b_frame = ctk.CTkFrame(vectors_container, fg_color=self.colors['bg_primary'], corner_radius=12)
        vector_b_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(vector_b_frame, text="Vector B", font=("SF Pro Text", 16, "bold"), 
                    text_color=self.colors['accent_secondary']).pack(pady=(15, 5))
        
        self.vector_b = ctk.CTkEntry(
            vector_b_frame,
            placeholder_text="[4, 5, 6]",
            width=300,
            height=45,
            font=("SF Pro Mono", 14),
            fg_color=self.colors['bg_secondary'],
            border_color=self.colors['accent_secondary'],
            text_color=self.colors['text_primary'],
            placeholder_text_color=self.colors['text_muted']
        )
        self.vector_b.pack(pady=(0, 15), padx=15)
        
    def create_operation_buttons(self, parent):
        """Botones de operaciones con diseño premium"""
        operations_frame = ctk.CTkFrame(parent, fg_color=self.colors['bg_tertiary'], corner_radius=15)
        operations_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        ops_title = ctk.CTkLabel(
            operations_frame,
            text="🔧 Operaciones",
            font=("SF Pro Text", 18, "bold"),
            text_color=self.colors['text_primary']
        )
        ops_title.pack(pady=(15, 20))
        
        buttons_container = ctk.CTkFrame(operations_frame, fg_color="transparent")
        buttons_container.pack(pady=(0, 20), padx=20)
        
        operations = [
            ("➕", "Suma", self.calcular_suma, self.colors['accent_success']),
            ("➖", "Resta", self.calcular_resta, self.colors['accent_warning']),
            ("⚬", "Producto Punto", self.calcular_punto, self.colors['accent_primary']),
            ("✕", "Producto Cruz", self.calcular_cruzado, self.colors['accent_error']),
            ("📏", "Magnitud", self.calcular_magnitud, self.colors['accent_secondary']),
        ]
        
        for i, (icon, text, command, color) in enumerate(operations):
            btn_frame = ctk.CTkFrame(buttons_container, fg_color=color, corner_radius=15)
            btn_frame.grid(row=0, column=i, padx=8, pady=5)
            
            btn = ctk.CTkButton(
                btn_frame,
                text=f"{icon}\n{text}",
                command=lambda cmd=command, op=text: self.execute_operation(cmd, op),
                width=140,
                height=80,
                font=("SF Pro Text", 14, "bold"),
                fg_color="transparent",
                text_color=self.colors['text_primary']
            )
            btn.pack(padx=3, pady=3)
            
    def create_results_panel(self, parent):
        """Panel de resultados con diseño moderno"""
        results_frame = ctk.CTkFrame(parent, fg_color=self.colors['bg_secondary'], corner_radius=20)
        results_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        results_title = ctk.CTkLabel(
            results_frame,
            text="📊 Resultados",
            font=("SF Pro Text", 18, "bold"),
            text_color=self.colors['text_primary']
        )
        results_title.pack(pady=(20, 15))
        
        # Status indicator
        self.status_frame = ctk.CTkFrame(results_frame, fg_color=self.colors['bg_tertiary'], corner_radius=10)
        self.status_frame.pack(pady=(0, 15), padx=20, fill="x")
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="⏳ Listo para calcular",
            font=("SF Pro Text", 14),
            text_color=self.colors['text_secondary']
        )
        self.status_label.pack(pady=10)
        
        # Resultado con scroll
        self.resultado = ctk.CTkTextbox(
            results_frame,
            width=700,
            height=120,
            font=("SF Pro Mono", 16),
            fg_color=self.colors['bg_primary'],
            text_color=self.colors['text_primary'],
            border_color=self.colors['accent_primary'],
            corner_radius=15
        )
        self.resultado.pack(pady=(0, 20), padx=20, fill="x")
        
    def create_visualization_panel(self, parent):
        """Panel de visualización mejorado"""
        viz_frame = ctk.CTkFrame(parent, fg_color=self.colors['bg_secondary'], corner_radius=20)
        viz_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)
        
        viz_title = ctk.CTkLabel(
            viz_frame,
            text="📈 Visualización",
            font=("SF Pro Text", 18, "bold"),
            text_color=self.colors['text_primary']
        )
        viz_title.pack(pady=(20, 15))
        
        self.grafica_frame = ctk.CTkFrame(viz_frame, fg_color=self.colors['bg_primary'], corner_radius=15)
        self.grafica_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)
        
        # Placeholder para gráfica
        placeholder_label = ctk.CTkLabel(
            self.grafica_frame,
            text="🎯 La visualización aparecerá aquí",
            font=("SF Pro Text", 16),
            text_color=self.colors['text_muted']
        )
        placeholder_label.pack(expand=True)
        
    def execute_operation(self, command, operation_name):
        """Ejecuta una operación con feedback visual"""
        self.current_operation = operation_name
        self.update_status(f"🔄 Calculando {operation_name}...", self.colors['accent_warning'])
        
        # Simular procesamiento con after
        self.after(100, command)
        
    def update_status(self, message, color=None):
        """Actualiza el status con color"""
        self.status_label.configure(text=message)
        if color:
            self.status_frame.configure(fg_color=color)
        
    def mostrar_resultado(self, texto: str):
        """Muestra resultado con animación"""
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("end", texto)
        self.resultado.configure(state="disabled")
        
        # Actualizar status
        self.update_status(f"✅ {self.current_operation} completada", self.colors['accent_success'])

    def generar_vectores(self):
        """Genera vectores aleatorios con feedback"""
        try:
            self.update_status("🎲 Generando vectores...", self.colors['accent_primary'])
            dim = self.dim_var.get()
            A = generar_vector_aleatorio(dim)
            B = generar_vector_aleatorio(dim)
            
            self.vector_a.delete(0, "end")
            self.vector_b.delete(0, "end")
            self.vector_a.insert(0, str(A.tolist()))
            self.vector_b.insert(0, str(B.tolist()))
            
            self.update_status("✅ Vectores generados", self.colors['accent_success'])
            
        except Exception as e:
            self.update_status("❌ Error al generar", self.colors['accent_error'])
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

    def obtener_vectores(self):
        """Obtiene vectores con validación mejorada"""
        try:
            a = np.array(eval(self.vector_a.get()), dtype=float)
            b = np.array(eval(self.vector_b.get()), dtype=float)
            return a, b
        except Exception as e:
            self.update_status("❌ Entrada inválida", self.colors['accent_error'])
            CTkMessagebox(title="Error", message=f"Entrada inválida: {e}", icon="cancel")
            return None, None

    def calcular_suma(self):
        a, b = self.obtener_vectores()
        if a is None: return
        r = sumar(a, b)
        self.mostrar_resultado(f"Vector A + Vector B = {r}")
        self.mostrar_grafica(a, b, r)

    def calcular_resta(self):
        a, b = self.obtener_vectores()
        if a is None: return
        r = restar(a, b)
        self.mostrar_resultado(f"Vector A - Vector B = {r}")
        self.mostrar_grafica(a, b, r)

    def calcular_punto(self):
        a, b = self.obtener_vectores()
        if a is None: return
        r = producto_punto(a, b)
        self.mostrar_resultado(f"A · B = {r:.6f}")
        self.mostrar_grafica(a, b, None)

    def calcular_cruzado(self):
        a, b = self.obtener_vectores()
        if a is None: return
        try:
            r = producto_cruzado(a, b)
            self.mostrar_resultado(f"A × B = {r}")
            self.mostrar_grafica(a, b, r)
        except Exception as e:
            self.update_status("❌ Error en cálculo", self.colors['accent_error'])
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

    def calcular_magnitud(self):
        a, b = self.obtener_vectores()
        if a is None: return
        mag_a = magnitud(a)
        mag_b = magnitud(b)
        self.mostrar_resultado(f"|Vector A| = {mag_a:.6f}\n|Vector B| = {mag_b:.6f}")
        self.mostrar_grafica(a, b, None)

    def mostrar_grafica(self, a: np.ndarray, b: np.ndarray, r: np.ndarray | None):
        """Visualización mejorada con estilo moderno"""
        if a.ndim != 1 or not (a.shape == b.shape):
            return
            
        dim = a.shape[0]
        if dim not in (2, 3):
            CTkMessagebox(title="Aviso", message="Solo se grafica en 2D/3D", icon="info")
            return
            
        # Limpiar frame anterior
        for widget in self.grafica_frame.winfo_children():
            widget.destroy()
        
        # Configurar matplotlib con tema oscuro
        plt.style.use('dark_background')
        
        if dim == 2:
            fig, ax = plt.subplots(figsize=(10, 8), facecolor=self.colors['bg_primary'])
            ax.set_facecolor(self.colors['bg_primary'])
            
            # Vectores principales
            ax.quiver(0, 0, a[0], a[1], angles='xy', scale_units='xy', scale=1, 
                     color='#6C63FF', width=0.006, label='Vector A', alpha=0.9)
            ax.quiver(0, 0, b[0], b[1], angles='xy', scale_units='xy', scale=1, 
                     color='#00D4FF', width=0.006, label='Vector B', alpha=0.9)
            
            if r is not None:
                ax.quiver(0, 0, r[0], r[1], angles='xy', scale_units='xy', scale=1, 
                         color='#00FF88', width=0.008, label='Resultado', alpha=0.9)
            
            # Estilo de grid moderno
            ax.grid(True, alpha=0.3, linestyle='--', color='#404040')
            ax.set_aspect('equal')
            ax.legend(frameon=True, facecolor=self.colors['bg_secondary'], 
                     edgecolor='none', fontsize=12)
            
        else:  # 3D
            fig = plt.figure(figsize=(12, 10), facecolor=self.colors['bg_primary'])
            ax = fig.add_subplot(111, projection='3d')
            ax.set_facecolor(self.colors['bg_primary'])
            
            # Vectores 3D con mejor estilo
            ax.quiver(0,0,0, a[0], a[1], a[2], color='#6C63FF', 
                     arrow_length_ratio=0.1, linewidth=3, label='Vector A', alpha=0.9)
            ax.quiver(0,0,0, b[0], b[1], b[2], color='#00D4FF', 
                     arrow_length_ratio=0.1, linewidth=3, label='Vector B', alpha=0.9)
            
            if r is not None:
                ax.quiver(0,0,0, r[0], r[1], r[2], color='#00FF88', 
                         arrow_length_ratio=0.1, linewidth=4, label='Resultado', alpha=0.9)
            
            # Configuración 3D mejorada
            max_range = max(np.max(np.abs(a)), np.max(np.abs(b)))
            if r is not None:
                max_range = max(max_range, np.max(np.abs(r)))
            
            limit = max_range * 1.2
            ax.set_xlim(-limit, limit)
            ax.set_ylim(-limit, limit)
            ax.set_zlim(-limit, limit)
            
            ax.set_xlabel('X', fontsize=12, color='white')
            ax.set_ylabel('Y', fontsize=12, color='white')
            ax.set_zlabel('Z', fontsize=12, color='white')
            
            ax.legend(fontsize=12)
            
        # Integrar con CustomTkinter
        canvas = FigureCanvasTkAgg(fig, master=self.grafica_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        plt.close(fig)  # Limpiar memoria