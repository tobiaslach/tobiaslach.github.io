import logging
from flask import Flask, render_template

from update_schedule import update_schedule

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/refresh', methods=['POST'])
def refresh():
    logging.info("Manual refresh requested")
    try:
        update_schedule()
        return '', 204
    except Exception as exc:
        logging.exception("Failed to update schedule: %s", exc)
        return 'error', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
