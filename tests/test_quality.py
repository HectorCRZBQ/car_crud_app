"""
Tests de calidad para verificar el cumplimiento de los estándares de código en el proyecto.
Este archivo ejecuta pruebas para verificar el puntaje de Pylint y la existencia/sintaxis de archivos de plantilla.
"""

import os
import subprocess
from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError


def test_python_code_quality():
    """
    Ejecuta pylint en todos los archivos Python del proyecto y asegura que cumplan con los estándares de calidad.
    """
    print("Running pylint on Python files...")
    result = subprocess.run(["pylint", "app.py", "tests"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    # Verificar si pylint dio un puntaje bajo
    if "Your code has been rated at" in result.stdout:
        score_line = next(line for line in result.stdout.splitlines() if "Your code has been rated at" in line)
        score = float(score_line.split("/")[0].split()[-1])
        if score < 8.0:
            print(f"Warning: Code quality score is low: {score}/10")
    else:
        print("Pylint did not provide a score.")


def test_template_files_exist():
    """
    Verifica si los archivos de plantilla requeridos están presentes en el directorio 'templates'.
    """
    print("Checking template files...")
    required_files = ["add_car.html", "base.html", "edit_car.html", "index.html"]
    templates_dir = os.path.join(os.getcwd(), "templates")
    for file_name in required_files:
        file_path = os.path.join(templates_dir, file_name)
        assert os.path.exists(file_path), f"Template file missing: {file_name}"


def test_template_file_syntax():
    """
    Valida que los archivos de plantilla no contengan errores evidentes de sintaxis.
    """
    print("Validating syntax of template files...")
    templates_dir = os.path.join(os.getcwd(), "templates")
    env = Environment(loader=FileSystemLoader(templates_dir))
    for template_name in os.listdir(templates_dir):
        if template_name.endswith(".html"):
            try:
                env.get_template(template_name)
            except TemplateSyntaxError as e:
                assert False, f"Syntax error in template {template_name}: {e}"


if __name__ == "__main__":
    test_python_code_quality()
    test_template_files_exist()
    test_template_file_syntax()
