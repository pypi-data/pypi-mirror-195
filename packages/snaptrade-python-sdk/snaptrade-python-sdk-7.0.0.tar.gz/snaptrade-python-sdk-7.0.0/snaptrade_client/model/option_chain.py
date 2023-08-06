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


class OptionChain(
    schemas.ListSchema
):
    """NOTE: This class is auto generated by Konfig.
    Ref: https://konfigthis.com

    Do not edit the class manually.

    chain of options
    """


    class MetaOapg:
        
        
        class items(
            schemas.DictSchema
        ):
        
        
            class MetaOapg:
                
                class properties:
                    expiryDate = schemas.StrSchema
                    description = schemas.StrSchema
                    listingExchange = schemas.StrSchema
                    optionExerciseType = schemas.StrSchema
                    
                    
                    class chainPerRoot(
                        schemas.ListSchema
                    ):
                    
                    
                        class MetaOapg:
                            
                            
                            class items(
                                schemas.DictSchema
                            ):
                            
                            
                                class MetaOapg:
                                    
                                    class properties:
                                        optionRoot = schemas.StrSchema
                                        
                                        
                                        class chainPerStrikePrice(
                                            schemas.ListSchema
                                        ):
                                        
                                        
                                            class MetaOapg:
                                                
                                                
                                                class items(
                                                    schemas.DictSchema
                                                ):
                                                
                                                
                                                    class MetaOapg:
                                                        
                                                        class properties:
                                                            
                                                            
                                                            class strikePrice(
                                                                schemas.Int32Base,
                                                                schemas.IntBase,
                                                                schemas.NoneBase,
                                                                schemas.Schema,
                                                                schemas.NoneDecimalMixin
                                                            ):
                                                            
                                                            
                                                                class MetaOapg:
                                                                    format = 'int32'
                                                            
                                                            
                                                                def __new__(
                                                                    cls,
                                                                    *args: typing.Union[None, decimal.Decimal, int, ],
                                                                    _configuration: typing.Optional[schemas.Configuration] = None,
                                                                ) -> 'strikePrice':
                                                                    return super().__new__(
                                                                        cls,
                                                                        *args,
                                                                        _configuration=_configuration,
                                                                    )
                                                            
                                                            
                                                            class callSymbolId(
                                                                schemas.Int32Base,
                                                                schemas.IntBase,
                                                                schemas.NoneBase,
                                                                schemas.Schema,
                                                                schemas.NoneDecimalMixin
                                                            ):
                                                            
                                                            
                                                                class MetaOapg:
                                                                    format = 'int32'
                                                            
                                                            
                                                                def __new__(
                                                                    cls,
                                                                    *args: typing.Union[None, decimal.Decimal, int, ],
                                                                    _configuration: typing.Optional[schemas.Configuration] = None,
                                                                ) -> 'callSymbolId':
                                                                    return super().__new__(
                                                                        cls,
                                                                        *args,
                                                                        _configuration=_configuration,
                                                                    )
                                                            
                                                            
                                                            class putSymbolId(
                                                                schemas.Int32Base,
                                                                schemas.IntBase,
                                                                schemas.NoneBase,
                                                                schemas.Schema,
                                                                schemas.NoneDecimalMixin
                                                            ):
                                                            
                                                            
                                                                class MetaOapg:
                                                                    format = 'int32'
                                                            
                                                            
                                                                def __new__(
                                                                    cls,
                                                                    *args: typing.Union[None, decimal.Decimal, int, ],
                                                                    _configuration: typing.Optional[schemas.Configuration] = None,
                                                                ) -> 'putSymbolId':
                                                                    return super().__new__(
                                                                        cls,
                                                                        *args,
                                                                        _configuration=_configuration,
                                                                    )
                                                            __annotations__ = {
                                                                "strikePrice": strikePrice,
                                                                "callSymbolId": callSymbolId,
                                                                "putSymbolId": putSymbolId,
                                                            }
                                                        additional_properties = schemas.AnyTypeSchema
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: typing_extensions.Literal["strikePrice"]) -> MetaOapg.properties.strikePrice: ...
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: typing_extensions.Literal["callSymbolId"]) -> MetaOapg.properties.callSymbolId: ...
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: typing_extensions.Literal["putSymbolId"]) -> MetaOapg.properties.putSymbolId: ...
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: str) -> MetaOapg.additional_properties: ...
                                                    
                                                    def __getitem__(self, name: typing.Union[typing_extensions.Literal["strikePrice"], typing_extensions.Literal["callSymbolId"], typing_extensions.Literal["putSymbolId"], str, ]):
                                                        # dict_instance[name] accessor
                                                        return super().__getitem__(name)
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: typing_extensions.Literal["strikePrice"]) -> typing.Union[MetaOapg.properties.strikePrice, schemas.Unset]: ...
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: typing_extensions.Literal["callSymbolId"]) -> typing.Union[MetaOapg.properties.callSymbolId, schemas.Unset]: ...
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: typing_extensions.Literal["putSymbolId"]) -> typing.Union[MetaOapg.properties.putSymbolId, schemas.Unset]: ...
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: str) -> typing.Union[MetaOapg.additional_properties, schemas.Unset]: ...
                                                    
                                                    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["strikePrice"], typing_extensions.Literal["callSymbolId"], typing_extensions.Literal["putSymbolId"], str, ]):
                                                        return super().get_item_oapg(name)
                                                
                                                    def __new__(
                                                        cls,
                                                        *args: typing.Union[dict, frozendict.frozendict, ],
                                                        strikePrice: typing.Union[MetaOapg.properties.strikePrice, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                                                        callSymbolId: typing.Union[MetaOapg.properties.callSymbolId, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                                                        putSymbolId: typing.Union[MetaOapg.properties.putSymbolId, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                                                        _configuration: typing.Optional[schemas.Configuration] = None,
                                                        **kwargs: typing.Union[MetaOapg.additional_properties, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                                                    ) -> 'items':
                                                        return super().__new__(
                                                            cls,
                                                            *args,
                                                            strikePrice=strikePrice,
                                                            callSymbolId=callSymbolId,
                                                            putSymbolId=putSymbolId,
                                                            _configuration=_configuration,
                                                            **kwargs,
                                                        )
                                        
                                            def __new__(
                                                cls,
                                                arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]], typing.List[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]]],
                                                _configuration: typing.Optional[schemas.Configuration] = None,
                                            ) -> 'chainPerStrikePrice':
                                                return super().__new__(
                                                    cls,
                                                    arg,
                                                    _configuration=_configuration,
                                                )
                                        
                                            def __getitem__(self, i: int) -> MetaOapg.items:
                                                return super().__getitem__(i)
                                        multiplier = schemas.Int32Schema
                                        __annotations__ = {
                                            "optionRoot": optionRoot,
                                            "chainPerStrikePrice": chainPerStrikePrice,
                                            "multiplier": multiplier,
                                        }
                                    additional_properties = schemas.AnyTypeSchema
                                
                                @typing.overload
                                def __getitem__(self, name: typing_extensions.Literal["optionRoot"]) -> MetaOapg.properties.optionRoot: ...
                                
                                @typing.overload
                                def __getitem__(self, name: typing_extensions.Literal["chainPerStrikePrice"]) -> MetaOapg.properties.chainPerStrikePrice: ...
                                
                                @typing.overload
                                def __getitem__(self, name: typing_extensions.Literal["multiplier"]) -> MetaOapg.properties.multiplier: ...
                                
                                @typing.overload
                                def __getitem__(self, name: str) -> MetaOapg.additional_properties: ...
                                
                                def __getitem__(self, name: typing.Union[typing_extensions.Literal["optionRoot"], typing_extensions.Literal["chainPerStrikePrice"], typing_extensions.Literal["multiplier"], str, ]):
                                    # dict_instance[name] accessor
                                    return super().__getitem__(name)
                                
                                @typing.overload
                                def get_item_oapg(self, name: typing_extensions.Literal["optionRoot"]) -> typing.Union[MetaOapg.properties.optionRoot, schemas.Unset]: ...
                                
                                @typing.overload
                                def get_item_oapg(self, name: typing_extensions.Literal["chainPerStrikePrice"]) -> typing.Union[MetaOapg.properties.chainPerStrikePrice, schemas.Unset]: ...
                                
                                @typing.overload
                                def get_item_oapg(self, name: typing_extensions.Literal["multiplier"]) -> typing.Union[MetaOapg.properties.multiplier, schemas.Unset]: ...
                                
                                @typing.overload
                                def get_item_oapg(self, name: str) -> typing.Union[MetaOapg.additional_properties, schemas.Unset]: ...
                                
                                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["optionRoot"], typing_extensions.Literal["chainPerStrikePrice"], typing_extensions.Literal["multiplier"], str, ]):
                                    return super().get_item_oapg(name)
                            
                                def __new__(
                                    cls,
                                    *args: typing.Union[dict, frozendict.frozendict, ],
                                    optionRoot: typing.Union[MetaOapg.properties.optionRoot, str, schemas.Unset] = schemas.unset,
                                    chainPerStrikePrice: typing.Union[MetaOapg.properties.chainPerStrikePrice, list, tuple, schemas.Unset] = schemas.unset,
                                    multiplier: typing.Union[MetaOapg.properties.multiplier, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                                    _configuration: typing.Optional[schemas.Configuration] = None,
                                    **kwargs: typing.Union[MetaOapg.additional_properties, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                                ) -> 'items':
                                    return super().__new__(
                                        cls,
                                        *args,
                                        optionRoot=optionRoot,
                                        chainPerStrikePrice=chainPerStrikePrice,
                                        multiplier=multiplier,
                                        _configuration=_configuration,
                                        **kwargs,
                                    )
                    
                        def __new__(
                            cls,
                            arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]], typing.List[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]]],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                        ) -> 'chainPerRoot':
                            return super().__new__(
                                cls,
                                arg,
                                _configuration=_configuration,
                            )
                    
                        def __getitem__(self, i: int) -> MetaOapg.items:
                            return super().__getitem__(i)
                    __annotations__ = {
                        "expiryDate": expiryDate,
                        "description": description,
                        "listingExchange": listingExchange,
                        "optionExerciseType": optionExerciseType,
                        "chainPerRoot": chainPerRoot,
                    }
                additional_properties = schemas.AnyTypeSchema
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["expiryDate"]) -> MetaOapg.properties.expiryDate: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["listingExchange"]) -> MetaOapg.properties.listingExchange: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["optionExerciseType"]) -> MetaOapg.properties.optionExerciseType: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["chainPerRoot"]) -> MetaOapg.properties.chainPerRoot: ...
            
            @typing.overload
            def __getitem__(self, name: str) -> MetaOapg.additional_properties: ...
            
            def __getitem__(self, name: typing.Union[typing_extensions.Literal["expiryDate"], typing_extensions.Literal["description"], typing_extensions.Literal["listingExchange"], typing_extensions.Literal["optionExerciseType"], typing_extensions.Literal["chainPerRoot"], str, ]):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["expiryDate"]) -> typing.Union[MetaOapg.properties.expiryDate, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["listingExchange"]) -> typing.Union[MetaOapg.properties.listingExchange, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["optionExerciseType"]) -> typing.Union[MetaOapg.properties.optionExerciseType, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["chainPerRoot"]) -> typing.Union[MetaOapg.properties.chainPerRoot, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: str) -> typing.Union[MetaOapg.additional_properties, schemas.Unset]: ...
            
            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["expiryDate"], typing_extensions.Literal["description"], typing_extensions.Literal["listingExchange"], typing_extensions.Literal["optionExerciseType"], typing_extensions.Literal["chainPerRoot"], str, ]):
                return super().get_item_oapg(name)
        
            def __new__(
                cls,
                *args: typing.Union[dict, frozendict.frozendict, ],
                expiryDate: typing.Union[MetaOapg.properties.expiryDate, str, schemas.Unset] = schemas.unset,
                description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
                listingExchange: typing.Union[MetaOapg.properties.listingExchange, str, schemas.Unset] = schemas.unset,
                optionExerciseType: typing.Union[MetaOapg.properties.optionExerciseType, str, schemas.Unset] = schemas.unset,
                chainPerRoot: typing.Union[MetaOapg.properties.chainPerRoot, list, tuple, schemas.Unset] = schemas.unset,
                _configuration: typing.Optional[schemas.Configuration] = None,
                **kwargs: typing.Union[MetaOapg.additional_properties, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
            ) -> 'items':
                return super().__new__(
                    cls,
                    *args,
                    expiryDate=expiryDate,
                    description=description,
                    listingExchange=listingExchange,
                    optionExerciseType=optionExerciseType,
                    chainPerRoot=chainPerRoot,
                    _configuration=_configuration,
                    **kwargs,
                )

    def __new__(
        cls,
        arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]], typing.List[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]]],
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'OptionChain':
        return super().__new__(
            cls,
            arg,
            _configuration=_configuration,
        )

    def __getitem__(self, i: int) -> MetaOapg.items:
        return super().__getitem__(i)
