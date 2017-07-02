#!/usr/bin/env python

import argparse
import logging

import OverTheWire

# Logging setup
logger = logging.getLogger("otw")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("%(name)s|%(levelname)s|%(message)s"))
ch.setLevel(logging.INFO)
logger.addHandler(ch)

# Global variables
CONNECTIONS_YML = "connections.yml"

# Comand line interface
def main_parser():
    logger.debug("Generating argument parser")
    parser = argparse.ArgumentParser(description="Connect to an OverTheWire wargame")
    parser.add_argument("wargame",
                        help="Wargame name")
    parser.add_argument("level", type=int,
                        help="Level number")
    parser.add_argument("-p", "--password",
                        help="Level password (defaults to passwords folder)")
    parser.add_argument("--debug", action="store_true",
                        help="Show DEBUG logging (defaults to INFO)")
    return parser

def main():
    logger.debug("Main called")
    parser = main_parser()
    args = parser.parse_args()
    logger.debug("Got arguments {0}".format(args))
    
    if args.debug:
        ch.setLevel(logging.DEBUG)

    try:
        level = OverTheWire.OTWLevel(args.wargame, args.level)
        if args.password:
            try:
                level.savePassword(args.password)
            except OTWException as e:
                logger.warn(e)
        command = level.startCommand()      
    except OTWException as e:
        logger.error(e)
        sys.exit(1)    

    logger.info("Connecting to {0}...".format(level.levelName))
    logger.debug("Printing '{0}'".format(command))
    print(command)
    logger.debug("Main completed")

if __name__ == "__main__":
    main()
