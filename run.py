from src.app import app
from src.config import settings

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.port, debug=settings.flask_env == "development")
