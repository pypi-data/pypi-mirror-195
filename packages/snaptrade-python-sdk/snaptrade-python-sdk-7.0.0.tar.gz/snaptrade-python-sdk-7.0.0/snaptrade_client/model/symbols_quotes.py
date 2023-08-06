# coding: utf-8

"""
    SnapTrade

    Connect brokerage accounts to your app for live positions and trading  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: api@snaptrade.com
    Generated by: https://konfigthis.com
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from snaptrade_client import schemas  # noqa: F401


class SymbolsQuotes(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by Konfig.
    Ref: https://konfigthis.com

    Do not edit the class manually.

    Symbols and Tickers Quotes object
    """


    class MetaOapg:
        
        class properties:
        
            @staticmethod
            def symbol() -> typing.Type['UniversalSymbol']:
                return UniversalSymbol
            bid_price = schemas.NumberSchema
            ask_price = schemas.NumberSchema
            last_trade_price = schemas.NumberSchema
            bid_size = schemas.NumberSchema
            ask_size = schemas.NumberSchema
            __annotations__ = {
                "symbol": symbol,
                "bid_price": bid_price,
                "ask_price": ask_price,
                "last_trade_price": last_trade_price,
                "bid_size": bid_size,
                "ask_size": ask_size,
            }
        additional_properties = schemas.AnyTypeSchema
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["symbol"]) -> 'UniversalSymbol': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bid_price"]) -> MetaOapg.properties.bid_price: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["ask_price"]) -> MetaOapg.properties.ask_price: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_trade_price"]) -> MetaOapg.properties.last_trade_price: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bid_size"]) -> MetaOapg.properties.bid_size: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["ask_size"]) -> MetaOapg.properties.ask_size: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> MetaOapg.additional_properties: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["symbol"], typing_extensions.Literal["bid_price"], typing_extensions.Literal["ask_price"], typing_extensions.Literal["last_trade_price"], typing_extensions.Literal["bid_size"], typing_extensions.Literal["ask_size"], str, ]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["symbol"]) -> typing.Union['UniversalSymbol', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bid_price"]) -> typing.Union[MetaOapg.properties.bid_price, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["ask_price"]) -> typing.Union[MetaOapg.properties.ask_price, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_trade_price"]) -> typing.Union[MetaOapg.properties.last_trade_price, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bid_size"]) -> typing.Union[MetaOapg.properties.bid_size, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["ask_size"]) -> typing.Union[MetaOapg.properties.ask_size, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[MetaOapg.additional_properties, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["symbol"], typing_extensions.Literal["bid_price"], typing_extensions.Literal["ask_price"], typing_extensions.Literal["last_trade_price"], typing_extensions.Literal["bid_size"], typing_extensions.Literal["ask_size"], str, ]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        symbol: typing.Union['UniversalSymbol', schemas.Unset] = schemas.unset,
        bid_price: typing.Union[MetaOapg.properties.bid_price, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        ask_price: typing.Union[MetaOapg.properties.ask_price, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        last_trade_price: typing.Union[MetaOapg.properties.last_trade_price, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        bid_size: typing.Union[MetaOapg.properties.bid_size, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        ask_size: typing.Union[MetaOapg.properties.ask_size, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[MetaOapg.additional_properties, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
    ) -> 'SymbolsQuotes':
        return super().__new__(
            cls,
            *args,
            symbol=symbol,
            bid_price=bid_price,
            ask_price=ask_price,
            last_trade_price=last_trade_price,
            bid_size=bid_size,
            ask_size=ask_size,
            _configuration=_configuration,
            **kwargs,
        )

from snaptrade_client.model.universal_symbol import UniversalSymbol
