import customtkinter as ctk
from PIL import Image

class AcercaDePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#0f1419")
        
        # Crear scrollable frame principal
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            scrollbar_fg_color="#1a1f26",
            scrollbar_button_color="#6c63ff"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._create_hero_section()
        self._create_project_info()
        self._create_tech_stack()
        self._create_features_section()
        self._create_footer()
    
    def _create_hero_section(self):
        """Crear sección principal con logo y título"""
        hero_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="#161b22",
            corner_radius=20,
            height=300
        )
        hero_frame.pack(fill="x", pady=(0, 30))
        
        # Contenedor centrado
        center_container = ctk.CTkFrame(hero_frame, fg_color="transparent")
        center_container.pack(expand=True, fill="both", pady=30)
        
        # Logo con efecto premium
        logo_container = ctk.CTkFrame(
            center_container,
            fg_color="#6c63ff",
            corner_radius=40,
            width=100,
            height=100
        )
        logo_container.pack(pady=(10, 20))
        logo_container.pack_propagate(False)
        
        try:
            logo = ctk.CTkImage(Image.open("assets/logo2.png"), size=(70, 70))
            ctk.CTkLabel(logo_container, image=logo, text="").pack(expand=True)
        except:
            ctk.CTkLabel(
                logo_container, 
                text="🧠", 
                font=("Arial", 35), 
                text_color="white"
            ).pack(expand=True)
        
        # Título principal
        ctk.CTkLabel(
            center_container,
            text="ModelaMath",
            font=("Segoe UI", 38, "bold"),
            text_color="#ffffff"
        ).pack(pady=(0, 8))
        
        # Subtítulo elegante
        ctk.CTkLabel(
            center_container,
            text="Calculadora Científica Avanzada",
            font=("Segoe UI", 18, "bold"),
            text_color="#6c63ff"
        ).pack(pady=(0, 8))
        
        # Descripción
        ctk.CTkLabel(
            center_container,
            text="Proyecto Académico • Modelos Matemáticos y Simulación",
            font=("Segoe UI", 14),
            text_color="#8b949e"
        ).pack()
    
    def _create_project_info(self):
        """Crear sección de información del proyecto"""
        # Título de sección
        section_title = ctk.CTkLabel(
            self.scroll_frame,
            text="📋 Información del Proyecto",
            font=("Segoe UI", 24, "bold"),
            text_color="#ffffff"
        )
        section_title.pack(pady=(0, 20), anchor="w")
        
        # Contenedor principal de información
        info_container = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="#1a1f26",
            corner_radius=16
        )
        info_container.pack(fill="x", pady=(0, 30))
        
        # Grid de información
        grid_frame = ctk.CTkFrame(info_container, fg_color="transparent")
        grid_frame.pack(fill="x", padx=30, pady=25)
        
        # Información del estudiante y proyecto
        student_info = [
            ("👨‍🎓", "Autor", "Victor Alejandro Celi Rivadeneira", "#ff6b6b"),
            ("🎓", "Carrera", "Ingeniería en Software", "#4ecdc4"),
            ("📆", "Semestre", "6to Semestre C1", "#45b7d1"),
            ("👨‍🏫", "Docente", "Isidro Fabricio Morales Torres", "#96ceb4"),
            ("📚", "Materia", "Modelos Matemáticos y Simulación", "#ffa726"),
            ("📦", "Año", "2025", "#ab47bc")
        ]
        
        for i, (icon, label, value, color) in enumerate(student_info):
            row = i // 2
            col = i % 2
            
            card = self._create_info_card(grid_frame, icon, label, value, color)
            card.grid(row=row, column=col, padx=15, pady=10, sticky="ew")
        
        # Configurar grid
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
    
    def _create_info_card(self, parent, icon, label, value, color):
        """Crear tarjeta de información individual"""
        card = ctk.CTkFrame(
            parent,
            fg_color="#252a32",
            corner_radius=12,
            height=80
        )
        
        # Contenido de la tarjeta
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Icono
        icon_frame = ctk.CTkFrame(
            content_frame,
            fg_color=color,
            corner_radius=6,
            width=35,
            height=35
        )
        icon_frame.pack(side="left", padx=(0, 15))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text=icon,
            font=("Arial", 16),
            text_color="white"
        ).pack(expand=True)
        
        # Contenido textual
        text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True)
        
        # Label
        ctk.CTkLabel(
            text_frame,
            text=label,
            font=("Segoe UI", 11, "bold"),
            text_color="#8b949e",
            anchor="w"
        ).pack(fill="x")
        
        # Value
        ctk.CTkLabel(
            text_frame,
            text=value,
            font=("Segoe UI", 13, "bold"),
            text_color="#ffffff",
            anchor="w"
        ).pack(fill="x")
        
        return card
    
    def _create_tech_stack(self):
        """Crear sección de tecnologías utilizadas"""
        # Título
        tech_title = ctk.CTkLabel(
            self.scroll_frame,
            text="🛠️ Stack Tecnológico",
            font=("Segoe UI", 24, "bold"),
            text_color="#ffffff"
        )
        tech_title.pack(pady=(0, 20), anchor="w")
        
        # Contenedor de tecnologías
        tech_container = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="#161b22",
            corner_radius=16
        )
        tech_container.pack(fill="x", pady=(0, 30))
        
        # Lista de tecnologías
        technologies = [
            ("🐍", "Python", "Lenguaje de programación principal"),
            ("🖼️", "CustomTkinter", "Framework para interfaz gráfica moderna"),
            ("🧮", "SymPy", "Biblioteca para matemáticas simbólicas"),
            ("🔢", "NumPy", "Computación numérica y arrays"),
            ("📊", "Matplotlib", "Visualización de gráficas 2D y 3D"),
            ("🖼️", "Pillow (PIL)", "Procesamiento de imágenes")
        ]
        
        tech_grid = ctk.CTkFrame(tech_container, fg_color="transparent")
        tech_grid.pack(fill="x", padx=30, pady=25)
        
        for i, (icon, name, desc) in enumerate(technologies):
            tech_row = ctk.CTkFrame(tech_grid, fg_color="#1a1f26", corner_radius=8)
            tech_row.pack(fill="x", pady=5)
            
            content = ctk.CTkFrame(tech_row, fg_color="transparent")
            content.pack(fill="x", padx=20, pady=12)
            
            # Icono
            ctk.CTkLabel(
                content,
                text=icon,
                font=("Arial", 20),
                width=40
            ).pack(side="left", padx=(0, 15))
            
            # Información
            info_frame = ctk.CTkFrame(content, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(
                info_frame,
                text=name,
                font=("Segoe UI", 14, "bold"),
                text_color="#ffffff",
                anchor="w"
            ).pack(fill="x")
            
            ctk.CTkLabel(
                info_frame,
                text=desc,
                font=("Segoe UI", 12),
                text_color="#8b949e",
                anchor="w"
            ).pack(fill="x")
        
    def _create_features_section(self):
        """Crear sección de características del proyecto"""
        features_title = ctk.CTkLabel(
            self.scroll_frame,
            text="✨ Características Principales",
            font=("Segoe UI", 24, "bold"),
            text_color="#ffffff"
        )
        features_title.pack(pady=(0, 20), anchor="w")
        
        # Contenedor de características
        features_container = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="#1a1f26",
            corner_radius=16
        )
        features_container.pack(fill="x", pady=(0, 30))
        
        # Descripción del proyecto
        desc_frame = ctk.CTkFrame(features_container, fg_color="transparent")
        desc_frame.pack(fill="x", padx=30, pady=25)
        
        ctk.CTkLabel(
            desc_frame,
            text="Aplicación integral diseñada para resolver operaciones matemáticas complejas "
                 "con una interfaz moderna e intuitiva. Combina cálculo simbólico, álgebra lineal "
                 "y visualización gráfica en una sola herramienta.",
            font=("Segoe UI", 14),
            text_color="#c9d1d9",
            wraplength=600,
            justify="left"
        ).pack(pady=(0, 20))
        
        # Lista de funcionalidades
        features = [
            "🔢 Operaciones con matrices y vectores",
            "∫ Cálculo de derivadas e integrales simbólicas",
            "📊 Visualización de funciones en 2D y 3D",
            "📈 Análisis y manipulación de polinomios",
            "🎯 Resolución de sistemas de ecuaciones lineales",
            "🖥️ Interfaz gráfica moderna y responsive"
        ]
        
        for feature in features:
            feature_row = ctk.CTkFrame(desc_frame, fg_color="#252a32", corner_radius=8)
            feature_row.pack(fill="x", pady=3)
            
            ctk.CTkLabel(
                feature_row,
                text=feature,
                font=("Segoe UI", 13),
                text_color="#e0e0e0",
                anchor="w"
            ).pack(fill="x", padx=20, pady=10)
    
    def _create_footer(self):
        """Crear pie de página"""
        footer_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="#6c63ff",
            corner_radius=18,
            height=80
        )
        footer_frame.pack(fill="x")
        
        # Contenido del footer
        footer_content = ctk.CTkFrame(footer_frame, fg_color="transparent")
        footer_content.pack(expand=True, fill="both")
        
        ctk.CTkLabel(
            footer_content,
            text="© 2025 ModelaMath",
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        ).pack(expand=True)
        
        ctk.CTkLabel(
            footer_content,
            text="Desarrollado con 💜 para la comunidad académica",
            font=("Segoe UI", 12),
            text_color="#e8e3ff"
        ).pack()