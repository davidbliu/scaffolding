#!/usr/bin/env python

import argparse
import atexit
import sys
import urlparse

from flask import Flask, request, jsonify
import marathon

from stores import InMemoryStore, SyslogUdpStore


app = Flask(__name__)

# re-initialize later
events = None
event_store = None

def on_exit(marathon_client, callback_url):
    marathon_client.delete_event_subscription(callback_url)

@app.route('/events', methods=['POST'])
def event_receiver():
    print 'hello'
    # event = request.get_json()
    # event_store.save(event)
    # return ''

@app.route('/events', methods=['GET'])
def list_events():
    print 'i have arrived here'
    # return jsonify({'events': event_store.list()})

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    print 'callback'
    try:
        event = request.get_json()
        print event
    except:
        print 'no event'
    return jsonify(result={"status": 200})

@app.route('/marathon', methods=['GET'])
def marathon_register():
    print 'marathon stuff happening here'
    marathon_url = 'localhost:8080'
    callback_url = 'localhost:5000/callback'
    m = marathon.MarathonClient(marathon_url)
    m.create_event_subscription(callback_url)
    atexit.register(on_exit, m, callback_url)
    return jsonify(result={"status": 200})


if __name__ == '__main__':
    print 'cool stuff dude'
    # parser = argparse.ArgumentParser(description='Marathon Logging Service')
    # parser.add_argument('-m', '--marathon-url', required=True, help='Marathon server URL (http[s]://<host>:<port>[<path>])')
    # parser.add_argument('-c', '--callback-url', required=True, help='callback URL for this service (http[s]://<host>:<port>[<path>]/events')
    # parser.add_argument('-e', '--event-store', default='in-memory://localhost/', help='event store connection string (default: in-memory://localhost/)')
    # parser.add_argument('-p', '--port', type=int, default=5000, help='Port to listen on (default: 5000)')
    # parser.add_argument('-i', '--ip', default='0.0.0.0', help='IP to listen on (default: 0.0.0.0)')
    # args = parser.parse_args()

    # event_store_url = urlparse.urlparse(args.event_store)

    # if event_store_url.scheme == 'in-memory':
    #     event_store = InMemoryStore(event_store_url)
    # elif event_store_url.scheme == 'syslog':
    #     event_store = SyslogUdpStore(event_store_url)
    # else:
    #     print 'Invalid event store type: "{scheme}" (from "{url}")'.format(scheme=event_store_url.scheme, url=args.event_store)
    #     sys.exit(1)


    marathon_url = 'http://localhost:8080'
    callback_url = 'http://localhost:5000/callback'
    m = marathon.MarathonClient(marathon_url)
    m.create_event_subscription(callback_url)
    atexit.register(on_exit, m, callback_url)

    app.run(port=5000, host='localhost')