import customtkinter as ctk
import numpy as np
from CTkMessagebox import CTkMessagebox
from backend.bk_matriz import (
    crear_matriz_aleatoria,
    sumar,
    restar,
    multiplicar,
    determinante,
    inversa,
    resolver_sistema
)

# Paleta de colores moderna para matrices
class MatrixColorScheme:
    DARK_BG = "#0A0C14"
    PANEL_BG = "#151922"
    CARD_BG = "#1E2532"
    SURFACE_BG = "#252D3D"
    MATRIX_BG = "#2A3441"
    CELL_BG = "#343E4F"
    ACCENT_PRIMARY = "#00D4FF"
    ACCENT_SECONDARY = "#FF6B6B"
    ACCENT_SUCCESS = "#4ECDC4"
    ACCENT_WARNING = "#FFD93D"
    ACCENT_PURPLE = "#A8E6CF"
    TEXT_PRIMARY = "#F8FAFC"
    TEXT_SECONDARY = "#CBD5E1"
    TEXT_MUTED = "#94A3B8"
    BORDER = "#334155"
    HOVER = "#475569"

class MatricesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=MatrixColorScheme.DARK_BG)
        
        # Variables de configuración
        self.filas_A = ctk.IntVar(value=3)
        self.columnas_A = ctk.IntVar(value=3)
        self.filas_B = ctk.IntVar(value=3)
        self.columnas_B = ctk.IntVar(value=3)
        
        # Variables para matrices
        self.entradas_A = []
        self.entradas_B = []
        
        # Crear layout principal
        self._create_layout()

    def _create_layout(self):
        """Crear el layout principal de la aplicación"""
        # Contenedor principal con scroll
        self.main_container = ctk.CTkScrollableFrame(
            self,
            fg_color=MatrixColorScheme.DARK_BG,
            scrollbar_button_color=MatrixColorScheme.ACCENT_PRIMARY,
            scrollbar_button_hover_color=MatrixColorScheme.HOVER
        )
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        self._create_header()
        
        # Configuración de dimensiones
        self._create_config_section()
        
        # Área de matrices
        self._create_matrix_area()
        
        # Botones de operaciones
        self._create_operations_section()
        
        # Generar matrices iniciales
        self.generar_matrices()

    def _create_header(self):
        """Crear header con diseño moderno"""
        header = ctk.CTkFrame(
            self.main_container,
            fg_color=MatrixColorScheme.PANEL_BG,
            height=120,
            corner_radius=20,
            border_width=1,
            border_color=MatrixColorScheme.BORDER
        )
        header.pack(fill="x", padx=15, pady=(0, 25))
        header.pack_propagate(False)
        
        # Contenido del header
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True)
        
        # Título principal
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(expand=True)
        
        ctk.CTkLabel(
            title_frame,
            text="🧮 Calculadora de Matrices",
            font=("Segoe UI", 32, "bold"),
            text_color=MatrixColorScheme.ACCENT_PRIMARY
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            title_frame,
            text="Operaciones algebraicas • Determinantes • Sistemas lineales",
            font=("Segoe UI", 14),
            text_color=MatrixColorScheme.TEXT_MUTED
        ).pack()

    def _create_config_section(self):
        """Crear sección de configuración de dimensiones"""
        config_card = ctk.CTkFrame(
            self.main_container,
            fg_color=MatrixColorScheme.CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=MatrixColorScheme.BORDER
        )
        config_card.pack(fill="x", padx=15, pady=(0, 25))
        
        # Título de la sección
        ctk.CTkLabel(
            config_card,
            text="⚙️ Configuración de Matrices",
            font=("Segoe UI", 18, "bold"),
            text_color=MatrixColorScheme.TEXT_PRIMARY
        ).pack(pady=(20, 15))
        
        # Frame para controles
        controls_frame = ctk.CTkFrame(config_card, fg_color="transparent")
        controls_frame.pack(pady=(0, 20))
        
        # Configurar grid
        controls_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        # Controles para Matriz A
        self._create_matrix_controls(controls_frame, "A", 0, MatrixColorScheme.ACCENT_PRIMARY)
        
        # Separador visual
        separator = ctk.CTkFrame(
            controls_frame,
            fg_color=MatrixColorScheme.BORDER,
            width=2,
            height=80
        )
        separator.grid(row=0, column=2, padx=20, sticky="ns")
        
        # Controles para Matriz B
        self._create_matrix_controls(controls_frame, "B", 3, MatrixColorScheme.ACCENT_SECONDARY)
        
        # Botones de acción
        action_frame = ctk.CTkFrame(config_card, fg_color="transparent")
        action_frame.pack(pady=(0, 20))
        
        generar_btn = ctk.CTkButton(
            action_frame,
            text="🔄 Generar Matrices",
            command=self.generar_matrices,
            width=180,
            height=50,
            font=("Segoe UI", 14, "bold"),
            fg_color=MatrixColorScheme.ACCENT_SUCCESS,
            hover_color="#45B7AF",
            corner_radius=12
        )
        generar_btn.pack(side="left", padx=(0, 15))
        
        aleatorio_btn = ctk.CTkButton(
            action_frame,
            text="🎲 Valores Aleatorios",
            command=self.generar_valores_aleatorios,
            width=180,
            height=50,
            font=("Segoe UI", 14, "bold"),
            fg_color=MatrixColorScheme.ACCENT_WARNING,
            hover_color="#E6C533",
            text_color="#1A1A1A",
            corner_radius=12
        )
        aleatorio_btn.pack(side="left")

    def _create_matrix_controls(self, parent, matrix_name, start_col, accent_color):
        """Crear controles para una matriz específica"""
        # Título de la matriz
        title_label = ctk.CTkLabel(
            parent,
            text=f"Matriz {matrix_name}",
            font=("Segoe UI", 16, "bold"),
            text_color=accent_color
        )
        title_label.grid(row=0, column=start_col, columnspan=2, pady=(0, 10))
        
        # Controles de filas
        filas_frame = ctk.CTkFrame(parent, fg_color="transparent")
        filas_frame.grid(row=1, column=start_col, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(
            filas_frame,
            text="Filas:",
            font=("Segoe UI", 12),
            text_color=MatrixColorScheme.TEXT_SECONDARY
        ).pack(anchor="w", pady=(0, 5))
        
        filas_var = self.filas_A if matrix_name == "A" else self.filas_B
        filas_entry = ctk.CTkEntry(
            filas_frame,
            textvariable=filas_var,
            width=80,
            height=35,
            font=("JetBrains Mono", 12),
            fg_color=MatrixColorScheme.SURFACE_BG,
            border_color=accent_color,
            text_color=MatrixColorScheme.TEXT_PRIMARY
        )
        filas_entry.pack(fill="x")
        
        # Controles de columnas
        cols_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cols_frame.grid(row=1, column=start_col + 1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(
            cols_frame,
            text="Columnas:",
            font=("Segoe UI", 12),
            text_color=MatrixColorScheme.TEXT_SECONDARY
        ).pack(anchor="w", pady=(0, 5))
        
        cols_var = self.columnas_A if matrix_name == "A" else self.columnas_B
        cols_entry = ctk.CTkEntry(
            cols_frame,
            textvariable=cols_var,
            width=80,
            height=35,
            font=("JetBrains Mono", 12),
            fg_color=MatrixColorScheme.SURFACE_BG,
            border_color=accent_color,
            text_color=MatrixColorScheme.TEXT_PRIMARY
        )
        cols_entry.pack(fill="x")

    def _create_matrix_area(self):
        """Crear área para mostrar las matrices"""
        self.matrix_container = ctk.CTkFrame(
            self.main_container,
            fg_color=MatrixColorScheme.CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=MatrixColorScheme.BORDER
        )
        self.matrix_container.pack(fill="both", expand=True, padx=15, pady=(0, 25))
        
        # Título del área de matrices
        ctk.CTkLabel(
            self.matrix_container,
            text="📊 Matrices de Trabajo",
            font=("Segoe UI", 18, "bold"),
            text_color=MatrixColorScheme.TEXT_PRIMARY
        ).pack(pady=(20, 15))
        
        # Frame scrollable para matrices
        self.matrices_scroll = ctk.CTkScrollableFrame(
            self.matrix_container,
            fg_color=MatrixColorScheme.SURFACE_BG,
            corner_radius=12,
            height=230,
            scrollbar_button_color=MatrixColorScheme.ACCENT_PRIMARY,
            scrollbar_button_hover_color=MatrixColorScheme.HOVER
        )
        self.matrices_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _create_operations_section(self):
        """Crear sección de operaciones"""
        operations_card = ctk.CTkFrame(
            self.main_container,
            fg_color=MatrixColorScheme.CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=MatrixColorScheme.BORDER
        )
        operations_card.pack(fill="x", padx=15, pady=(0, 20))
        
        # Título
        ctk.CTkLabel(
            operations_card,
            text="🔢 Operaciones Disponibles",
            font=("Segoe UI", 18, "bold"),
            text_color=MatrixColorScheme.TEXT_PRIMARY
        ).pack(pady=(20, 15))
        
        # Frame para botones
        buttons_frame = ctk.CTkFrame(operations_card, fg_color="transparent")
        buttons_frame.pack(pady=(0, 20))
        
        # Definir operaciones con colores específicos
        operations = [
            ("A + B", "+", MatrixColorScheme.ACCENT_SUCCESS, "➕"),
            ("A - B", "-", MatrixColorScheme.ACCENT_WARNING, "➖"),
            ("A × B", "*", MatrixColorScheme.ACCENT_SECONDARY, "✖️"),
            ("Det(A)", "det", MatrixColorScheme.ACCENT_PRIMARY, "🔢"),
            ("A⁻¹", "inv", MatrixColorScheme.ACCENT_PURPLE, "🔄"),
            ("B⁻¹", "inv_b", MatrixColorScheme.ACCENT_PURPLE, "🔃"),
            ("Ax = B", "solve", "#FF9F43", "🎯")
        ]
        
        # Crear botones en grid
        for i, (text, op_type, color, icon) in enumerate(operations):
            row = i // 4
            col = i % 4

            btn = ctk.CTkButton(
            buttons_frame,
            text=f"{icon} {text}",
            command=lambda t=op_type: self.realizar_operacion(t),
            width=160,
            height=50,
            font=("Segoe UI", 13, "bold"),
            fg_color=color,
            hover_color=self._darken_color(color),
            corner_radius=12,
            border_width=1,
            border_color=self._lighten_color(color),
            text_color="#1A1A1A"  # Letras negras
            )
            btn.grid(row=row, column=col, padx=8, pady=8)

    def _darken_color(self, hex_color):
        """Oscurecer un color hexadecimal para hover"""
        # Implementación simple para oscurecer colores
        color_map = {
            MatrixColorScheme.ACCENT_SUCCESS: "#45B7AF",
            MatrixColorScheme.ACCENT_WARNING: "#E6C533",
            MatrixColorScheme.ACCENT_SECONDARY: "#E55A5A",
            MatrixColorScheme.ACCENT_PRIMARY: "#00BFDD",
            MatrixColorScheme.ACCENT_PURPLE: "#98D982",
            "#FF9F43": "#E6903D"
        }
        return color_map.get(hex_color, hex_color)

    def _lighten_color(self, hex_color):
        """Aclarar un color hexadecimal para bordes"""
        color_map = {
            MatrixColorScheme.ACCENT_SUCCESS: "#5CEFE6",
            MatrixColorScheme.ACCENT_WARNING: "#FFF952",
            MatrixColorScheme.ACCENT_SECONDARY: "#FF8F8F",
            MatrixColorScheme.ACCENT_PRIMARY: "#33E0FF",
            MatrixColorScheme.ACCENT_PURPLE: "#C7F0BA",
            "#FF9F43": "#FFB366"
        }
        return color_map.get(hex_color, hex_color)

    def crear_matriz(self, nombre, filas, columnas, parent_frame):
        """Crear una matriz visual mejorada"""
        # Frame principal para la matriz
        matrix_frame = ctk.CTkFrame(
            parent_frame,
            fg_color=MatrixColorScheme.MATRIX_BG,
            corner_radius=12,
            border_width=1,
            border_color=MatrixColorScheme.BORDER
        )
        
        # Color del título según la matriz
        title_color = MatrixColorScheme.ACCENT_PRIMARY if nombre == "A" else MatrixColorScheme.ACCENT_SECONDARY
        
        # Título de la matriz
        title_label = ctk.CTkLabel(
            matrix_frame,
            text=f"Matriz {nombre} ({filas}×{columnas})",
            font=("Segoe UI", 16, "bold"),
            text_color=title_color
        )
        title_label.pack(pady=(15, 10))
        
        # Frame para las celdas
        cells_frame = ctk.CTkFrame(matrix_frame, fg_color="transparent")
        cells_frame.pack(padx=20, pady=(0, 20))
        
        # Crear las celdas de entrada
        entradas = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                cell = ctk.CTkEntry(
                    cells_frame,
                    width=70,
                    height=40,
                    font=("JetBrains Mono", 12),
                    fg_color=MatrixColorScheme.CELL_BG,
                    border_color=MatrixColorScheme.BORDER,
                    text_color=MatrixColorScheme.TEXT_PRIMARY,
                    placeholder_text="0",
                    placeholder_text_color=MatrixColorScheme.TEXT_MUTED,
                    corner_radius=8
                )
                cell.grid(row=i, column=j, padx=3, pady=3)
                
                # Efecto hover para las celdas
                def on_enter(event, entry=cell):
                    entry.configure(border_color=title_color)
                def on_leave(event, entry=cell):
                    entry.configure(border_color=MatrixColorScheme.BORDER)
                
                cell.bind("<Enter>", on_enter)
                cell.bind("<Leave>", on_leave)
                
                fila.append(cell)
            entradas.append(fila)
        
        # Guardar referencias
        if nombre == "A":
            self.entradas_A = entradas
        else:
            self.entradas_B = entradas
        
        return matrix_frame

    def generar_matrices(self):
        """Generar las matrices con validación mejorada"""
        # Limpiar área de matrices
        for widget in self.matrices_scroll.winfo_children():
            widget.destroy()
        
        try:
            fA, cA = self.filas_A.get(), self.columnas_A.get()
            fB, cB = self.filas_B.get(), self.columnas_B.get()
            
            # Validación
            if min(fA, cA, fB, cB) <= 0:
                raise ValueError("Las dimensiones deben ser positivas")
            if max(fA, cA, fB, cB) > 10:
                raise ValueError("Las dimensiones no pueden exceder 10")
            
            # Crear contenedor para ambas matrices
            matrices_container = ctk.CTkFrame(self.matrices_scroll, fg_color="transparent")
            matrices_container.pack(fill="x", pady=10)
            
            # Crear matrices lado a lado
            matrix_a = self.crear_matriz("A", fA, cA, matrices_container)
            matrix_a.pack(side="left", padx=(0, 20), fill="y")
            
            matrix_b = self.crear_matriz("B", fB, cB, matrices_container)
            matrix_b.pack(side="left", fill="y")
            
        except ValueError as e:
            CTkMessagebox(
                title="⚠️ Error de Validación",
                message=str(e),
                icon="warning"
            )
        except Exception as e:
            CTkMessagebox(
                title="❌ Error",
                message=f"Error al generar matrices: {str(e)}",
                icon="cancel"
            )

    def generar_valores_aleatorios(self):
        """Generar valores aleatorios para las matrices"""
        self.generar_matrices()
        
        try:
            fA, cA = self.filas_A.get(), self.columnas_A.get()
            fB, cB = self.filas_B.get(), self.columnas_B.get()
            
            # Generar matrices aleatorias
            A = crear_matriz_aleatoria(fA, cA, low=1, high=10)
            B = crear_matriz_aleatoria(fB, cB, low=1, high=10)
            
            # Llenar Matriz A
            for i in range(len(self.entradas_A)):
                for j in range(len(self.entradas_A[0])):
                    self.entradas_A[i][j].delete(0, "end")
                    self.entradas_A[i][j].insert(0, str(int(A[i, j])))
            
            # Llenar Matriz B
            for i in range(len(self.entradas_B)):
                for j in range(len(self.entradas_B[0])):
                    self.entradas_B[i][j].delete(0, "end")
                    self.entradas_B[i][j].insert(0, str(int(B[i, j])))
                    
        except Exception as e:
            CTkMessagebox(
                title="❌ Error",
                message=f"Error al generar valores aleatorios: {str(e)}",
                icon="cancel"
            )

    def leer_matriz(self, entradas):
        """Leer valores de una matriz con validación mejorada"""
        try:
            matriz = []
            for fila in entradas:
                fila_valores = []
                for entry in fila:
                    valor = entry.get().strip()
                    if not valor:
                        valor = "0"
                    fila_valores.append(float(valor))
                matriz.append(fila_valores)
            return np.array(matriz)
        except ValueError:
            CTkMessagebox(
                title="⚠️ Error de Entrada",
                message="Por favor, ingresa solo números válidos en las matrices.",
                icon="warning"
            )
            return None
        except Exception as e:
            CTkMessagebox(
                title="❌ Error",
                message=f"Error al leer matriz: {str(e)}",
                icon="cancel"
            )
            return None

    def realizar_operacion(self, tipo):
        """Realizar operación matricial con manejo de errores mejorado"""
        A = self.leer_matriz(self.entradas_A)
        B = self.leer_matriz(self.entradas_B) if tipo in ["+", "-", "*", "solve", "inv_b"] else None
        
        if A is None or (B is None and tipo in ["+", "-", "*", "solve", "inv_b"]):
            return
        
        try:
            if tipo == "+":
                resultado = sumar(A, B)
                titulo = "Suma de Matrices (A + B)"
            elif tipo == "-":
                resultado = restar(A, B)
                titulo = "Resta de Matrices (A - B)"
            elif tipo == "*":
                resultado = multiplicar(A, B)
                titulo = "Multiplicación de Matrices (A × B)"
            elif tipo == "det":
                resultado = determinante(A)
                titulo = "Determinante de la Matriz A"
            elif tipo == "inv":
                resultado = inversa(A)
                titulo = "Inversa de la Matriz A"
            elif tipo == "inv_b":
                resultado = inversa(B)
                titulo = "Inversa de la Matriz B"
            elif tipo == "solve":
                resultado = resolver_sistema(A, B)
                titulo = "Solución del Sistema Ax = B"
            else:
                return
                
            self.mostrar_resultado(resultado, titulo)
            
        except Exception as e:
            CTkMessagebox(
                title="❌ Error de Operación",
                message=f"No se pudo realizar la operación:\n{str(e)}",
                icon="cancel"
            )

    def mostrar_resultado(self, resultado, titulo):
        """Mostrar resultado en ventana modal mejorada"""
        # Crear ventana modal
        ventana = ctk.CTkToplevel(self)
        ventana.title("Resultado de la Operación")
        ventana.geometry("800x600")
        ventana.grab_set()
        ventana.configure(fg_color=MatrixColorScheme.DARK_BG)
        
        # Centrar ventana
        ventana.transient(self)
        
        # Header de la ventana
        header = ctk.CTkFrame(
            ventana,
            fg_color=MatrixColorScheme.PANEL_BG,
            height=80,
            corner_radius=0
        )
        header.pack(fill="x")
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text=titulo,
            font=("Segoe UI", 20, "bold"),
            text_color=MatrixColorScheme.ACCENT_PRIMARY
        ).pack(expand=True)
        
        # Área de contenido
        content_frame = ctk.CTkScrollableFrame(
            ventana,
            fg_color=MatrixColorScheme.CARD_BG,
            scrollbar_button_color=MatrixColorScheme.ACCENT_PRIMARY
        )
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mostrar resultado
        if isinstance(resultado, (float, int, np.floating, np.integer)):
            # Resultado escalar
            result_frame = ctk.CTkFrame(
                content_frame,
                fg_color=MatrixColorScheme.SURFACE_BG,
                corner_radius=12,
                border_width=1,
                border_color=MatrixColorScheme.BORDER
            )
            result_frame.pack(fill="x", pady=20)
            
            ctk.CTkLabel(
                result_frame,
                text=f"{float(resultado):.6f}",
                font=("JetBrains Mono", 32, "bold"),
                text_color=MatrixColorScheme.ACCENT_SUCCESS
            ).pack(pady=40)
            
        else:
            # Resultado matricial
            matrix_frame = ctk.CTkFrame(
                content_frame,
                fg_color=MatrixColorScheme.SURFACE_BG,
                corner_radius=12,
                border_width=1,
                border_color=MatrixColorScheme.BORDER
            )
            matrix_frame.pack(fill="both", expand=True, pady=20)
            
            # Grid para la matriz resultado
            cells_container = ctk.CTkFrame(matrix_frame, fg_color="transparent")
            cells_container.pack(expand=True, pady=20)
            
            for i, fila in enumerate(resultado):
                for j, val in enumerate(fila):
                    cell = ctk.CTkLabel(
                        cells_container,
                        text=f"{float(val):.4f}",
                        font=("JetBrains Mono", 14),
                        fg_color=MatrixColorScheme.CELL_BG,
                        text_color=MatrixColorScheme.TEXT_PRIMARY,
                        width=90,
                        height=40,
                        corner_radius=8
                    )
                    cell.grid(row=i, column=j, padx=3, pady=3)
        
        # Botón cerrar
        close_btn = ctk.CTkButton(
            ventana,
            text="✅ Cerrar",
            command=ventana.destroy,
            width=120,
            height=40,
            font=("Segoe UI", 14, "bold"),
            fg_color=MatrixColorScheme.ACCENT_SUCCESS,
            hover_color="#45B7AF",
            corner_radius=12
        )
        close_btn.pack(pady=20)