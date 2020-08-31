from flask import Flask, json, request, session
from modules import server
from modules import loggingconf
import logging

loggingconf.init()

log = logging.getLogger(__name__)
log.debug("Logging is configured.")

api = Flask(__name__,  static_url_path='', static_folder='web')
api.secret_key = b'dfjk34889234_100'

server.init('')

# server routing
@api.route('/')
def rootRouteProcessor():
    return api.send_static_file('index.html')


@api.route('/api/say', methods=['POST'])
def sayRouteProcessor():
    return server.sayRequestProcessor()


# server start
if __name__ == '__main__':
    api.run(debug=True)