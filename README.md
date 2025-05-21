# Calculadora Científica UNEMI

**Proyecto**: Aplicación de escritorio para cálculos matemáticos y simulaciones de modelos.

Desarrollada con Python y CustomTkinter, esta calculadora científica modular integra:

* Operaciones con matrices y sistemas de ecuaciones
* Polinomios y vectores
* Gráficas 2D y 3D
* Derivación e integración simbólica y numérica
* Solución de ecuaciones diferenciales (Euler, Runge–Kutta, Taylor)
* Modelos SIR de propagación epidémica
* Optimización de rutas (Dijkstra y A\*)
* Simulación de cadenas de Markov
* Generador de distribuciones y estimación de áreas por Monte Carlo
* Agricultura inteligente: riego automatizado y balance hídrico

---

## Tabla de Contenidos

1. [Requisitos](#requisitos)
2. [Instalación](#instalación)
3. [Estructura de Carpetas](#estructura-de-carpetas)
4. [Uso](#uso)
5. [Generar Ejecutable (.exe)](#generar-ejecutable-exe)
6. [Módulos](#módulos)
7. [Contribuir](#contribuir)
8. [Licencia](#licencia)

---

## Requisitos

* Python 3.8 o superior
* pip

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Instalación

1. Clonar el repositorio:

   ```bash
   ```

git clone [https://github.com/tu-usuario/Calculadora-Cientifica-UNEMI.git](https://github.com/tu-usuario/Calculadora-Cientifica-UNEMI.git)
cd Calculadora-Cientifica-UNEMI

````
2. Crear y activar entorno virtual:
   ```bash
python -m venv venv
# Windows
env\\Scripts\\activate
# macOS/Linux
source venv/bin/activate
````

3. Instalar dependencias:

   ```bash
   ```

pip install -r requirements.txt

````

---
## Estructura de Carpetas

```bash
├─ assets/            # Íconos, imágenes y recursos estáticos
├─ backend/           # Lógica y modelos matemáticos (módulos Python)
├─ frontend/          # Interfaz de usuario (CustomTkinter)
├─ main.py            # Script de arranque de la aplicación
├─ requirements.txt   # Dependencias del proyecto
└─ venv/              # Entorno virtual (no incluir en el exe)
````

---

## Uso

Ejecutar la aplicación:

```bash
python main.py
```

Se abrirá la ventana principal con un menú lateral para acceder a cada módulo.

---

## Generar Ejecutable (.exe)

Usando PyInstaller:

```bash
pyinstaller \
  --onefile \
  --windowed \
  --icon assets/icono.ico \
  --add-data "assets;assets" \
  main.py
```

O con **auto-py-to-exe** (GUI):

1. `auto-py-to-exe`
2. Seleccionar `main.py` y marcar *One File* y *Window Based*
3. Incluir carpeta `assets` en *Additional Files*
4. Convertir y revisar en `dist/main.exe`

---

## Módulos

| Módulo                             | Descripción                                      |
| ---------------------------------- | ------------------------------------------------ |
| Matrices                           | Operaciones, inversa, determinantes, sistemas    |
| Polinomios                         | Evaluación, derivada, raíces                     |
| Vectores                           | Suma, producto, magnitud, visualización          |
| Gráficas 2D y 3D                   | Trazado de funciones y superficies               |
| Cálculo (Derivación e Integración) | Simbólico y numérico                             |
| Ecuaciones Diferenciales           | Métodos analítico, Euler, RK4, Taylor            |
| Propagación Epidémica (SIR)        | Simulación de contagios                          |
| Optimización de Rutas              | Dijkstra y A\*                                   |
| Cadenas de Markov                  | Matriz de transición y estado estable            |
| Distribuciones y Monte Carlo       | Uniforme, Poisson, Exponencial, Binomial, Normal |
| Agricultura Inteligente            | Riego automatizado y balance hídrico             |

---

## Contribuir

1. Hacer fork del repositorio
2. Crear una rama (`git checkout -b feature/nombre`)
3. Hacer commit de tus cambios (`git commit -m "feat: mensaje"`)
4. Push a la rama (`git push origin feature/nombre`)
5. Crear un Pull Request

---

## Licencia

Este proyecto está bajo la licencia MIT. Lee el archivo [LICENSE](LICENSE) para más detalles.
