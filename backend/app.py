from flask import Flask
from flask_cors import CORS
from routes.file_routes import file_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(file_bp, url_prefix="/files")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
