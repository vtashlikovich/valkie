from flask import Flask, json, request
from modules import server
import logging.config

LOGGING_CONFIG = { 
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': { 
        'default': { 
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
            # 'stream': 'ext://file.log',  # Default is stderr
        },
    },
    'loggers': { 
        '': {  # root logger
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False
        },
        'my.packg': { 
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    } 
}

logging.config.dictConfig(LOGGING_CONFIG)

log = logging.getLogger(__name__)
log.debug("Logging is configured.")
log.info("Logging is configured.")

api = Flask(__name__,  static_url_path='', static_folder='web')

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