from app import create_app

def main():
    app = create_app()
    app.socketio.run(app, **app.boot_params)

if __name__ == "__main__":
    main()
