#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 22:31:42 2020

@author: Lucs1590
"""

import datetime
import hashlib
import json
from flask import Flask, jsonify


class Blockchain(object):
    def __init__(self):
        self.chain = []

    def create_block(self, proof, prev_hash):
        ...


def main():
    bc = Blockchain()
    bc.create_block(1, "0")


if __name__ == "__main__":
    main()
