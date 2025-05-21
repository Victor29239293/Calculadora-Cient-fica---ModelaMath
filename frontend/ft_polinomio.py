import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
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
        self.configure(fg_color="#121212")

        ctk.CTkLabel(self, text="📊 Análisis de Polinomios",font=("Segoe UI", 26, "bold"),text_color="#6c63ff").pack(pady=20)
 
        self.coef_entries = []
        self.grado_var = ctk.StringVar(value="2")

        config_frame = ctk.CTkFrame(self)
        config_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(config_frame, text="Grado:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkOptionMenu(config_frame, values=["1", "2"], variable=self.grado_var).grid(row=0, column=1)

        ctk.CTkButton(config_frame, text="Generar Coeficientes", command=self.generar_campos).grid(row=0, column=2, padx=20)

        self.tipo_label = ctk.CTkLabel(config_frame, text="Tipo: Cuadrático", font=("Arial", 14))
        self.tipo_label.grid(row=0, column=3, padx=10)

        self.frame_coef = ctk.CTkFrame(self, fg_color="#1c1c1c")
        self.frame_coef.pack(pady=10)

        eval_frame = ctk.CTkFrame(self)
        eval_frame.pack(pady=10)

        ctk.CTkLabel(eval_frame, text="Evaluar en x =", font=("Arial", 14)).pack(side="left", padx=10)
        self.eval_x = ctk.CTkEntry(eval_frame, width=80)
        self.eval_x.pack(side="left", padx=5)

        ctk.CTkButton(eval_frame, text="Evaluar", width=120, command=self.evaluar).pack(side="left", padx=10)

        acciones_frame = ctk.CTkFrame(self)
        acciones_frame.pack(pady=5)

        ctk.CTkButton(acciones_frame, text="Derivar", width=120, command=self.derivar).pack(side="left", padx=10)
        ctk.CTkButton(acciones_frame, text="Integrar", width=120, command=self.integrar).pack(side="left", padx=10)

        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.pack(pady=15, padx=10, fill="both", expand=True)
        self.canvas = None

        self.generar_campos()

    def generar_campos(self):
        for widget in self.frame_coef.winfo_children():
            widget.destroy()
        self.coef_entries.clear()

        try:
            grado = int(self.grado_var.get())
        except:
            CTkMessagebox(title="Error", message="Grado inválido", icon="cancel")
            return

        self.tipo_label.configure(text="Tipo: " + ("Lineal" if grado == 1 else "Cuadrático"))

        ctk.CTkLabel(self.frame_coef, text="Coeficientes:", font=("Arial", 14)).pack(side="left", padx=10)

        coefs = generar_coeficientes(grado)
        for coef in coefs:
            entry = ctk.CTkEntry(self.frame_coef, width=60)
            entry.pack(side="left", padx=5)
            entry.insert(0, str(coef))
            self.coef_entries.append(entry)

    def leer_coeficientes(self) -> list[float] | None:
        try:
            return [float(entry.get()) for entry in self.coef_entries]
        except:
            CTkMessagebox(title="Error", message="Asegúrate de ingresar números válidos", icon="cancel")
            return None

    def evaluar(self):
        coefs = self.leer_coeficientes()
        if coefs is None:
            return
        try:
            x_val = float(self.eval_x.get())
            resultado = evaluar_polinomio(coefs, x_val)
            CTkMessagebox(title="Evaluación", message=f"f({x_val}) = {resultado:.4f}", icon="check")
            self.graficar_polinomio(coefs)
        except:
            CTkMessagebox(title="Error", message="Ingresa un valor válido para x", icon="cancel")

    def derivar(self):
        coefs = self.leer_coeficientes()
        if coefs is None:
            return
        derivada = derivar_polinomio(coefs)
        CTkMessagebox(title="Derivada", message=formatear_polinomio(derivada), icon="info")
        self.graficar_polinomio(derivada)

    def integrar(self):
        coefs = self.leer_coeficientes()
        if coefs is None:
            return
        integral = integrar_polinomio(coefs)
        CTkMessagebox(title="Integral", message=formatear_polinomio(integral), icon="info")
        self.graficar_polinomio(integral)

    def graficar_polinomio(self, coefs: list[float]):
        x = np.linspace(-10, 10, 400)
        y = np.polyval(coefs, x)

        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(x, y, label='f(x)')
        ax.axhline(0, linestyle='--')
        ax.axvline(0, linestyle='--')
        ax.grid(True, linestyle=':')
        ax.set_title("Gráfica del Polinomio")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas = canvas