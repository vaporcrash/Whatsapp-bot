from app import app
from app.routes import question

if __name__ == '__main__':
    app.run("0.0.0.0","8443")