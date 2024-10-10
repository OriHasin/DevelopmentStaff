from app import create_app
from config import DevConfig    # Development Environment


app = create_app(DevConfig)

if __name__ == '__main__':
    app.run()
