#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 22:31:42 2020

@author: Lucs1590
"""

import datetime
import hashlib
import json
import requests

from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, Response, request


class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.response.data = self.action()
        return self.response


class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)

    def run(self):
        self.app.run()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))


class Requests(object):
    def __init__(self):
        self.blockchain = Blockchain()

    def mine_block(self):
        prev_block = self.blockchain.get_prev_block()
        proff = self.blockchain.proof_of_work(prev_block["proof"])
        prev_hash = self.blockchain.hash(prev_block)

        block = self.blockchain.create_block(proff, prev_hash)

        response = {
            "message": "Mined block!",
            "index": block["index"],
            "timestamp": block["timestamp"],
            "proof": block["proof"],
            "prev_hash": block["prev_hash"]
        }

        return json.dumps(response)

    def get_chain(self):
        response = {
            "chain": self.blockchain.chain,
            "lenght": len(self.blockchain.chain)
        }
        return json.dumps(response)

    def is_valid(self):
        response = {"message": "block valid!"} if self.blockchain.is_chain_valid(
            self.blockchain.chain) else {"message": "block invalid!"}
        return json.dumps(response)


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(1, "0")

    def create_block(self, proof, prev_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "prev_hash": prev_hash,
            "transactions": self.transactions
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return self.chain[-1]

    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - prev_proof**2).encode()).hexdigest()

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

    def add_transaction(self, sender, reciver, amount):
        self.transactions.append({
            "sender": sender,
            "reciver": reciver,
            "amount": amount
        })
        prev_block = self.get_prev_block()
        return prev_block["index"] + 1


def main():
    flask_wrapper = FlaskAppWrapper(__name__)
    request_service = Requests()

    flask_wrapper.add_endpoint(
        endpoint='/mine_block',
        endpoint_name='mine_block',
        handler=request_service.mine_block
    )
    flask_wrapper.add_endpoint(
        endpoint='/get_chain',
        endpoint_name='get_chain',
        handler=request_service.get_chain
    )
    flask_wrapper.add_endpoint(
        endpoint='/is_valid',
        endpoint_name='is_valid',
        handler=request_service.is_valid
    )
    flask_wrapper.run()


if __name__ == "__main__":
    main()
