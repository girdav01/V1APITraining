# This is a version of the Cookbook for ES that only persist to disk for API training purpose only
import datetime
import argparse
import os
import json
import requests

# default settings
import tmconfig

# V1_TOKEN = os.environ.get('TMV1_TOKEN', '')
V1_TOKEN= tmconfig.xdr_token
# V1_URL = os.environ.get('TMV1_URL', 'https://api.xdr.trendmicro.com')
V1_URL = tmconfig.region['us']


def check_datetime_aware(d):
    return (d.tzinfo is not None) and (d.tzinfo.utcoffset(d) is not None)


class TmV1Client:
    base_url_default = V1_URL
    oat_size_default = 50
    # API seems to have the maximum value of 'size' parameter, 200
    oat_size_max = 200

    def __init__(self, token, base_url=None):
        if not token:
            raise ValueError('Authentication token missing')
        self.token = token
        self.base_url = base_url or TmV1Client.base_url_default

    def make_headers(self):
        return {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json;charset=utf-8'
        }

    def get(self, path, **kwargs):
        kwargs.setdefault('headers', {}).update(self.make_headers())
        r = requests.get(self.base_url + path, **kwargs)
        if ((200 == r.status_code)
                and ('application/json' in r.headers.get('Content-Type', ''))):
            return r.json()
        raise RuntimeError(f'Request unsuccessful (GET {path}):'
                           f' {r.status_code} {r.text}')

    def post(self, path, **kwargs):
        kwargs.setdefault('headers', {}).update(self.make_headers())
        r = requests.post(self.base_url + path, **kwargs)
        if ((200 == r.status_code)
                and ('application/json' in r.headers.get('Content-Type', ''))):
            return r.json()
        raise RuntimeError(f'Request unsuccessful (POST {path}):'
                           f' {r.status_code} {r.text}')

    def get_workbench_histories(self, start, end, offset=None, size=None):
        if not check_datetime_aware(start):
            start = start.astimezone()
        if not check_datetime_aware(end):
            end = end.astimezone()
        start = start.astimezone(datetime.timezone.utc)
        end = end.astimezone(datetime.timezone.utc)
        start = start.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        end = end.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        # API returns data in the range of [offset, offset+limit)
        return self.get(
            '/v2.0/xdr/workbench/workbenchHistories',
            params=dict([('startTime', start), ('endTime', end),
                        ('sortBy', '-createdTime')]
                        + ([('offset', offset)] if offset is not None else [])
                        + ([('limit', size)] if size is not None else [])
                        ))['data']['workbenchRecords']

    def get_oat(self, start, end, size=None, nextBatchToken=None):
        if size is None:
            size = TmV1Client.oat_size_default
        start = int(start.timestamp())
        end = int(end.timestamp())
        # API returns data in the range of [start, end]
        data = self.get('/v2.0/xdr/oat/detections', params=dict([
            ('start', start), ('end', end), ('size', size),
        ]
            + ([('nextBatchToken', nextBatchToken)]
                if nextBatchToken is not None else [])
        ))['data']
        return data['detections'], data.get('nextBatchToken', '')

    def get_detection(self, start, end, offset=None, query=None):
        return self.post('/v2.0/xdr/search/data', json=dict([
            ('fields', []),
            ('from', int(start.timestamp())),
            ('to', int(end.timestamp())),
            ('source', 'detections'),
            ('query', query if query is not None else 'hostName: *')
        ]
            + ([('offset', offset)] if offset is not None else [])
        ))['data']['logs']


def fetch_workbench_alerts(v1, start, end):
    """
    This function do the loop to get all workbench alerts by changing
    the parameters of both 'offset' and 'size'.
    """
    offset = 0
    size = 100
    alerts = []
    while True:
        gotten = v1.get_workbench_histories(start, end, offset, size)
        if not gotten:
            break
        print(f'Workbench alerts ({offset} {offset+size}): {len(gotten)}')
        alerts.extend(gotten)
        offset = len(alerts)
    return alerts


def fetch_observed_attack_techniques(v1, start, end):
    """
    This functions do the loop to get the oat events by changing the parameters
    of 'nextBatchToken' if the response has it.
    """
    if not check_datetime_aware(start):
        start = start.astimezone()
    if not check_datetime_aware(end):
        end = end.astimezone()
    start = start.astimezone(datetime.timezone.utc)
    end = end.astimezone(datetime.timezone.utc)
    detections = []
    size = TmV1Client.oat_size_max
    next_token = ''
    offset = 0
    while True:
        gotten, next_token = v1.get_oat(start, end, size, next_token)
        print(f'Observed Attack Technique events({offset} {offset+size}):'
              f' {len(gotten)}')
        detections.extend(gotten)
        if not next_token:
            break
        offset = len(detections)
    return detections


def fetch_detections(v1, start, end):
    """
    This function do the loop to get the detections by changing the parameter
    of the offset.
    """
    offset = 0
    logs = []
    while True:
        gotten = v1.get_detection(start, end, offset)
        if not gotten:
            break
        print(f'Other detections({start} {end}): {len(gotten)}')
        logs.extend(gotten)
        offset = len(logs)
    return logs


def correct_data(docs):
    """
    This function correct VisionOne data for Elasticsearch

    1. The workbench detail has ['inpactScope'][N]['entityValue'] and
       ['indicators'][N]['objectValue'] have two kinds of types; one is string
       and the other is object.
       Because Elasticsearch cannot define the union of both string and object,
       this function names these string fields 'entityValue' and 'objectValue'
       to 'entityString' and 'objectString', respectively.

    2. The three kinds of data have different names for timestamp.
       This function names the same field for timestamp, 'es_basetime'.

    3. Both workbench and detections have the 'severity' field with different
       type; workbench is string and detections is integer.
       Because Elasticsearch cannot define the union of both string and
       integer, this function name the string field to another one,
       'severityString'.
    """


    for d in docs['workbench']:
        for entity in d['detail']['impactScope']:
            if isinstance(entity['entityValue'], str):
                entity['entityString'] = entity['entityValue']
                entity['entityValue'] = {}
        for entity in d['detail']['indicators']:
            if isinstance(entity['objectValue'], str):
                entity['objectString'] = entity['objectValue']
                entity['objectValue'] = {}
        if 'severity' in d:
            d['severityString'] = d['severity']
            del d['severity']
        d['es_basetime'] = d['detail']['workbenchCompleteTimestamp']
    for d in docs['observed_techniques']:
        d['es_basetime'] = d['detectionTime']
    if 'detections' in docs:
        for d in docs['detections']:
            d['es_basetime'] = d['eventTimeDT'].replace('+00:00', 'Z')


def index_data_to_es(docs, include_detections):
    #def index_actions(name, data):
    #    for source in data:
    #        yield {
    #            '_index': name,
    #            '_op_type': 'index',
    #            '_source': source
    #        }
    for name, data in docs.items():
        if ('detections' == name) and (not include_detections): continue
        with open(name + '.out', 'w') as fp:
            json.dump(data, fp, indent=2)



def pull_v1_data_to_files(v1, start, end, include_detections):

    docs = {}
    docs['workbench'] = fetch_workbench_alerts(v1, start, end)
    docs['observed_techniques'] = fetch_observed_attack_techniques(
        v1, start, end)
    if include_detections:
        docs['detections'] = fetch_detections(v1, start, end)
    correct_data(docs)
    for name, data in docs.items():
        if ('detections' == name) and (not include_detections): continue
        with open(name + '.out', 'w') as fp:
            json.dump(data, fp, indent=2)


def main(start, end, days, v1_token, v1_url, detections):
    if end is None:
        end = datetime.datetime.now(datetime.timezone.utc)
    else:
        end = datetime.datetime.fromisoformat(end)
    if start is None:
        start = end + datetime.timedelta(days=-days)
    else:
        start = datetime.datetime.fromisoformat(start)

    v1 = TmV1Client(v1_token, v1_url)

    pull_v1_data_to_files(v1, start, end, detections)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=('Send Workbench alerts and other detection data '
                     'to Elasticsearch'),
        epilog=(f'Example: python {os.path.basename(__file__)} '
                '-e 2021-04-12T14:28:00.123456+00:00 -d 5 -D'))
    parser.add_argument(
        '-s', '--start',
        help=('Timestamp in ISO 8601 format that indicates the start of'
              ' the data retrieval time range'))
    parser.add_argument(
        '-e', '--end',
        help=('Timestamp in ISO 8601 format that indicates the end of the data'
              ' retrieval time range. The default value is the current time.'))
    parser.add_argument(
        '-d', '--days', type=int, default=5,
        help=('Number of days before the end time of the data retrieval'
              ' time range. The default value is 5.'))
    parser.add_argument(
        '-t', '--v1-token', default=V1_TOKEN,
        help=('Authentication token of your Trend Micro Vision One'
              ' user account'))
    parser.add_argument(
        '-r', '--v1-url',
        default=TmV1Client.base_url_default,
        help=('URL of the Trend Micro Vision One server for your region.'
              f' The default value is "{TmV1Client.base_url_default}"'))
    parser.add_argument(
        '-D', '--detections', action='store_true',
        help=('Parameter that searches the "Detections" data via API'
              ' and sends matching records to Elasticsearch'))

    main(**vars(parser.parse_args()))
