from app import app
from app.routes import question,newman

if __name__ == '__main__':
    app.run("0.0.0.0","8443")