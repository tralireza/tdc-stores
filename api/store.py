import threading
import flask
from lib import (rwlock, db)


rw_lock = rwlock.ReadWriteLock()
database = db.database

DATA_NOT_READY = {'code': 1001, 'message': 'Data not ready yet! Please try again later.'}
POSTCODE_NOT_FOUND = {'code': 1002, 'message': 'Postcode not found!'}

bp = flask.Blueprint('stores', __name__, url_prefix='/stores')


@bp.route('admin/reset_database', methods=['GET'])
@bp.route('admin/load_database', methods=['GET'])
def load_database():
    logger = flask.current_app.logger
    logger.info('Loading database... This may take a while!')

    reset_db = False
    if flask.request.path.endswith('admin/reset_database'):
        reset_db = True

    rw_lock.acquire_write()
    try:
        if not database['loading']:
            database['loading'] = True
            loader_thread = threading.Thread(target=db.db_loader, args=(rw_lock, reset_db, logger))
            loader_thread.start()
            return flask.jsonify({'code': 2002, 'message': 'Loading database. May take a while!'})
        return flask.jsonify({'code': 2001, 'message': 'Still loading...'}), 202
    finally:
        rw_lock.release_write()


@bp.route('', methods=['GET'])
def stores():
    rw_lock.acquire_read()
    try:
        if database['ready']:
            return flask.jsonify(database['stores'])
        return flask.jsonify(DATA_NOT_READY), 202
    finally:
        rw_lock.release_read()


@bp.route('<postcode>', methods=['GET'])
def get(postcode):
    rw_lock.acquire_read()
    try:
        if database['ready']:
            key = db.postcode_normalize(postcode)
            if key in database['keys']:
                return flask.jsonify(db.get(key))
            else:
                return flask.jsonify(POSTCODE_NOT_FOUND), 404
        else:
            return flask.jsonify(DATA_NOT_READY), 202
    finally:
        rw_lock.release_read()


@bp.route('<postcode>/circle', methods=['GET'])
def search(postcode):
    rw_lock.acquire_read()
    try:
        if database['ready']:
            key = db.postcode_normalize(postcode)
            if key in database['keys']:
                miles = True
                try:
                    radius = flask.request.args.get('q', '')
                    if radius.lower().endswith('km'):
                        miles = False
                        radius = radius[:-2]
                    elif radius.lower().endswith('m'):
                        radius = radius[:-1]
                    radius = int(radius)
                    if radius < 0:
                        raise ValueError
                except ValueError:
                    return flask.jsonify({'code': 3003,
                                          'message': 'Radius should be a positive distance (miles/Km)'}), 400
                else:
                    result = sorted(db.search(key, radius, miles=miles), key=lambda e: e[db.FLD_LATITUDE])
                    return flask.jsonify({'radius': radius, 'postcode': key, 'result': result})
            else:
                return flask.jsonify(POSTCODE_NOT_FOUND), 404

        return flask.jsonify(DATA_NOT_READY), 202
    finally:
        rw_lock.release_read()
