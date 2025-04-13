from app import create_app
from app.args import parse_args

def main():
    app = create_app()

    if parse_args(app):
        exit(0)
    else:
        app.socketio.run(app, **app.boot_params)

if __name__ == "__main__":
    main()
