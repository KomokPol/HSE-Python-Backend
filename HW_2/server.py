from flask import Flask
from flask import jsonify
from dotenv import dotenv_values
from flask import request
from controllers import operation

app = Flask(__name__)


@app.route("/")
def server_info() -> str:
    return "My server"


@app.route('/author')
def author():
    auth = {
        'name': 'Polina',
        'course': 2,
        'age': 19,
    }
    return jsonify(auth)


@app.route('/sum')
def runner():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    return jsonify({'sum': operation(a, b)})


def get_port() -> int:
    config = dotenv_values('.env')
    port_value = config.get('PORT')
    try:
        if port_value is not None:
            return int(port_value)
    except (ValueError, TypeError):
        pass
    return 5000


if __name__ == "__main__":
    app.run(debug=True, port=get_port())
