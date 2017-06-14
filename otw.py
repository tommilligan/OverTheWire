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
ch.setLevel(logging.INFO)
logger.addHandler(ch)

class OTWException(Exception):
    pass

def ensure_mkdir(path):
    logger.debug("Ensuring directory '{0}' exists".format(path))
    try:
        os.mkdir(path)
    except OSError as e:
        if e.errno != 17:
            pass

def handle_level_password(wargame, level, password):
    username = "{0}{1}".format(wargame, level)
    password_dir = os.path.join("passwords", wargame)
    password_path = os.path.join(password_dir, username)
    logger.debug("Password file at '{0}'".format(password_path))    
        
    if password:
        logger.debug("Saving down password for {0}".format(username))
        try:
            ensure_mkdir(password_dir)
            with open(password_path, "w") as password_fh:
                password_fh.write(password)
        except OSError as e:
            logger.warn("Error saving password for '{0}'; {1}".format(username, e))
    else:
        logger.debug("Looking up password for {0}".format(username))
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
        # Get wargame information
        config = get_wargame_connection_config(args.wargame)

        # Save/load password as necessary
        password = handle_level_password(args.wargame, args.level, args.password)

        # Format command
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
