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
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "prev_hash": prev_hash
        }
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return self.chain[-1]


def main():
    bc = Blockchain()
    bc.create_block(1, "0")


if __name__ == "__main__":
    main()
