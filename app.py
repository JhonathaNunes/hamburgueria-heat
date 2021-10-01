from app import init_app
from app.telegram_bot.telegram_bot import main
import threading

app = init_app()


class FlaskThread(threading.Thread):
    def run(self) -> None:
        app.run(host='0.0.0.0')


if __name__ == '__main__':
    flask_thread = FlaskThread()
    flask_thread.start()

    main()
