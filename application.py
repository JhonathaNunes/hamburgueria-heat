from app import init_app
application = init_app()

if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0')
