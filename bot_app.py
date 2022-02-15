from app import my_app, Config


if __name__ == '__main__':
    my_app.run(debug=True, host=Config.APP_URL)
