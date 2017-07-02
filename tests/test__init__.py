#!/usr/bin/env python

import argparse
import unittest

import OverTheWire

class TestOTWLevelSetup(unittest.TestCase):
    def test_otw_level_setup_known_int(self):
        level = OverTheWire.OTWLevel("bandit", 0)
        self.assertEqual(level.levelNumber, 0)
        self.assertEqual(level.levelName, "bandit0")
        self.assertEqual(level.configFile, "connections.yml")        

    def test_otw_level_setup_known_str(self):
        level = OverTheWire.OTWLevel("bandit", "0", configFile="hovercraft.yml")
        self.assertEqual(level.levelNumber, 0)
        self.assertEqual(level.levelName, "bandit0")
        self.assertEqual(level.configFile, "hovercraft.yml")        

class TestOTWLevelNormal(unittest.TestCase):
    def setUp(self):
        self.level = OverTheWire.OTWLevel("bandit", 0)
        self.level.savePassword("eggs")

    def test_otw_level_savePassword(self):
        self.level.savePassword("spam")

    def test_otw_level_loadPassword(self):
        password = self.level.loadPassword()
        self.assertEqual(password, "eggs")

    def test_otw_level_config(self):
        config = self.level.config()
        self.assertEqual(config["domain"], "bandit.labs.overthewire.org")
        self.assertEqual(config["port"], 2220)

    def test_otw_level_connectionCommand(self):
        command = self.level.connectionCommand()
        self.assertEqual(command, "sshpass -p eggs ssh -o StrictHostKeyChecking=no -p 2220 bandit0@bandit.labs.overthewire.org")

    def tearDown(self):
        self.level.savePassword("bandit0")

class TestOTWLevelEdge(unittest.TestCase):
    def test_otw_level_loadPassword_not_exist(self):
        level = OverTheWire.OTWLevel("bandit", -1)
        with self.assertRaises(OverTheWire.OTWException):
            password = level.loadPassword()

    def test_otw_level_savePassword_permissions_error(self):
        level = OverTheWire.OTWLevel("bandit", 0)
        level.passwordFile = '/no-permissions-here'
        with self.assertRaises(OverTheWire.OTWException):
            level.savePassword("spam")
