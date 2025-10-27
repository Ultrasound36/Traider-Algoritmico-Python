# Ambiente de Desarrollo Python

Este repositorio contiene varios proyectos de Python con diferentes enfoques.

## Repositorios

* **Curso-Python**: Contiene material y ejercicios del curso de Python de Santander.
* **Curso-Python-MS**: Contiene demos y ejemplos de Python para servicios de Microsoft, incluyendo OpenAI y embeddings de vectores.
* **Traider-Algoritmico-Python**: Contiene scripts para trading algorítmico en Python.

## Configuración Local

Para levantar el ambiente en local, se recomienda seguir los siguientes pasos:

1. **Clonar el repositorio:**

    ```bash
    git clone <URL-del-repositorio>
    cd Ambiente-Python
    ```

2. **Crear un entorno virtual:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Instalar dependencias:**
    Cada subdirectorio de proyecto puede tener su propio archivo `requirements.txt`. Navega a cada directorio de proyecto y corre:

    ```bash
    pip install -r requirements.txt
    ```
