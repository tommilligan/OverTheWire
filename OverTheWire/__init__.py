#!/usr/bin/env python

import argparse
import errno
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
        if e.errno != errno.EEXIST:
            pass

class OTWLevel(object):
    def __init__(self, wargame, levelNumber, configFile=CONNECTIONS_YML):
        self.wargame = wargame
        self.levelNumber = int(levelNumber)
        
        self.levelName = "{0}{1}".format(self.wargame, self.levelNumber)
        self.logger = logging.getLogger("otw.{0}".format(self.levelName))
        self.passwordDirectory = os.path.join("passwords", self.wargame)
        self.passwordFile = os.path.join(self.passwordDirectory, self.levelName)
        self.configFile = configFile

    def savePassword(self, newPassword):
        self.logger.debug("Saving down password")
        try:
            ensure_mkdir(self.passwordDirectory)
            with open(self.passwordFile, "w") as passwordFileHandle:
                passwordFileHandle.write(newPassword)
        except IOError as e:
            raise OTWException("Error saving password to file; {0}".format(e))

    def loadPassword(self):
        self.logger.debug("Looking up password")
        try:
            with open(self.passwordFile, "r") as passwordFileHandle:
                password = passwordFileHandle.read().strip()
                self.logger.debug("Retreived password '{0}'".format(password))
        except IOError as e:
            if e.errno == errno.ENOENT:
                raise OTWException("No password file found; {0}".format(e))
        return password

    def config(self):
        self.logger.debug("Loading configuration")
        with open(self.configFile, "r") as stream_yml:
            try:
                yml = yaml.load(stream_yml)
            except yaml.YAMLError as e:
                raise OTWException("Error parsing connections config file; {0}".format(e))

            try:
                config = yml[self.wargame]
                self.logger.debug("Loaded config; {0}".format(config))
                # Check we have the minimum config set
                domain = config["domain"]
                port = config["port"]
            except KeyError as e:
                raise OTWException("Bad configuration; {0} not found".format(e))
        return config

    def connectionCommand(self):
        self.logger.debug("Getting connection command")
        config = self.config()
        target = "{0}@{1}".format(self.levelName, config["domain"])
        command = ' '.join(["sshpass",
                    "-p", self.loadPassword(),
                    "ssh",
                    "-o", "StrictHostKeyChecking=no",
                    "-p", str(config["port"]),
                    target])
        return command

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
        level = OTWLevel(args.wargame, args.level)
        if args.password:
            try:
                level.savePassword(args.password)
            except OTWException as e:
                logger.warn(e)
        connectionCommand = level.connectionCommand()      
    except OTWException as e:
        logger.error(e)
        sys.exit(1)    

    logger.info("Connecting to {0}...".format(level.levelName))
    logger.debug("Printing '{0}'".format(connectionCommand))
    print(connectionCommand)
    logger.debug("Main completed")

if __name__ == "__main__":
    main()
