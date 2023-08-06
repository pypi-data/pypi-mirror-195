# coding: utf-8

"""
    SnapTrade

    Connect brokerage accounts to your app for live positions and trading  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: api@snaptrade.com
    Generated by: https://konfigthis.com
"""

from snaptrade_client.paths.snap_trade_delete_user.delete import DeleteSnapTradeUser
from snaptrade_client.paths.snap_trade_encrypted_jwt.get import GetUserJwt
from snaptrade_client.paths.snap_trade_list_users.get import ListSnapTradeUsers
from snaptrade_client.paths.snap_trade_login.post import LoginSnapTradeUser
from snaptrade_client.paths.snap_trade_register_user.post import RegisterSnapTradeUser


class AuthenticationApi(
    DeleteSnapTradeUser,
    GetUserJwt,
    ListSnapTradeUsers,
    LoginSnapTradeUser,
    RegisterSnapTradeUser,
):
    """NOTE: This class is auto generated by Konfig
    Ref: https://konfgithis.com

    Do not edit the class manually.
    """
    pass
