#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 22:31:42 2020

@author: Lucs1590
"""

import datetime
import hashlib
import json
from flask import Flask, Response, jsonify


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.create_block(1, "0")

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

    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False

        while check_proof == False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - prev_proof**2)).hexdigest()

            (check_proof, new_proof) = (
                True, new_proof) if hash_operation[:4] == "0000" else (False, new_proof + 1)

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        prev_block = chain[0]
        i = 1
        while i < len(chain):
            curr_block = chain[i]
            if curr_block["prev_hash"] != self.hash(prev_block):
                return False

            hash_operation = hashlib.sha256(
                str(curr_block["proof"]**2 - prev_block["proof"]**2).encode()).hexdigest()

            if hash_operation[:4] != "0000":
                return False

            prev_block = curr_block
            i += 1
        return True


class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response


class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)

    def run(self):
        self.app.run()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))


def main():
    flask_wrapper = FlaskAppWrapper(__name__)
    flask_wrapper.add_endpoint(
        endpoint='/ad', endpoint_name='ad')
    flask_wrapper.run()
    bc = Blockchain()


if __name__ == "__main__":
    main()
