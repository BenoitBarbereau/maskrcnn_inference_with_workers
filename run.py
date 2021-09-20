"""App entry point."""
from app import app
import config

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host=config.URL, port=config.PORT)
