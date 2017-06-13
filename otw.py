#!/usr/bin/env python3

import argparse
import logging
import os
import sys
import yaml

# Global variables
CONNECTIONS_YML = "connections.yml"

# Logging setup
logger = logging.getLogger("otw")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("%(name)s|%(levelname)s|%(message)s"))
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class OTWException(Exception):
    pass

def lookup_level_password(wargame, level):
    username = "{0}{1}".format(wargame, level)
    logger.debug("Looking up password for {0}".format(username))
    password_path = os.path.join("passwords", wargame, username)
    logger.debug("Password file should be at '{0}'".format(password_path))    
    try:
        with open(password_path, "r") as password_fh:
            password = password_fh.read().strip()
            logger.debug("Retreived password '{0}'".format(password))
    except OSError as e:
        if e.errno == 2:
            raise OTWException("No password file found for '{0}'".format(username))
    return password

def get_wargame_connection_config(wargame):
    logger.debug("Loading '{0}' connection configuration".format(wargame))
    with open(CONNECTIONS_YML, "r") as stream_yml:
        try:
            yml = yaml.load(stream_yml)
        except yaml.YAMLError as e:
            raise OTWException("Error parsing connections config file; {0}".format(e))

        try:
            config = yml[wargame]
            logger.debug("Config for '{0}'; {1}".format(wargame, config))
            # Check we have the minimum config set
            domain = config["domain"]
            port = config["port"]
        except KeyError as e:
            raise OTWException("Wargame '{0}' not configured correctly; {1} not found".format(wargame, e))
    
    return config

def main_parser():
    logger.debug("Generating argument parser")
    parser = argparse.ArgumentParser(description="Connect to an OverTheWire wargame")
    parser.add_argument("wargame",
                        help="Wargame name")
    parser.add_argument("level", type=int,
                        help="Level number")
    parser.add_argument("-p", "--password",
                        help="Level password (defaults to passwords folder)")
    return parser

def main():
    logger.debug("Main called")
    parser = main_parser()
    args = parser.parse_args()
    logger.debug("Got arguments {0}".format(args))

    try:
        config = get_wargame_connection_config(args.wargame)
        if args.password:
            password = args.password
        else:
            password = lookup_level_password(args.wargame, int(args.level))

        username = "{0}{1}".format(args.wargame, args.level)
        target = "{0}@{1}".format(username, config["domain"])
        command = ' '.join(["sshpass",
                    "-p", password,
                    "ssh",
                    "-p", str(config["port"]),
                    target])
    except OTWException as e:
        logger.error(e)
        sys.exit(1)    

    logger.info("Connecting to {0}{1}...".format(args.wargame, args.level))
    logger.debug("Printing arguments '{0}'".format(command))
    print(command)

if __name__ == "__main__":
    main()
