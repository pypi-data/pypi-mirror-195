"""
    SnapTrade

    Connect brokerage accounts to your app for live positions and trading  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: api@snaptrade.com
    Generated by: https://konfigthis.com
"""


import os
import unittest
import uuid
from pprint import pprint
from snaptrade_client import SnapTrade


class TestGettingStarted(unittest.TestCase):
    """AccountHoldings unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGettingStarted(self):
        # 1) Initialize a client with your clientID and consumerKey.
        snaptrade = SnapTrade(
            consumer_key=os.environ['SNAPTRADE_CONSUMER_KEY'],
            client_id=os.environ["SNAPTRADE_CLIENT_ID"]
        )

        # 2) Check that the client is able to make a request to the API server.
        api_response = snaptrade.api_status.check()
        pprint(api_response.body)

        # 3) Create a new user on SnapTrade
        user_id = str(uuid.uuid4())
        register_response = snaptrade.authentication.register_snap_trade_user(body={"userId": user_id})
        pprint(register_response.body)

        # Note: A user secret is only generated once. It's required to access
        # resources for certain endpoints.
        user_secret = register_response.body["userSecret"]

        # 4) Get a redirect URI. Users will need this to connect
        # their brokerage to the SnapTrade server.
        redirect_uri = snaptrade.authentication.login_snap_trade_user(query_params={"userId": user_id, "userSecret": user_secret})
        print(redirect_uri.body)

        snaptrade.portfolio_management.create(query_params={"userId": user_id, "userSecret": user_secret}, body={"id": str(uuid.uuid4()), "name": "MyPortfolio"})
        res = snaptrade.portfolio_management.list(query_params={"userId": user_id, "userSecret": user_secret})
        pprint(res.body)

        snaptrade.api_disclaimer.accept(query_params={"userId": user_id, "userSecret": user_secret}, body={"accepted": True})

        # 5) Obtaining account holdings data
        holdings = snaptrade.account_information.get_all_user_holdings(query_params={"userId": user_id, "userSecret": user_secret})
        pprint(holdings.body)

        # 6) Deleting a user
        deleted_response = snaptrade.authentication.delete_snap_trade_user(query_params={"userId": user_id})
        pprint(deleted_response.body)
    
    def test_get_user_account_balance(self):
        snaptrade = SnapTrade(
            consumer_key=os.environ['SNAPTRADE_CONSUMER_KEY'],
            client_id=os.environ["SNAPTRADE_CLIENT_ID"]
        )
        user_id = os.environ["SNAPTRADE_TEST_USER_ID"]
        user_secret = os.environ["SNAPTRADE_TEST_USER_SECRET"]
        accounts = snaptrade.account_information.list_user_accounts(query_params={"userId": user_id, "userSecret": user_secret})
        response = snaptrade.account_information.get_user_account_balance(
            path_params = {
                'accountId': accounts.body[0]["id"],
            },
            query_params = {
                'userId': user_id,
                'userSecret': user_secret,
            },
        )
        pprint(response.body)

    def test_get_user_holdings(self):
        snaptrade = SnapTrade(
            consumer_key=os.environ['SNAPTRADE_CONSUMER_KEY'],
            client_id=os.environ["SNAPTRADE_CLIENT_ID"]
        )
        user_id = os.environ["SNAPTRADE_TEST_USER_ID"]
        user_secret = os.environ["SNAPTRADE_TEST_USER_SECRET"]
        accounts = snaptrade.account_information.list_user_accounts(query_params={"userId": user_id, "userSecret": user_secret})
        account_id = accounts.body[0]["id"]
        holdings = snaptrade.account_information.get_user_holdings(query_params={"userId": user_id, "userSecret": user_secret}, path_params={"accountId": account_id})
        pprint(holdings)

    @unittest.skip(reason="getting 500 internal server error")
    def test_get_options_chain(self):
        
        snaptrade = SnapTrade(
            consumer_key=os.environ['SNAPTRADE_CONSUMER_KEY'],
            client_id=os.environ["SNAPTRADE_CLIENT_ID"]
        )
        user_id = os.environ["SNAPTRADE_TEST_USER_ID"]
        user_secret = os.environ["SNAPTRADE_TEST_USER_SECRET"]
        accounts = snaptrade.account_information.list_user_accounts(query_params={"userId": user_id, "userSecret": user_secret})
        account_id = accounts.body[0]["id"]
        symbols = snaptrade.reference_data.get_symbols(body={"substring": "apple"})
        symbol_id = symbols.body[0]["id"]
        options_chain = snaptrade.options.get_options_chain(query_params={"userId": user_id, "userSecret": user_secret, "symbol": symbol_id}, path_params={"accountId": account_id})
        pprint(options_chain)


if __name__ == '__main__':
    unittest.main()
