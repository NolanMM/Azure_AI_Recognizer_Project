import subprocess
import sys
import os


def create_virtualenv(env_name):
    python_executable = sys.executable  # Get path to the current Python interpreter
    subprocess.run([python_executable, "-m", "venv", env_name])  # Create virtual environment


def install_requirements(env_name, requirements_file):
    python_executable = os.path.join(env_name, "Scripts", "python.exe") if os.name == "nt" else os.path.join(env_name, "bin", "python")
    subprocess.run([python_executable, "-m", "pip", "install", "-r", requirements_file])  # Install requirements


def main():
    env_name = ".venv"
    requirements_file = "requirements.txt"

    create_virtualenv(env_name)
    install_requirements(env_name, requirements_file)


if __name__ == "__main__":
    main()
