#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 22:31:42 2020

@author: Lucs1590
"""

import datetime
import hashlib
import json
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, Response, request


class EndpointAction:

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.response.data = self.action()
        return self.response


class FlaskAppWrapper:
    app = None

    def __init__(self, name):
        self.app = Flask(name)

    def run(self):
        self.app.run(
            host="0.0.0.0",
            port=5001
        )

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))


class Requests:
    def __init__(self):
        self.blockchain = Blockchain()
        self.node_address = str(uuid4()).replace("-", "")

    def mine_block(self):
        prev_block = self.blockchain.get_prev_block()
        proff = self.blockchain.proof_of_work(prev_block["proof"])
        prev_hash = self.blockchain.hash(prev_block)

        self.blockchain.add_transaction(
            sender=self.node_address,
            receiver="Lucs1590",
            amount=1
        )

        block = self.blockchain.create_block(proff, prev_hash)

        response = {
            "message": "Mined block!",
            "index": block["index"],
            "timestamp": block["timestamp"],
            "proof": block["proof"],
            "prev_hash": block["prev_hash"],
            "transactions": block["transactions"]
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

    def add_transaction(self):
        json_request = request.get_json()
        transaction_keys = ["sender", "receiver", "amount"]
        if not all(key in json_request for key in transaction_keys):
            response = "Missing keys"
        else:
            index = self.blockchain.add_transaction(
                json_request["sender"],
                json_request["receiver"],
                json_request["amount"]
            )
            response = {
                "message": f"This transaction will be added to block {index}"
            }
        return json.dumps(response)

    def connect_node(self):
        json_request = request.get_json()
        nodes = json_request.get("nodes")
        if nodes is None:
            response = "No node"
        for node in nodes:
            self.blockchain.add_node(node)
        response = {
            "message": "All nodes connected",
            "total_nodes": list(self.blockchain.node)
        }
        return json.dumps(response)

    def replace_chain(self):
        is_chain_replaced = self.blockchain.replace_chain()
        response = {
            "chain": self.blockchain.chain
        }
        response["message"] = "Chain replaced" if is_chain_replaced else "Chain not replaced"
        return json.dumps(response)


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(1, "0")
        self.node = set()

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

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        })
        prev_block = self.get_prev_block()
        return prev_block["index"] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.node.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.node
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            response = requests.get(f"http://{node}/get_chain")
            if response.status_code == 200:
                length = response.json()["lenght"]
                chain = response.json()["chain"]
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True
        return False


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
    flask_wrapper.add_endpoint(
        endpoint='/add_transaction',
        endpoint_name='add_transaction',
        handler=request_service.add_transaction
    )
    flask_wrapper.add_endpoint(
        endpoint='/connect_node',
        endpoint_name='connect_node',
        handler=request_service.connect_node
    )
    flask_wrapper.add_endpoint(
        endpoint='/replace_chain',
        endpoint_name='replace_chain',
        handler=request_service.replace_chain
    )
    flask_wrapper.run()


if __name__ == "__main__":
    main()
