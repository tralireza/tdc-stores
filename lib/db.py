import json
from urllib import (request)
from lib import (gcd)


BASE_API = 'http://api.postcodes.io/postcodes'

database = {
    'ready': False,
    'loading': False,
    'stores': [],
    'keys': []
}

FLD_POSTCODE, FLD_LONGITUDE, FLD_LATITUDE = 'postcode', 'longitude', 'latitude'


def postcode_normalize(postcode):
    """
        UK Postcode format
        https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom
        Not verifying, only normalising
    """
    postcode = postcode.replace(' ', '').upper()
    if len(postcode) == 7:
        return postcode[0: 4] + ' ' + postcode[4:]
    if len(postcode) == 5:
        return postcode[0: 2] + ' ' + postcode[2:]
    return postcode[0: 3] + ' ' + postcode[3: ]


def search(postcode, radius, miles=False):
    result = []

    origin, target = (0, 0), (0, 0)
    for store in database['stores']:
        if postcode == store[FLD_POSTCODE]:
            origin = (store[FLD_LATITUDE], store[FLD_LONGITUDE])
            break

    for store in database['stores']:
        if postcode != store[FLD_POSTCODE]:
            try:
                target = (store[FLD_LATITUDE], store[FLD_LONGITUDE])
            except KeyError:
                continue
            distance = gcd.gcd(origin, target)
            if miles:
                distance /= 1.6
            if distance <= radius:
                store['distance'] = round(distance)
                result.append(store)

    return result


def fetch_geo_data(stores, logger=None):
    geo_data, has_error = {}, False
    for i in range(0, len(stores), 10):
        postcodes = [e[FLD_POSTCODE] for e in stores[i: min(i + 10, len(stores))]]
        rq = request.Request(BASE_API,
                             data=json.dumps({'postcodes': postcodes}).encode(),
                             headers={'Content-Type': 'application/json'}, method='POST')

        if logger:
            logger.debug('api -> ' + BASE_API)
            logger.debug('headers -> ' + str(rq.headers))
            logger.debug('data[POST] -> ' + rq.data.decode())

        with request.urlopen(rq) as rsp:
            if rsp.getcode() == 200:
                for result in json.loads(rsp.read())['result']:
                    data = {}
                    key = postcode_normalize(result['query'])
                    if result['result']:
                        for field in [FLD_POSTCODE, FLD_LONGITUDE, FLD_LATITUDE]:
                            data[field] = result['result'][field]
                    geo_data[key] = data
            else:
                has_error = True
                if logger:
                    logger.error('Could not load geo-data! Status: ' + rsp.getcode())

        if logger:
            logger.info('Loaded data points in range: %d -> %d' % (i, i + len(postcodes)))

    return geo_data, has_error


def db_loader(rw_lock, reset_database=False, logger=None, json_input='stores.json'):
    with open(json_input, 'r') as stores_json:
        stores = json.loads(stores_json.read())

    if logger:
        logger.info('Loaded %i data point(s) from input: "%s"' % (len(stores), json_input))

    merged_data, keys = [], []
    if not reset_database:
        geo_data, geo_data_error = fetch_geo_data(stores, logger)

        for store in sorted(stores, key=lambda e: e['name']):
            key = postcode_normalize(store[FLD_POSTCODE])
            if geo_data.get(key):
                keys.append(key)
                for field in [FLD_POSTCODE, FLD_LONGITUDE, FLD_LATITUDE]:
                    store[field] = geo_data.get(key)[field]
            merged_data.append(store)

        if logger:
            logger.info('Geo data loaded successfully? ' + ('No!' if geo_data_error else 'Yes.'))

    rw_lock.acquire_write()
    database['loading'] = False
    database['ready'] = True
    database['stores'] = sorted(stores, key=lambda e: e['name']) if reset_database else merged_data
    database['keys'] = sorted(keys)
    rw_lock.release_write()

    if logger:
        logger.info('Database loaded.')
