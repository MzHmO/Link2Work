# ------------------------------------------------------
#   Link2Work Project Start File
#   Urfu Project Digital Portfolio
# ------------------------------------------------------
#  
# Description:
#   main.py - entrypoint file
#   routes.py - route management
#   db.py - user's creating,  SQLite3 integration
#
#
# Author:
#   Team «Мы»


import logging
import argparse
from backend.routes import deploy_web
from backend.database import Database

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    add_help=True,
                    description=
                        "link2work.py - it is URFU Digital Project\
                        for managing users's achievements and awards \
                        in one self-hosted solution")
    parser.add_argument("-debug", action="store_true", help='Turn Debug output ON')
    parser.add_argument("-port", action="store", help="From 1 to 65536 port value on which web server will be started", default=8000)
    parser.add_argument("-host", action="store", help="IP of network interface on which deploy web app on", default="127.0.0.1")

    options = parser.parse_args()

    if options.debug is True:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')

    Database.setup_db()
    deploy_web(host=options.host, port=options.port, debug=options.debug)