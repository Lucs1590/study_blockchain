# DripsCoin
This is an network to simulate the transactions, mineration and other features of a cryptocurrency, for example, the replacement of chain when it is unupdated.

## How to run
To run the network, you need to install the dependencies first. You can do it by running the following command:
```
pip install -r requirements.txt
```
Because we will work with network interaction, you need to install a tool to make the requests. We recommend you to use Postman, but you can use any other tool that you want.

After that, you can run the network, but to simulate the sincronization of the network, you need to run the following command in three different terminals:
```
python3 dripscoin.py
python3 dripscoin1.py
python3 dripscoin2.py
```

## Note
In this project we will use the port 5000, 5001 and 5002, so you need to make sure that these ports are not being used by other applications.
Another thing that you need to know is that the network will be running in the localhost, so you can't run the network in different computers.
Thus, it's important to say that we use FlaskWrapper to organize the code, so you can use only GET methods.

## Requests order
1. /get_chain
2. /connect_node (for each node and with nodes.json as body)
3. /add_transaction (with transaction.json as body)
4. /mine_block
5. /get_chain
6. /replace_chain (for each node)
7. /get_chain