"""
===============================================================================
Project: InstagramFollowerBot
Author:  Joaquin Albano
Date:    2025-10-30
Version: 1.0.0
Python:  3.12+
-------------------------------------------------------------------------------
Description:
    Este script ejecuta el flujo principal del bot de Instagram. El bot:
      1. Inicia sesión usando credenciales almacenadas en el archivo .env.
      2. Accede al perfil objetivo y abre la lista de seguidores.
      3. Sigue automáticamente a una cantidad configurada de usuarios (por defecto 15).
         - Gestiona popups de confirmación y scroll en la ventana modal.
         - Incluye pausas aleatorias para simular comportamiento humano.

Dependencies:
    - selenium >= 4.22.0
    - python-dotenv
    - Google Chrome (instalado y compatible con chromedriver)

Environment Variables (.env):
    USERNAME
    PASSWORD

Usage:
    $ python main.py
-------------------------------------------------------------------------------
License:
    MIT License - Este script puede utilizarse y modificarse libremente
    siempre que se mencione al autor original.
===============================================================================
"""

from instafollower import InstFollower


def main():
    """Ejecuta el flujo principal del bot de Instagram."""
    instafollower = InstFollower()
    instafollower.login()
    instafollower.find_followers()
    instafollower.follow()


if __name__ == "__main__":
    main()