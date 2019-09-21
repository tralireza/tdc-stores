import argparse
import sys
import json
import logging
from lib import (db, rwlock)


FORMAT = '%(asctime)s %(levelname)s %(name)s|%(module)s|%(funcName)s|%(lineno)d %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()


def distance_normalise(distance_string):
    """
    Valid strings are like 4.3 or 5m or 7.3km
    """
    distance_string = distance_string.lower()
    if distance_string.endswith('km'):
        try:
            return float(distance_string[:-2]), False
        except ValueError:
            return -1, None
    if distance_string.endswith('m'):
        try:
            return float(distance_string[:-1]), True
        except ValueError:
            return -1, None
    try:
        return float(distance_string), True
    except ValueError:
        return -1, None


def get_params(argv):
    def action(a):
        if a.lower() in ['list', 'search']:
            return a.lower()
        else:
            raise argparse.ArgumentTypeError('Not a valid action, it could either be: "list" or "search"')

    def distance(a):
        v, _ = distance_normalise(a)
        if v == -1:
            raise argparse.ArgumentTypeError('Must be a positive number, ie 7.2km or 8 or 12m')
        return a

    parser = argparse.ArgumentParser(prog='cli', description='TDC-Stores CLI.')

    parser.add_argument('action', type=action,
                        help='what to do, ie: <list | search>'
                             ' [ list: show all the stores ]'
                             ' [ search: look for stores in the radius of postcode ]')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='be verbose...')
    parser.add_argument('-g', '--include-geo-data', default=False, action='store_true',
                        help='(list) include longitude and latitude in the list, first load the data from postcodes.io')
    parser.add_argument('-p', '--postcode', metavar='postcode',
                        help='(search) postcode looking for near stores, ie TW2 5AH or tw25ah')
    parser.add_argument('-d', '--distance', metavar='distance', type=distance,
                        help='(search) distance in either miles/Km, ie 2km or 7m, defaults to miles: 7 is 7m')

    args = parser.parse_args(argv)
    return vars(args)


def run():
    params = get_params(sys.argv[1:])

    if params['verbose']:
        logging.getLogger().setLevel('DEBUG')

    rw_lock = rwlock.ReadWriteLock()
    database = db.database

    with_geo_data = params['include_geo_data'] or params['action'] == 'search'

    logger.info('Loading database...')

    db.db_loader(rw_lock, reset_database=not with_geo_data, logger=logger)
    logger.info('Complete.')

    if params['action'] == 'list':
        print(json.dumps(database['stores'], indent=2))
    if params['action'] == 'search':
        postcode = db.postcode_normalize(params['postcode'])
        if postcode not in database['keys']:
            logger.error('Postcode not valid. No information is held for it in the database.')
        else:
            distance, miles = distance_normalise(params['distance'])
            result = db.search(postcode, distance, miles=miles)
            print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
