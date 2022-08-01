#!/usr/bin/env python3
"""
Arrancar gunicorn para que se ejecute el servicio de la API
"""
import argparse
import os
import sys


def main():
    """Main function"""

    # Parsear argumentos
    parser = argparse.ArgumentParser(description="Arrancar gunicorn")
    parser.add_argument("-r", "--reload", type=bool, default=True)
    parser.add_argument("-w", "--workers", type=int, default=4)
    parser.add_argument("-b", "--bind", type=str, default="0.0.0.0:8006")
    parser.add_argument("-k", "--worker-class", type=str, default="uvicorn.workers.UvicornWorker")
    args = parser.parse_args()

    # Definir comando a ejecutar
    reload_str = "--reload" if args.reload else ""
    cmd = f"gunicorn {reload_str} -w {args.workers} -b {args.bind} -k {args.worker_class} citas_admin.app:app"
    print(cmd)

    # Ejecutar comando
    os.system(cmd)


if __name__ == "__main__":
    main()
    sys.exit(0)
