import customtkinter as ctk
import numpy as np
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
        self.configure(fg_color="#121212")

        ctk.CTkLabel(self, text="📐 Operaciones con Vectores", font=("Segoe UI", 26, "bold"),
            text_color="#6c63ff").pack(pady=20)

        config_frame = ctk.CTkFrame(self)
        config_frame.pack(pady=10)

        ctk.CTkLabel(config_frame, text="Dimensión:", font=("Arial", 14)).grid(row=0, column=0, padx=5)
        self.dim_var = ctk.IntVar(value=3)
        ctk.CTkEntry(config_frame, textvariable=self.dim_var, width=60).grid(row=0, column=1, padx=5)
        ctk.CTkButton(config_frame, text="Generar Aleatorio", command=self.generar_vectores).grid(row=0, column=2, padx=10)

        entrada_frame = ctk.CTkFrame(self)
        entrada_frame.pack(pady=10, padx=20)

        self.vector_a = ctk.CTkEntry(entrada_frame, placeholder_text="Vector A (ej: [1,2,3])", width=300)
        self.vector_a.grid(row=0, column=0, padx=10, pady=10)

        self.vector_b = ctk.CTkEntry(entrada_frame, placeholder_text="Vector B (ej: [4,5,6])", width=300)
        self.vector_b.grid(row=0, column=1, padx=10, pady=10)

        botones_frame = ctk.CTkFrame(self)
        botones_frame.pack(pady=10)

        acciones = [
            ("➕ Suma", self.calcular_suma),
            ("➖ Resta", self.calcular_resta),
            ("✴ Punto", self.calcular_punto),
            ("✳ Cruzado", self.calcular_cruzado),
            ("📏 Magnitud", self.calcular_magnitud),
        ]
        for i, (texto, cmd) in enumerate(acciones):
            ctk.CTkButton(botones_frame, text=texto, command=cmd, width=140).grid(row=0, column=i, padx=8)

        ctk.CTkLabel(self, text="Resultado:", font=("Arial", 16)).pack(pady=(10, 0))
        self.resultado = ctk.CTkTextbox(self, width=700, height=70, font=("Courier", 14))
        self.resultado.pack(padx=20, pady=10)

        self.grafica_frame = ctk.CTkFrame(self)
        self.grafica_frame.pack(pady=10, fill="both", expand=True)

    def mostrar_resultado(self, texto: str):
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("end", texto)
        self.resultado.configure(state="disabled")

    def generar_vectores(self):
        try:
            dim = self.dim_var.get()
            A = generar_vector_aleatorio(dim)
            B = generar_vector_aleatorio(dim)
            self.vector_a.delete(0, "end")
            self.vector_b.delete(0, "end")
            self.vector_a.insert(0, str(A.tolist()))
            self.vector_b.insert(0, str(B.tolist()))
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

    def obtener_vectores(self):
        try:
            a = np.array(eval(self.vector_a.get()), dtype=float)
            b = np.array(eval(self.vector_b.get()), dtype=float)
            return a, b
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Entrada inválida: {e}", icon="cancel")
            return None, None

    def calcular_suma(self):
        a, b = self.obtener_vectores()
        if a is None: return
        r = sumar(a, b)
        self.mostrar_resultado(f"A + B = {r}")
        self.mostrar_grafica(a, b, r)

    def calcular_resta(self):
        a, b = self.obtener_vectores()
        if a is None: return
        r = restar(a, b)
        self.mostrar_resultado(f"A - B = {r}")
        self.mostrar_grafica(a, b, r)

    def calcular_punto(self):
        a, b = self.obtener_vectores()
        if a is None: return
        r = producto_punto(a, b)
        self.mostrar_resultado(f"A · B = {r}")
        self.mostrar_grafica(a, b, None)

    def calcular_cruzado(self):
        a, b = self.obtener_vectores()
        if a is None: return
        try:
            r = producto_cruzado(a, b)
            self.mostrar_resultado(f"A × B = {r}")
            self.mostrar_grafica(a, b, r)
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

    def calcular_magnitud(self):
        a, b = self.obtener_vectores()
        if a is None: return
        mag_a = magnitud(a)
        mag_b = magnitud(b)
        self.mostrar_resultado(f"|A| = {mag_a:.4f}\n|B| = {mag_b:.4f}")
        self.mostrar_grafica(a, b, None)

    def mostrar_grafica(self, a: np.ndarray, b: np.ndarray, r: np.ndarray | None):
        if a.ndim != 1 or not (a.shape == b.shape):
            return
        dim = a.shape[0]
        if dim not in (2, 3):
            CTkMessagebox(title="Aviso", message="Solo se grafica en 2D/3D", icon="info")
            return
        for w in self.grafica_frame.winfo_children():
            w.destroy()
        
        if dim == 2:
            fig, ax = plt.subplots()
            ax.quiver(0, 0, a[0], a[1], angles='xy', scale_units='xy', scale=1, label='A')
            ax.quiver(0, 0, b[0], b[1], angles='xy', scale_units='xy', scale=1, label='B')
            if r is not None:
                ax.quiver(0, 0, r[0], r[1], angles='xy', scale_units='xy', scale=1, label='R')
            ax.set_aspect('equal'); ax.grid(True)
            ax.legend()
        else:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.quiver(0,0,0, a[0], a[1], a[2], color='blue', label='A')
            ax.quiver(0,0,0, b[0], b[1], b[2], color='green', label='B')
            if r is not None:
                ax.quiver(0,0,0, r[0], r[1], r[2], color='red', label='R')
            ax.set_xlim(-20,20); ax.set_ylim(-20,20); ax.set_zlim(-20,20)
            ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.grafica_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)