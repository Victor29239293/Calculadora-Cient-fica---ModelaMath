import customtkinter as ctk
from PIL import Image

class MenuPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#0f1419")  # Fondo más oscuro y moderno
        
        # Crear scrollable frame principal
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            scrollbar_fg_color="#1a1f26",
            scrollbar_button_color="#6c63ff"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._create_header()
        self._create_feature_cards()
        self._create_info_section()
        self._create_footer()
    
    def _create_header(self):
        """Crear sección del encabezado con logo y título"""
        header_frame = ctk.CTkFrame(
            self.scroll_frame, 
            fg_color="transparent",
            height=200
        )
        header_frame.pack(fill="x", pady=(0, 40))
        
        # Contenedor centrado para logo y texto
        center_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        center_container.pack(expand=True, fill="both")
        
        # Logo con efecto de sombra
        logo_container = ctk.CTkFrame(
            center_container, 
            fg_color="#1a1f26",
            corner_radius=50,
            width=120,
            height=120
        )
        logo_container.pack(pady=(20, 15))
        logo_container.pack_propagate(False)
        
        try:
            logo_img = ctk.CTkImage(Image.open("assets/logo2.png"), size=(80, 80))
            ctk.CTkLabel(logo_container, image=logo_img, text="").pack(expand=True)
        except:
            ctk.CTkLabel(
                logo_container, 
                text="🧠", 
                font=("Arial", 40), 
                text_color="#6c63ff"
            ).pack(expand=True)
        
        # Título con gradiente simulado
        titulo = ctk.CTkLabel(
            center_container,
            text="ModelaMath",
            font=("Segoe UI", 42, "bold"),
            text_color="#ffffff"
        )
        titulo.pack(pady=(0, 8))
        
        # Subtítulo elegante
        subtitulo = ctk.CTkLabel(
            center_container,
            text="Herramientas matemáticas avanzadas al alcance de todos",
            font=("Segoe UI", 16),
            text_color="#8b949e"
        )
        subtitulo.pack(pady=(0, 10))
        
        # Línea decorativa
        linea = ctk.CTkFrame(
            center_container,
            height=2,
            width=200,
            fg_color="#6c63ff"
        )
        linea.pack(pady=10)
    
    def _create_feature_cards(self):
        """Crear tarjetas de características principales"""
        features_title = ctk.CTkLabel(
            self.scroll_frame,
            text="🚀 Módulos Disponibles",
            font=("Segoe UI", 24, "bold"),
            text_color="#ffffff"
        )
        features_title.pack(pady=(0, 20), anchor="w")
        
        # Grid de características
        grid_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        grid_frame.pack(fill="x", pady=(0, 30))
        
        features = [
            {
                "icon": "🔢",
                "title": "Álgebra Lineal",
                "desc": "Operaciones con matrices y vectores, sistemas de ecuaciones lineales",
                "color": "#ff6b6b"
            },
            {
                "icon": "∫",
                "title": "Cálculo Simbólico", 
                "desc": "Derivadas, integrales y manipulación de expresiones matemáticas",
                "color": "#4ecdc4"
            },
            {
                "icon": "📊",
                "title": "Visualización",
                "desc": "Gráficas interactivas en 2D y 3D para funciones y datos",
                "color": "#45b7d1"
            },
            {
                "icon": "📈",
                "title": "Polinomios",
                "desc": "Análisis, factorización y visualización de funciones polinómicas",
                "color": "#96ceb4"
            }
        ]
        
        # Crear tarjetas en grid 2x2
        for i, feature in enumerate(features):
            row = i // 2
            col = i % 2
            
            card = self._create_feature_card(grid_frame, feature)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        # Configurar grid
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
    
    def _create_feature_card(self, parent, feature_data):
        """Crear una tarjeta individual de característica"""
        card = ctk.CTkFrame(
            parent,
            fg_color="#1a1f26",
            corner_radius=12,
            height=140
        )
        
        # Hover effect simulation
        def on_enter(event):
            card.configure(fg_color="#252a32")
        
        def on_leave(event):
            card.configure(fg_color="#1a1f26")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        # Contenido de la tarjeta
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Icono con color
        icon_frame = ctk.CTkFrame(
            content_frame,
            fg_color=feature_data["color"],
            corner_radius=8,
            width=40,
            height=40
        )
        icon_frame.pack(anchor="w", pady=(0, 10))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text=feature_data["icon"],
            font=("Arial", 20),
            text_color="white"
        ).pack(expand=True)
        
        # Título
        ctk.CTkLabel(
            content_frame,
            text=feature_data["title"],
            font=("Segoe UI", 16, "bold"),
            text_color="#ffffff",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        # Descripción
        ctk.CTkLabel(
            content_frame,
            text=feature_data["desc"],
            font=("Segoe UI", 12),
            text_color="#8b949e",
            anchor="w",
            wraplength=200,
            justify="left"
        ).pack(fill="x")
        
        return card
    
    def _create_info_section(self):
        """Crear sección informativa"""
        info_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="#161b22",
            corner_radius=16
        )
        info_frame.pack(fill="x", pady=(20, 30))
        
        # Título de la sección
        ctk.CTkLabel(
            info_frame,
            text="💡 Guía de Uso",
            font=("Segoe UI", 20, "bold"),
            text_color="#ffffff"
        ).pack(pady=(25, 15), anchor="w", padx=30)
        
        # Tips de uso
        tips = [
            "Navega por el menú lateral para acceder a cada módulo específico",
            "Ingresa datos numéricos válidos para obtener resultados precisos",
            "Usa el modo pantalla completa para una mejor experiencia visual",
            "Los sistemas de ecuaciones requieren matrices cuadradas compatibles",
            "Exporta tus gráficas y resultados para uso posterior"
        ]
        
        for i, tip in enumerate(tips, 1):
            tip_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            tip_frame.pack(fill="x", padx=30, pady=5)
            
            # Número del tip
            num_label = ctk.CTkLabel(
                tip_frame,
                text=f"{i}",
                font=("Segoe UI", 12, "bold"),
                text_color="#6c63ff",
                width=30
            )
            num_label.pack(side="left", padx=(0, 15))
            
            # Texto del tip
            ctk.CTkLabel(
                tip_frame,
                text=tip,
                font=("Segoe UI", 13),
                text_color="#c9d1d9",
                anchor="w",
                justify="left"
            ).pack(side="left", fill="x", expand=True)
        
        # Espaciado final
        ctk.CTkFrame(info_frame, fg_color="transparent", height=20).pack()
    
    def _create_footer(self):
        """Crear pie de página"""
        footer_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="transparent",
            height=80
        )
        footer_frame.pack(fill="x")
        
        # Mensaje motivacional
        ctk.CTkLabel(
            footer_frame,
            text="✨ Aplicación modular • Intuitiva • Lista para el futuro ✨",
            font=("Segoe UI", 14, "bold"),
            text_color="#6c63ff"
        ).pack(expand=True)
        
        # Versión
        ctk.CTkLabel(
            footer_frame,
            text="Versión 2.0 - Diseñado para la excelencia matemática",
            font=("Segoe UI", 11),
            text_color="#8b949e"
        ).pack(pady=(5, 20))