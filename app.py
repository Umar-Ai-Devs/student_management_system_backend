from src import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

app = create_app()


@app.route('/',methods=['GET'])
def home():
    return "<h1>Welcome to the Student Management System<h1>"