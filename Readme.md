# Proyecto de Desarrollo con Entorno Virtual y PyQt5

Este README contiene las instrucciones necesarias para configurar el entorno virtual y ejecutar el proyecto correctamente utilizando **Python 3.11.8**.

---

## 1. Prerrequisitos

Asegúrate de tener instalado **Python 3.11.8** y **pip**.

### Instalar virtualenv
Para manejar las dependencias y evitar conflictos con otras bibliotecas, usaremos un entorno virtual:

```bash
pip install virtualenv
```

---

## 2. Crear y Activar el Entorno Virtual

### Crear el entorno virtual
Usa el siguiente comando para crear el entorno virtual:

```bash
virtualenv -p python env_IDE
```

Esto generará una carpeta llamada `env_IDE` en el directorio actual.

### Activar el entorno virtual
Dependiendo de tu sistema operativo:

- **Windows**:
  ```bash
  .\env_IDE\Scripts\activate
  ```

- **Linux/Mac**:
  ```bash
  source env_IDE/bin/activate
  ```

---

## 3. Instalar Dependencias

Una vez activado el entorno virtual, instala las dependencias necesarias. En este caso, **PyQt5**:

```bash
pip install PyQt5
```

---

## 4. Estructura del Proyecto

El desarrollo del proyecto se realizará en la carpeta `src`:

```
proyecto/
│
├── env_IDE/            # Entorno virtual
├── src/                # Carpeta para el desarrollo del código
│   └── main.py         # Script principal
└── README.md           # Archivo de instrucciones
```

---

## 5. Ejecutar el Código

Una vez dentro del entorno virtual y con las dependencias instaladas, ejecuta el proyecto con el siguiente comando:

```bash
py .\src\main.py
```

---

## 6. Salir del Entorno Virtual
Para desactivar el entorno virtual cuando termines de trabajar, usa el siguiente comando:

```bash
deactivate
```

---

## ¿Qué es un Compilador? - Compiladores I y II

Un **compilador** es una herramienta fundamental en el mundo de la programación, encargada de traducir el código fuente (escrito por el programador) a un lenguaje de bajo nivel o código máquina que pueda ser ejecutado por la computadora. Este proceso permite que un programa escrito en lenguajes como **C, Java o Python** se convierta en instrucciones entendibles por la máquina.

En las materias **Compiladores I y II** de la **Universidad Autónoma de Aguascalientes**, aprenderás:

- **Análisis Léxico, Sintáctico y Semántico**:
  - **Léxico**: Cómo se descompone el código fuente en componentes básicos (tokens).
  - **Sintáctico**: Cómo se validan las reglas del lenguaje mediante la estructura del código.
  - **Semántico**: Cómo se asegura que las instrucciones tengan un significado válido en el contexto del programa.
- **Generación de Código Intermedio y Optimización**: Técnicas para mejorar el rendimiento del código generado.
- **Traducción de Lenguajes**: Cómo desarrollar compiladores para transformar lenguajes de alto nivel a instrucciones ejecutables.

Un compilador no solo es una herramienta, ¡es la columna vertebral de todo software moderno! Comprender cómo funciona te abrirá las puertas para dominar lenguajes de programación, construir herramientas propias y mejorar el rendimiento de tus desarrollos.

---

## Notas
- Verifica que estás usando la versión correcta de Python (3.11.8).
- Asegúrate de activar el entorno virtual antes de instalar cualquier dependencia o correr el proyecto.

---

⚠️ **Advertencia**: Este proyecto contiene errores en la generación, con algunos fallos en el árbol de análisis y en la generación de código intermedio. Úsalo con precaución y con fines de aprendizaje.

¡Listo! Ahora tu entorno está configurado y puedes empezar a desarrollar.
