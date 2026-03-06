from src import create_app

# Create the app once
app = create_app()

# Define routes
@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the Student Management System</h1>"

# Run the app only when this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)