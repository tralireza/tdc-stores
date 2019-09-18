import secrets
import logging
import flask


FORMAT = '%(asctime)s %(levelname)s %(name)s|%(module)s|%(funcName)s|%(lineno)d %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')


def create_app(test_config=None):
    app = flask.Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=secrets.token_urlsafe(64)
    )

    @app.route('/health', methods=['GET'])
    def health():
        return 'OK', 200

    from . import (store)
    app.register_blueprint(store.bp)

    return app
