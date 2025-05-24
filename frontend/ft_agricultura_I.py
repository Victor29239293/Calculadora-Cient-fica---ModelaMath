import json
from tkinter import filedialog
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os
import numpy as np
from backend.bk_agricultura_I import simulate_soil_moisture

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwin = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)
        
    def show(self, _):
        if self.tipwin or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, "bbox") else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tipwin = tw = ctk.CTkToplevel(self.widget)
        tw.wm_attributes("-topmost", True)
        tw.wm_overrideredirect(True)
        
        label = ctk.CTkLabel(
            tw, 
            text=self.text, 
            fg_color="#1E2030", 
            corner_radius=8,
            text_color="#E0E0E0",
            padx=10, 
            pady=6
        )
        label.pack()
        
        tw.geometry(f"+{x}+{y}")
        
    def hide(self, _):
        if self.tipwin:
            self.tipwin.destroy()
            self.tipwin = None

class AgriculturaApp(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.simulation_data = None
        
        self.create_ui()
        
    def create_ui(self):
  
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        

        self.sidebar = ctk.CTkFrame(self, fg_color="#1A1C2C", corner_radius=15)
        self.sidebar.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")
        

        self.main_panel = ctk.CTkFrame(self, fg_color="#1E2030", corner_radius=15)
        self.main_panel.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        
        self.setup_sidebar()
        

        self.setup_main_panel()
        
    def setup_sidebar(self):
        header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))
        
        title = ctk.CTkLabel(
            header, 
            text="Parámetros de Simulación",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#8AADF4"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header, 
            text="Configure los valores para la simulación de riego",
            text_color="#A5ADCB",
            font=ctk.CTkFont(size=12)
        )
        subtitle.pack(anchor="w", pady=(0, 10))
        
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="#364A82")
        separator.pack(fill="x", padx=15, pady=5)
        
        param_container = ctk.CTkScrollableFrame(
            self.sidebar, 
            fg_color="transparent",
            scrollbar_fg_color="#1E2030",
            scrollbar_button_color="#5BABDC",
            scrollbar_button_hover_color="#7DC4F7"
        )
        param_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        labels = [
            ("Capacidad de campo", "Capacidad máxima de humedad del suelo (0–1)"),
            ("Punto de marchitez", "Humedad mínima antes de marchitarse (0–1)"),
            ("Umbral riego", "Nivel de humedad para activar riego (0–1)"),
            ("Tasa riego (mm/h)", "Caudal de riego cuando se activa"),
            ("ET (mm/h)", "Evapotranspiración estimada"),
            ("Humedad inicial", "Humedad al inicio de simulación (0–1)"),
            ("Simulación (h)", "Duración total en horas"),
            ("Paso dt (h)", "Paso de tiempo en horas"),
        ]
        
        defaults = [0.4, 0.1, 0.2, 5, 1, 0.3, 48, 0.5]
        
        self.entries = {}
        for i, ((lbl, tip), val) in enumerate(zip(labels, defaults)):
            frame = ctk.CTkFrame(param_container, fg_color="#242842", corner_radius=10)
            frame.pack(fill="x", pady=8, padx=5)
            
            label = ctk.CTkLabel(
                frame, 
                text=lbl, 
                text_color="#CAD3F5", 
                width=150,
                font=ctk.CTkFont(size=13)
            )
            label.pack(side="top", anchor="w", padx=12, pady=(10, 5))
            
            entry = ctk.CTkEntry(
                frame, 
                width=140, 
                fg_color="#181926", 
                border_color="#5BABDC",
                text_color="#F4DBD6",
                placeholder_text=f"Valor ({val})"
            )
            entry.pack(side="top", padx=12, pady=(0, 10), fill="x")
            entry.insert(0, str(val))
            self.entries[lbl] = entry
            
            ToolTip(frame, tip)
        
        actions_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        actions_frame.pack(fill="x", padx=15, pady=15)
        
        btn_simular = ctk.CTkButton(
            actions_frame, 
            text="Ejecutar Simulación", 
            command=self.on_simular,
            fg_color="#8839EF",
            hover_color="#A270FF",
            text_color="#FFFFFF",
            font=ctk.CTkFont(weight="bold"),
            height=40,
            corner_radius=10
        )
        btn_simular.pack(fill="x", pady=(0, 10))
        
        buttons_row = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_row.pack(fill="x")
        buttons_row.grid_columnconfigure(0, weight=1)
        buttons_row.grid_columnconfigure(1, weight=1)
        
        btn_cargar = ctk.CTkButton(
            buttons_row, 
            text="Cargar", 
            command=self.load_params,
            fg_color="#5BABDC",
            hover_color="#7DC4F7",
            height=32,
            corner_radius=8
        )
        btn_cargar.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        btn_guardar = ctk.CTkButton(
            buttons_row, 
            text="Guardar", 
            command=self.save_params,
            fg_color="#5BABDC",
            hover_color="#7DC4F7",
            height=32,
            corner_radius=8
        )
        btn_guardar.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
    def setup_main_panel(self):

        self.main_panel.grid_rowconfigure(0, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)
        
        self.tabs = ctk.CTkTabview(
            self.main_panel, 
            fg_color="#242842", 
            segmented_button_fg_color="#1A1C2C",
            segmented_button_selected_color="#8839EF",
            segmented_button_unselected_color="#1A1C2C",
            segmented_button_selected_hover_color="#A270FF",
            text_color="#CAD3F5",
            corner_radius=10
        )
        self.tabs.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
  
        self.tab_graph = self.tabs.add("Gráfico de Simulación")
        self.tabs.set("Gráfico de Simulación")  # Pestaña activa por defecto
        
        self.tab_balance = self.tabs.add("Balance Hídrico")
        
        self.tab_summary = self.tabs.add("Resumen")
        
        self.setup_graph_tab()
        self.setup_balance_tab()
        self.setup_summary_tab()
        
    def setup_graph_tab(self):
        self.graph_frame = ctk.CTkFrame(self.tab_graph, fg_color="#181926", corner_radius=10)
        self.graph_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.placeholder_label = ctk.CTkLabel(
            self.graph_frame,
            text="Ejecute una simulación para visualizar\nresultados gráficos",
            font=ctk.CTkFont(size=16),
            text_color="#A5ADCB"
        )
        self.placeholder_label.pack(fill="both", expand=True)
        
        self.canvas = None
        
    def setup_balance_tab(self):
        balance_container = ctk.CTkFrame(self.tab_balance, fg_color="transparent")
        balance_container.pack(fill="both", expand=True, padx=15, pady=15)
  
        header = ctk.CTkFrame(balance_container, fg_color="#242842", corner_radius=10, height=50)
        header.pack(fill="x", pady=(0, 10))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, 
            text="Balance Hídrico Acumulado (mm)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#8AADF4"
        ).pack(side="left", padx=15)
        
        self.balance_frame = ctk.CTkScrollableFrame(
            balance_container,
            fg_color="#181926",
            corner_radius=10,
            scrollbar_fg_color="#242842",
            scrollbar_button_color="#5BABDC",
            scrollbar_button_hover_color="#7DC4F7"
        )
        self.balance_frame.pack(fill="both", expand=True)
        
        self.balance_text = ctk.CTkTextbox(
            self.balance_frame, 
            fg_color="#181926", 
            text_color="#CAD3F5",
            font=ctk.CTkFont(family="Consolas", size=13),
            activate_scrollbars=False,
            corner_radius=0
        )
        self.balance_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def setup_summary_tab(self):

        summary_container = ctk.CTkFrame(self.tab_summary, fg_color="transparent")
        summary_container.pack(fill="both", expand=True, padx=15, pady=15)

        # Cambia CTkFrame por CTkScrollableFrame aquí:
        self.summary_frame = ctk.CTkScrollableFrame(summary_container, fg_color="#181926", corner_radius=10)
        self.summary_frame.pack(fill="both", expand=True)

        self.summary_placeholder = ctk.CTkLabel(
            self.summary_frame,
            text="Ejecute una simulación para generar un resumen",
            font=ctk.CTkFont(size=16),
            text_color="#A5ADCB"
        )
        self.summary_placeholder.pack(fill="both", expand=True)

        self.summary_content = ctk.CTkFrame(self.summary_frame, fg_color="#181926")
        
        
    def load_params(self):
        path = filedialog.askopenfilename(
            title="Cargar parámetros de simulación",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        if not path:
            return
            
        try:
            with open(path) as f:
                data = json.load(f)
                
            for lbl, e in self.entries.items():
                if lbl in data:
                    e.delete(0, "end")
                    e.insert(0, str(data[lbl]))
                    
            CTkMessagebox(
                title="Cargado correctamente", 
                message="Parámetros cargados desde:\n" + os.path.basename(path), 
                icon="check",
                option_1="Aceptar"
            )
        except Exception as e:
            CTkMessagebox(
                title="Error al cargar", 
                message=f"No se pudieron cargar los parámetros:\n{str(e)}", 
                icon="cancel",
                option_1="Aceptar"
            )

    def save_params(self):
        path = filedialog.asksaveasfilename(
            title="Guardar parámetros de simulación",
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        if not path:
            return
            
        try:
            data = {lbl: float(e.get()) for lbl, e in self.entries.items()}
            
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
                
            CTkMessagebox(
                title="Guardado correctamente", 
                message="Parámetros guardados en:\n" + os.path.basename(path), 
                icon="check",
                option_1="Aceptar"
            )
        except Exception as e:
            CTkMessagebox(
                title="Error al guardar", 
                message=f"No se pudieron guardar los parámetros:\n{str(e)}", 
                icon="cancel",
                option_1="Aceptar"
            )

    def on_simular(self):
        try:
            vals = {lbl: float(e.get()) for lbl, e in self.entries.items()}

            self.simulation_data = simulate_soil_moisture(
                field_capacity=vals["Capacidad de campo"],
                wilting_point=vals["Punto de marchitez"],
                threshold=vals["Umbral riego"],
                irrigation_rate=vals["Tasa riego (mm/h)"],
                et_rate=vals["ET (mm/h)"],
                theta0=vals["Humedad inicial"],
                t_end=vals["Simulación (h)"],
                dt=vals["Paso dt (h)"],
            )

            self._plot_graph()
            self._show_balance()
            self._update_summary()

            self.tabs.set("Gráfico de Simulación")
            
        except Exception as e:
            CTkMessagebox(
                title="Error en la simulación", 
                message=f"No se pudo ejecutar la simulación:\n{str(e)}", 
                icon="cancel",
                option_1="Aceptar"
            )

    def _plot_graph(self):

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            
        self.placeholder_label.pack_forget()
        
        plt.style.use('dark_background')
        fig = Figure(figsize=(8, 5), dpi=100, facecolor="#181926")
        ax = fig.add_subplot(111)

        data = self.simulation_data

        ax.plot(data['t'], data['theta'], 
                linewidth=2.5, 
                color='#8AADF4', 
                label='Humedad del suelo')
                
        irrigation_times = data['t'][data['events']]
        irrigation_values = data['theta'][data['events']]
        
        if len(irrigation_times) > 0:
            ax.scatter(irrigation_times, irrigation_values,
                      color='#F5A97F', 
                      marker='s', 
                      s=80,
                      edgecolor='white',
                      linewidth=1,
                      label='Evento de riego',
                      zorder=5)
                      
        field_capacity = float(self.entries["Capacidad de campo"].get())
        wilting_point = float(self.entries["Punto de marchitez"].get())
        threshold = float(self.entries["Umbral riego"].get())
        
        ax.axhline(y=field_capacity, color='#A6DA95', linestyle='--', alpha=0.8, label='Capacidad de campo')
        ax.axhline(y=wilting_point, color='#ED8796', linestyle='--', alpha=0.8, label='Punto de marchitez')
        ax.axhline(y=threshold, color='#EED49F', linestyle=':', alpha=0.8, label='Umbral de riego')
 
        ax.set_xlabel("Tiempo (horas)", fontsize=12, color='#CAD3F5')
        ax.set_ylabel("Contenido de humedad (θ)", fontsize=12, color='#CAD3F5')
        ax.set_ylim(0, max(1.0, field_capacity * 1.2))
        ax.set_xlim(0, data['t'][-1])

        ax.grid(True, linestyle=':', alpha=0.3, color='#A5ADCB')
        ax.tick_params(colors='#CAD3F5', which='both')
        for spine in ax.spines.values():
            spine.set_color('#364A82')
            

        ax.set_title("Simulación de Humedad del Suelo y Eventos de Riego", 
                    fontsize=14, color='#8AADF4', pad=10)
                    
        legend = ax.legend(loc='upper right', frameon=True, fancybox=True, 
                          framealpha=0.7, edgecolor='#364A82', fontsize=10)
        legend.get_frame().set_facecolor('#242842')
        for text in legend.get_texts():
            text.set_color('#CAD3F5')
            
        fig.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def _show_balance(self):

        self.balance_text.delete("0.0", "end")
        
        if not self.simulation_data:
            self.balance_text.insert("end", "No hay datos de simulación disponibles.")
            return
        
        self.balance_text.insert("end", "Tiempo (h)".ljust(15))
        self.balance_text.insert("end", "Balance (mm)".ljust(15))
        self.balance_text.insert("end", "Estado\n")
        self.balance_text.insert("end", "─" * 45 + "\n")
        
        data = self.simulation_data
        for i, (ti, b) in enumerate(zip(data['t'], data['balance'])):
            if i % max(1, len(data['t']) // 100) == 0 or i == len(data['t']) - 1:
                self.balance_text.insert("end", f"{ti:.1f}".ljust(15))
                self.balance_text.insert("end", f"{b:.2f}".ljust(15))
                if b > 0:
                    self.balance_text.insert("end", "Excedente\n")
                elif b < 0:
                    self.balance_text.insert("end", "Déficit\n")
                else:
                    self.balance_text.insert("end", "Equilibrio\n")

    def _update_summary(self):
        self.summary_placeholder.pack_forget()
        
        for widget in self.summary_content.winfo_children():
            widget.destroy()
            
        self.summary_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        data = self.simulation_data
        if not data:
            return

        field_capacity = float(self.entries["Capacidad de campo"].get())
        wilting_point = float(self.entries["Punto de marchitez"].get())

        irrigation_events = np.sum(data['events'])

        event_indices = np.where(data['events'])[0]
        if len(event_indices) > 1:
            event_times = data['t'][event_indices]
            avg_time_between = np.mean(np.diff(event_times))
        else:
            avg_time_between = 0
            
        avg_moisture = np.mean(data['theta'])
        

        threshold = float(self.entries["Umbral riego"].get())
        optimal_time = np.sum((data['theta'] >= threshold) & (data['theta'] <= field_capacity)) * float(self.entries["Paso dt (h)"].get())
        total_time = float(self.entries["Simulación (h)"].get())
        optimal_percent = (optimal_time / total_time) * 100 if total_time > 0 else 0
       
        irrigation_rate = float(self.entries["Tasa riego (mm/h)"].get())
        water_usage = irrigation_events * irrigation_rate * float(self.entries["Paso dt (h)"].get())
        
        final_balance = data['balance'][-1]
        
        title_frame = ctk.CTkFrame(self.summary_content, fg_color="#242842", corner_radius=10)
        title_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            title_frame,
            text="Resumen de Simulación",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#8AADF4"
        ).pack(pady=10)
        

        stats_grid = ctk.CTkFrame(self.summary_content, fg_color="transparent")
        stats_grid.pack(fill="both", expand=True)
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)
        

        def create_stat_card(parent, title, value, unit, row, col, text_color="#CAD3F5", value_color="#F5A97F"):
            card = ctk.CTkFrame(parent, fg_color="#242842", corner_radius=10)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=13),
                text_color=text_color
            ).pack(pady=(10, 5))
            
            ctk.CTkLabel(
                card,
                text=f"{value}",
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color=value_color
            ).pack(pady=5)
            
            ctk.CTkLabel(
                card,
                text=unit,
                font=ctk.CTkFont(size=12),
                text_color=text_color
            ).pack(pady=(0, 10))
            

        create_stat_card(stats_grid, "Eventos de Riego", irrigation_events, "eventos", 0, 0)
        create_stat_card(stats_grid, "Tiempo entre Riegos", f"{avg_time_between:.1f}", "horas", 0, 1)
        create_stat_card(stats_grid, "Humedad Promedio", f"{avg_moisture:.2f}", "θ", 1, 0)
        create_stat_card(stats_grid, "Tiempo en Condiciones Óptimas", f"{optimal_percent:.1f}", "% del tiempo", 1, 1)
        create_stat_card(stats_grid, "Consumo de Agua", f"{water_usage:.1f}", "mm", 2, 0)

        balance_color = "#A6DA95" if final_balance >= 0 else "#ED8796"
        create_stat_card(stats_grid, "Balance Hídrico Final", f"{final_balance:.2f}", "mm", 2, 1, 
                         value_color=balance_color)

