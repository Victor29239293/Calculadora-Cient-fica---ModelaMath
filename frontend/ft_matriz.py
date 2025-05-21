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


class MatricesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#1a1c1e")

        ctk.CTkLabel(
            self,
            text="🧮 Operaciones con Matrices",
            font=("Segoe UI", 26, "bold"),
            text_color="#6c63ff"
        ).pack(pady=20)

        config_frame = ctk.CTkFrame(self, fg_color="#23272a")
        config_frame.pack(padx=20, pady=10, fill="x")

        self.filas_A = ctk.IntVar(value=3)
        self.columnas_A = ctk.IntVar(value=3)
        self.filas_B = ctk.IntVar(value=3)
        self.columnas_B = ctk.IntVar(value=3)

        etiquetas = ["Filas A:", "Columnas A:", "Filas B:", "Columnas B:"]
        variables = [self.filas_A, self.columnas_A, self.filas_B, self.columnas_B]

        for i, (label, var) in enumerate(zip(etiquetas, variables)):
            ctk.CTkLabel(config_frame, text=label, font=("Segoe UI", 14)).grid(
                row=0, column=i * 2, padx=5, pady=10
            )
            ctk.CTkEntry(config_frame, textvariable=var, width=50).grid(
                row=0, column=i * 2 + 1
            )

        ctk.CTkButton(
            config_frame,
            text="Generar",
            command=self.generar_matrices
        ).grid(row=0, column=8, padx=15)
        ctk.CTkButton(
            config_frame,
            text="Aleatorio",
            command=self.generar_valores_aleatorios
        ).grid(row=0, column=9, padx=5)

        self.scroll_frame = ctk.CTkFrame(self)
        self.scroll_frame.pack(expand=True, fill="both", padx=20, pady=10)

        self.canvas = ctk.CTkCanvas(
            self.scroll_frame,
            bg="#1a1c1e",
            highlightthickness=0
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scroll_y = ctk.CTkScrollbar(
            self.scroll_frame,
            orientation="vertical",
            command=self.canvas.yview
        )
        self.scroll_y.pack(side="right", fill="y")

        self.scroll_x = ctk.CTkScrollbar(
            self,
            orientation="horizontal",
            command=self.canvas.xview
        )
        self.scroll_x.pack(fill="x")

        self.canvas.configure(
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set
        )

        self.matriz_frame = ctk.CTkFrame(
            self.canvas,
            fg_color="#1e1e1e"
        )
        self.canvas_id = self.canvas.create_window(
            (0, 0), window=self.matriz_frame,
            anchor="nw",
            tags="matriz_container"
        )

        self.matriz_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind("<Configure>", self.centrar_matrices)

        op_frame = ctk.CTkFrame(self, fg_color="#23272a")
        op_frame.pack(padx=10, pady=20)

        botones = [
            ("A + B", "+"), ("A - B", "-"), ("A x B", "*"),
            ("Det(A)", "det"), ("Inv(A)", "inv"), ("Inv(B)", "inv_b"),
            ("Resolver Ax=B", "solve")
        ]

        for i, (texto, tipo) in enumerate(botones):
            ctk.CTkButton(
                op_frame,
                text=texto,
                width=130,
                height=36,
                corner_radius=10,
                fg_color="#6c63ff",
                hover_color="#7d74ff",
                text_color="#ffffff",
                font=("Segoe UI", 14),
                command=lambda t=tipo: self.realizar_operacion(t)
            ).grid(row=0, column=i, padx=8, pady=5)

        self.entradas_A = []
        self.entradas_B = []
        self.generar_matrices()

    def centrar_matrices(self, event=None):
        self.canvas.update_idletasks()
        ancho_canvas = self.canvas.winfo_width()
        ancho_frame = self.matriz_frame.winfo_reqwidth()
        offset = max((ancho_canvas - ancho_frame) // 2, 0)
        self.canvas.coords("matriz_container", offset, 0)

    def crear_matriz(self, nombre, filas, columnas, offset_col):
        label = ctk.CTkLabel(
            self.matriz_frame,
            text=f"Matriz {nombre}",
            font=("Segoe UI", 16, "bold"),
            text_color="#f0f0f0"
        )
        label.grid(row=0, column=offset_col, columnspan=columnas, pady=(10, 5))

        fondo = ctk.CTkFrame(
            self.matriz_frame,
            fg_color="#2f2f2f",
            corner_radius=10
        )
        fondo.grid(row=1, column=offset_col, columnspan=columnas, padx=10, pady=5)

        entradas = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                entry = ctk.CTkEntry(fondo, width=60)
                entry.grid(row=i, column=j, padx=4, pady=4)
                fila.append(entry)
            entradas.append(fila)

        if nombre == "A":
            self.entradas_A = entradas
        else:
            self.entradas_B = entradas

    def generar_matrices(self):
        for widget in self.matriz_frame.winfo_children():
            widget.destroy()
        try:
            fA, cA = self.filas_A.get(), self.columnas_A.get()
            fB, cB = self.filas_B.get(), self.columnas_B.get()
            if min(fA, cA, fB, cB) <= 0 or max(fA, cA, fB, cB) > 15:
                raise ValueError
            self.crear_matriz("A", fA, cA, 0)
            self.crear_matriz("B", fB, cB, cA + 2)
            self.centrar_matrices()
        except Exception:
            CTkMessagebox(title="Error", message="Dimensiones inválidas", icon="cancel")

    def generar_valores_aleatorios(self):
        self.generar_matrices()
        try:
            A = crear_matriz_aleatoria(
                self.filas_A.get(),
                self.columnas_A.get(),
                low=1, high=20
            )
            B = crear_matriz_aleatoria(
                self.filas_B.get(),
                self.columnas_B.get(),
                low=1, high=20
            )
            for i in range(len(self.entradas_A)):
                for j in range(len(self.entradas_A[0])):
                    self.entradas_A[i][j].insert(0, str(A[i, j]))
            for i in range(len(self.entradas_B)):
                for j in range(len(self.entradas_B[0])):
                    self.entradas_B[i][j].insert(0, str(B[i, j]))
        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo generar aleatorio: {e}", icon="cancel")

    def leer_matriz(self, entradas):
        try:
            return np.array([
                [float(entry.get()) for entry in fila]
                for fila in entradas
            ])
        except Exception:
            CTkMessagebox(
                title="Error",
                message="Asegúrate de ingresar solo números",
                icon="cancel"
            )
            return None

    def realizar_operacion(self, tipo):
        A = self.leer_matriz(self.entradas_A)
        B = self.leer_matriz(self.entradas_B) if tipo in ["+", "-", "*", "solve", "inv_b"] else None

        if A is None or (B is None and tipo in ["+", "-", "*", "solve", "inv_b"]):
            return

        try:
            if tipo == "+":
                resultado = sumar(A, B)
            elif tipo == "-":
                resultado = restar(A, B)
            elif tipo == "*":
                resultado = multiplicar(A, B)
            elif tipo == "det":
                resultado = determinante(A)
            elif tipo == "inv":
                resultado = inversa(A)
            elif tipo == "inv_b":
                resultado = inversa(B)
            elif tipo == "solve":
                resultado = resolver_sistema(A, B)
            else:
                return
            self.mostrar_resultado(resultado)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Ocurrió un error:\n{e}", icon="cancel")

    def mostrar_resultado(self, resultado):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Resultado de la Operación")
        ventana.geometry("720x480")
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="Resultado:",
            font=("Segoe UI", 18, "bold"),
            text_color="#6c63ff"
        ).pack(pady=10)

        frame = ctk.CTkFrame(ventana, fg_color="#1e1e1e")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        if isinstance(resultado, (float, int, np.floating)):
            label_result = ctk.CTkLabel(
                frame,
                text=f"{resultado:.4f}",
                font=("Consolas", 24),
                text_color="#f0f0f0"
            )
            label_result.pack(expand=True)
        else:
            for i, fila in enumerate(resultado):
                for j, val in enumerate(fila):
                    cell = ctk.CTkLabel(
                        frame,
                        text=f"{val:.4f}",
                        font=("Consolas", 14),
                        fg_color="#292d32",
                        text_color="#f0f0f0",
                        width=80,
                        height=30,
                        corner_radius=6
                    )
                    cell.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
