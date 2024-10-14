from app import create_app

app=create_app()

@app.route('/')
def home():
    return "Hello, World!"

if __name__=='__main__':
    print("Starting the Flask application...")
    app.run(debug=True,port=5004)
