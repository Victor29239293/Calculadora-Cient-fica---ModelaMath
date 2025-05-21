import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import StringVar, DoubleVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from backend.bk_grafica3D import generar_malla ,evaluar_funcion_3d 
class Graficas3DPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#1a1c1e")

        ctk.CTkLabel(
            self,
            text="🌐 Visualizador de Funciones 3D",
            font=("Segoe UI", 26, "bold"),
            text_color="#6c63ff"
        ).pack(pady=15)

        # Input de función y rangos
        input_frame = ctk.CTkFrame(self, fg_color="#23272a", corner_radius=10)
        input_frame.pack(pady=10)
        self.entrada_funcion = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ejemplo: sin(x)*cos(y)",
            width=450
        )
        self.entrada_funcion.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.x_min = ctk.CTkEntry(input_frame, placeholder_text="X mín", width=120)
        self.x_max = ctk.CTkEntry(input_frame, placeholder_text="X máx", width=120)
        self.y_min = ctk.CTkEntry(input_frame, placeholder_text="Y mín", width=120)
        self.y_max = ctk.CTkEntry(input_frame, placeholder_text="Y máx", width=120)
        self.x_min.grid(row=1, column=0, padx=8, pady=5)
        self.x_max.grid(row=1, column=1, padx=8, pady=5)
        self.y_min.grid(row=2, column=0, padx=8, pady=5)
        self.y_max.grid(row=2, column=1, padx=8, pady=5)

        # Opciones avanzadas
        opciones_frame = ctk.CTkFrame(self, fg_color="#23272a", corner_radius=10)
        opciones_frame.pack(pady=10, fill="x", padx=20)
        # Colormap
        ctk.CTkLabel(opciones_frame, text="Colormap:").grid(row=0, column=0, padx=5)
        self.cmap_var = StringVar(value="plasma")
        ctk.CTkOptionMenu(
            opciones_frame,
            values=["plasma", "viridis", "coolwarm", "magma", "cividis"],
            variable=self.cmap_var
        ).grid(row=0, column=1, padx=5)
        # Resolución
        ctk.CTkLabel(opciones_frame, text="Resolución:").grid(row=0, column=2, padx=5)
        self.resol_var = DoubleVar(value=150)
        ctk.CTkSlider(
            opciones_frame,
            from_=50,
            to=300,
            number_of_steps=10,
            variable=self.resol_var,
            width=150
        ).grid(row=0, column=3, padx=5)
        # Ángulos
        ctk.CTkLabel(opciones_frame, text="Elevación:").grid(row=1, column=0, padx=5, pady=5)
        self.elev_var = DoubleVar(value=35)
        ctk.CTkSlider(
            opciones_frame,
            from_=-90,
            to=90,
            variable=self.elev_var,
            width=150
        ).grid(row=1, column=1, padx=5)
        ctk.CTkLabel(opciones_frame, text="Azimut:").grid(row=1, column=2, padx=5)
        self.azim_var = DoubleVar(value=135)
        ctk.CTkSlider(
            opciones_frame,
            from_=-180,
            to=180,
            variable=self.azim_var,
            width=150
        ).grid(row=1, column=3, padx=5)

        ctk.CTkButton(
            self,
            text="📈 Graficar función",
            command=self.graficar_3d,
            height=42,
            width=220,
            font=("Segoe UI", 14),
            fg_color="#6c63ff",
            hover_color="#7d74ff"
        ).pack(pady=15)

        # Frame para la gráfica
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

    def graficar_3d(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        try:
            x0, x1 = float(self.x_min.get()), float(self.x_max.get())
            y0, y1 = float(self.y_min.get()), float(self.y_max.get())
            num = int(self.resol_var.get())
            cmap = self.cmap_var.get()
            elev = float(self.elev_var.get())
            azim = float(self.azim_var.get())
            X, Y = generar_malla(x0, x1, y0, y1, num)
            Z = evaluar_funcion_3d(self.entrada_funcion.get(), X, Y)
        except Exception as e:
            CTkMessagebox(title="❌ Error", message=str(e), icon="cancel")
            return

        fig = plt.figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        superficie = ax.plot_surface(X, Y, Z, cmap=cmap, edgecolor='k', linewidth=0.2)
        ax.set_title(f"f(x, y) = {self.entrada_funcion.get()}", fontsize=14)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.view_init(elev=elev, azim=azim)
        fig.colorbar(superficie, ax=ax, shrink=0.6, aspect=12, pad=0.05)
        fig.tight_layout()
        fig.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.grid(row=0, column=0, sticky="nsew")
