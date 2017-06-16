#!/usr/bin/env python

import unittest

import OverTheWire

class TestOTWLevelKnown(unittest.TestCase):
    def setUp(self):
        self.level = OverTheWire.OTWLevel("bandit", 0)

    def test_otw_level_attrbutes(self):
        self.assertEqual(self.level.levelNumber, 0)
        self.assertEqual(self.level.levelName, "bandit0")
        for k in ["domain", "port"]:
            self.assertTrue(k in self.level.config)

    def test_otw_level_sync_password(self):
        self.level.savePassword('spam')
        password = self.level.loadPassword()
        self.assertEqual(password, 'spam')

    def test_otw_level_connectionCommand(self):
        self.level.savePassword('spam')
        command = self.level.connectionCommand()
        self.assertEqual(command, 'sshpass -p spam ssh -o StrictHostKeyChecking=no -p 2220 bandit0@bandit.labs.overthewire.org')

    def tearDown(self):
        self.level.savePassword("bandit0")
