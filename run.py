from app import app
import os
# from flaskblog import create_app

# app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug = os.environ.get('DEBUG') == '1')