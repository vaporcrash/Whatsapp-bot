from app import app


@app.route("/health")
def health():
    return "Alive and kicking!"


def create_question():
    return

def retrieve_question():
    return

def update_question():
    return

def delete_question():
    return