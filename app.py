"""
Compatibilidade para executar com `python app.py` ou `gunicorn app:create_app()`.
"""

import os

from run import create_app


app = create_app()


if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))

    app.run(debug=debug_mode, host=host, port=port)
