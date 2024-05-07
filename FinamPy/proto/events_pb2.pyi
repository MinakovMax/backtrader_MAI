"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import FinamPy.proto.common_pb2
import FinamPy.proto.orders_pb2
import FinamPy.proto.portfolios_pb2
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class TimeFrame(google.protobuf.message.Message):
    """Timeframe.
    Таймфрейм.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Unit:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _UnitEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[TimeFrame._Unit.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        UNIT_UNSPECIFIED: TimeFrame._Unit.ValueType  # 0
        """Value is not specified. Do not use.
        Значение не указано. Не использовать.
        """
        UNIT_MINUTE: TimeFrame._Unit.ValueType  # 1
        """Munute.
        Минута.
        """
        UNIT_HOUR: TimeFrame._Unit.ValueType  # 2
        """Hour.
        Час.
        """
        UNIT_DAY: TimeFrame._Unit.ValueType  # 3
        """Day.
        День.
        """
        UNIT_WEEK: TimeFrame._Unit.ValueType  # 4
        """Week.
        Неделя.
        """
        UNIT_MONTH: TimeFrame._Unit.ValueType  # 5
        """Month.
        Месяц.
        """
        UNIT_QUARTER: TimeFrame._Unit.ValueType  # 6
        """Quarter.
        Квартал.
        """
        UNIT_YEAR: TimeFrame._Unit.ValueType  # 7
        """Year.
        Год.
        """

    class Unit(_Unit, metaclass=_UnitEnumTypeWrapper): ...
    UNIT_UNSPECIFIED: TimeFrame.Unit.ValueType  # 0
    """Value is not specified. Do not use.
    Значение не указано. Не использовать.
    """
    UNIT_MINUTE: TimeFrame.Unit.ValueType  # 1
    """Munute.
    Минута.
    """
    UNIT_HOUR: TimeFrame.Unit.ValueType  # 2
    """Hour.
    Час.
    """
    UNIT_DAY: TimeFrame.Unit.ValueType  # 3
    """Day.
    День.
    """
    UNIT_WEEK: TimeFrame.Unit.ValueType  # 4
    """Week.
    Неделя.
    """
    UNIT_MONTH: TimeFrame.Unit.ValueType  # 5
    """Month.
    Месяц.
    """
    UNIT_QUARTER: TimeFrame.Unit.ValueType  # 6
    """Quarter.
    Квартал.
    """
    UNIT_YEAR: TimeFrame.Unit.ValueType  # 7
    """Year.
    Год.
    """

    TIME_UNIT_FIELD_NUMBER: builtins.int
    time_unit: global___TimeFrame.Unit.ValueType
    """Timeframe units.
    Единицы измерения таймфрейма.
    """
    def __init__(
        self,
        *,
        time_unit: global___TimeFrame.Unit.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["time_unit", b"time_unit"]) -> None: ...

global___TimeFrame = TimeFrame

@typing.final
class SubscriptionRequest(google.protobuf.message.Message):
    """Subscription/unsubscription.
    Подписка/отписка.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ORDER_BOOK_SUBSCRIBE_REQUEST_FIELD_NUMBER: builtins.int
    ORDER_BOOK_UNSUBSCRIBE_REQUEST_FIELD_NUMBER: builtins.int
    ORDER_TRADE_SUBSCRIBE_REQUEST_FIELD_NUMBER: builtins.int
    ORDER_TRADE_UNSUBSCRIBE_REQUEST_FIELD_NUMBER: builtins.int
    KEEP_ALIVE_REQUEST_FIELD_NUMBER: builtins.int
    @property
    def order_book_subscribe_request(self) -> global___OrderBookSubscribeRequest:
        """OrderBook subscription request.
        Запрос подписки на стакан.
        """

    @property
    def order_book_unsubscribe_request(self) -> global___OrderBookUnsubscribeRequest:
        """OrderBook unsubscribe request.
        Запрос на отписку от стакана.
        """

    @property
    def order_trade_subscribe_request(self) -> global___OrderTradeSubscribeRequest:
        """Subscribe for trades and orders.
        Запрос подписки на ордера и сделки.
        """

    @property
    def order_trade_unsubscribe_request(self) -> global___OrderTradeUnsubscribeRequest:
        """Cancel all previous subscription for trades and orders.
        Отменить все предыдущие запросы на подписки на ордера и сделки.
        """

    @property
    def keep_alive_request(self) -> global___KeepAliveRequest:
        """Keep-alive request.
        Keep-alive запрос.
        """

    def __init__(
        self,
        *,
        order_book_subscribe_request: global___OrderBookSubscribeRequest | None = ...,
        order_book_unsubscribe_request: global___OrderBookUnsubscribeRequest | None = ...,
        order_trade_subscribe_request: global___OrderTradeSubscribeRequest | None = ...,
        order_trade_unsubscribe_request: global___OrderTradeUnsubscribeRequest | None = ...,
        keep_alive_request: global___KeepAliveRequest | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["keep_alive_request", b"keep_alive_request", "order_book_subscribe_request", b"order_book_subscribe_request", "order_book_unsubscribe_request", b"order_book_unsubscribe_request", "order_trade_subscribe_request", b"order_trade_subscribe_request", "order_trade_unsubscribe_request", b"order_trade_unsubscribe_request", "payload", b"payload"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["keep_alive_request", b"keep_alive_request", "order_book_subscribe_request", b"order_book_subscribe_request", "order_book_unsubscribe_request", b"order_book_unsubscribe_request", "order_trade_subscribe_request", b"order_trade_subscribe_request", "order_trade_unsubscribe_request", b"order_trade_unsubscribe_request", "payload", b"payload"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["payload", b"payload"]) -> typing.Literal["order_book_subscribe_request", "order_book_unsubscribe_request", "order_trade_subscribe_request", "order_trade_unsubscribe_request", "keep_alive_request"] | None: ...

global___SubscriptionRequest = SubscriptionRequest

@typing.final
class Event(google.protobuf.message.Message):
    """Event.
    Событие.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ORDER_FIELD_NUMBER: builtins.int
    TRADE_FIELD_NUMBER: builtins.int
    ORDER_BOOK_FIELD_NUMBER: builtins.int
    PORTFOLIO_FIELD_NUMBER: builtins.int
    RESPONSE_FIELD_NUMBER: builtins.int
    @property
    def order(self) -> global___OrderEvent:
        """Order event.
        Событие с заявкой.
        """

    @property
    def trade(self) -> global___TradeEvent:
        """Trade event.
        Событие со сделкой.
        """

    @property
    def order_book(self) -> global___OrderBookEvent:
        """OrderBook event.
        Событие стакана.
        """

    @property
    def portfolio(self) -> global___PortfolioEvent:
        """Portfolio event.
        Событие портфеля.
        """

    @property
    def response(self) -> FinamPy.proto.common_pb2.ResponseEvent:
        """Request execution result.
        Результат выполнения запроса.
        """

    def __init__(
        self,
        *,
        order: global___OrderEvent | None = ...,
        trade: global___TradeEvent | None = ...,
        order_book: global___OrderBookEvent | None = ...,
        portfolio: global___PortfolioEvent | None = ...,
        response: FinamPy.proto.common_pb2.ResponseEvent | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["order", b"order", "order_book", b"order_book", "payload", b"payload", "portfolio", b"portfolio", "response", b"response", "trade", b"trade"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["order", b"order", "order_book", b"order_book", "payload", b"payload", "portfolio", b"portfolio", "response", b"response", "trade", b"trade"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["payload", b"payload"]) -> typing.Literal["order", "trade", "order_book", "portfolio", "response"] | None: ...

global___Event = Event

@typing.final
class OrderBookSubscribeRequest(google.protobuf.message.Message):
    """OrderBook subscribe request.
    Запрос подписки на стакан.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    REQUEST_ID_FIELD_NUMBER: builtins.int
    SECURITY_CODE_FIELD_NUMBER: builtins.int
    SECURITY_BOARD_FIELD_NUMBER: builtins.int
    request_id: builtins.str
    """Request ID.
    Идентификатор запроса.
    """
    security_code: builtins.str
    """Security Code.
    Тикер инструмента.
    """
    security_board: builtins.str
    """Trading Board.
    Режим торгов.
    """
    def __init__(
        self,
        *,
        request_id: builtins.str = ...,
        security_code: builtins.str = ...,
        security_board: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["request_id", b"request_id", "security_board", b"security_board", "security_code", b"security_code"]) -> None: ...

global___OrderBookSubscribeRequest = OrderBookSubscribeRequest

@typing.final
class OrderBookUnsubscribeRequest(google.protobuf.message.Message):
    """OrderBook unsubscribe request.
    Запрос на отписку от стакана.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    REQUEST_ID_FIELD_NUMBER: builtins.int
    SECURITY_CODE_FIELD_NUMBER: builtins.int
    SECURITY_BOARD_FIELD_NUMBER: builtins.int
    request_id: builtins.str
    """Request ID.
    Идентификатор запроса.
    """
    security_code: builtins.str
    """Security Code.
    Тикер инструмента.
    """
    security_board: builtins.str
    """Trading Board.
    Режим торгов.
    """
    def __init__(
        self,
        *,
        request_id: builtins.str = ...,
        security_code: builtins.str = ...,
        security_board: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["request_id", b"request_id", "security_board", b"security_board", "security_code", b"security_code"]) -> None: ...

global___OrderBookUnsubscribeRequest = OrderBookUnsubscribeRequest

@typing.final
class OrderTradeSubscribeRequest(google.protobuf.message.Message):
    """Subscribe for trades and orders.
    Запрос подписки на ордера и сделки.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    REQUEST_ID_FIELD_NUMBER: builtins.int
    INCLUDE_TRADES_FIELD_NUMBER: builtins.int
    INCLUDE_ORDERS_FIELD_NUMBER: builtins.int
    CLIENT_IDS_FIELD_NUMBER: builtins.int
    request_id: builtins.str
    """Request ID.
    Идентификатор запроса.
    """
    include_trades: builtins.bool
    """Включить сделки в подписку."""
    include_orders: builtins.bool
    """Включить заявки в подписку.
    Тикер инструмента.
    """
    @property
    def client_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Торговые коды счетов."""

    def __init__(
        self,
        *,
        request_id: builtins.str = ...,
        include_trades: builtins.bool = ...,
        include_orders: builtins.bool = ...,
        client_ids: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["client_ids", b"client_ids", "include_orders", b"include_orders", "include_trades", b"include_trades", "request_id", b"request_id"]) -> None: ...

global___OrderTradeSubscribeRequest = OrderTradeSubscribeRequest

@typing.final
class OrderTradeUnsubscribeRequest(google.protobuf.message.Message):
    """Cancel all previous subscription for trades and orders.
    Отменить все предыдущие запросы на подписки на ордера и сделки.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    REQUEST_ID_FIELD_NUMBER: builtins.int
    request_id: builtins.str
    """Request ID.
    Идентификатор запроса.
    """
    def __init__(
        self,
        *,
        request_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["request_id", b"request_id"]) -> None: ...

global___OrderTradeUnsubscribeRequest = OrderTradeUnsubscribeRequest

@typing.final
class PortfolioSubscription(google.protobuf.message.Message):
    """Portfolio subscription.
    Подписка на портфель.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLIENT_ID_FIELD_NUMBER: builtins.int
    CONTENT_FIELD_NUMBER: builtins.int
    client_id: builtins.str
    """Trade Account ID.
    Идентификатор торгового счёта.
    """
    @property
    def content(self) -> FinamPy.proto.portfolios_pb2.PortfolioContent:
        """What kind of data the response contains.
        Какие данные будут в ответе.
        """

    def __init__(
        self,
        *,
        client_id: builtins.str = ...,
        content: FinamPy.proto.portfolios_pb2.PortfolioContent | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["content", b"content"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["client_id", b"client_id", "content", b"content"]) -> None: ...

global___PortfolioSubscription = PortfolioSubscription

@typing.final
class OrderEvent(google.protobuf.message.Message):
    """Order event.
    Событие с заявкой.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ORDER_NO_FIELD_NUMBER: builtins.int
    TRANSACTION_ID_FIELD_NUMBER: builtins.int
    SECURITY_CODE_FIELD_NUMBER: builtins.int
    CLIENT_ID_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    BUY_SELL_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    PRICE_FIELD_NUMBER: builtins.int
    QUANTITY_FIELD_NUMBER: builtins.int
    BALANCE_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    CURRENCY_FIELD_NUMBER: builtins.int
    CONDITION_FIELD_NUMBER: builtins.int
    VALID_BEFORE_FIELD_NUMBER: builtins.int
    ACCEPTED_AT_FIELD_NUMBER: builtins.int
    order_no: builtins.int
    """Order No. Appear only when an order is placed in OrderBook.
    Биржевой номер заявки. Появляется после того, как заявка попадает в стакан.
    """
    transaction_id: builtins.int
    """Transaction Id . Assigned when a command for new order creation is sent.
    Идентификатор транзакции. Назначается после подачи команды на создание новой заявки.
    """
    security_code: builtins.str
    """Security Code.
    Тикер инструмента.
    """
    client_id: builtins.str
    """Trade Account ID.
    Идентификатор торгового счёта.
    """
    status: FinamPy.proto.orders_pb2.OrderStatus.ValueType
    """Order status.
    Состояние заявки.
    """
    buy_sell: FinamPy.proto.common_pb2.BuySell.ValueType
    """Transaction direction.
    Направление сделки.
    """
    price: builtins.float
    """Lot price.
    Цена за лот.
    """
    quantity: builtins.int
    """Volume in lots.
    Количество, в лотах.
    """
    balance: builtins.int
    """Residual volume in lots.
    Неисполненный остаток, в лотах.
    """
    message: builtins.str
    """Rejection reason or conditional order resolution.
    Причина отказа или вердикт по условной заявке.
    """
    currency: builtins.str
    """Price currency.
    Валюта цены инструмента.
    """
    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Time of Order placement in UTC.
        Время регистрации заявки на бирже. В UTC.
        """

    @property
    def condition(self) -> FinamPy.proto.orders_pb2.OrderCondition:
        """Conditional order properties.
        Параметры условной заявки.
        """

    @property
    def valid_before(self) -> FinamPy.proto.common_pb2.OrderValidBefore:
        """Order lifetime.
        Время действия заявки.
        """

    @property
    def accepted_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Time of order registration on the server in UTC.
        Время, когда заявка была зарегистрирована на сервере. В UTC.
        """

    def __init__(
        self,
        *,
        order_no: builtins.int = ...,
        transaction_id: builtins.int = ...,
        security_code: builtins.str = ...,
        client_id: builtins.str = ...,
        status: FinamPy.proto.orders_pb2.OrderStatus.ValueType = ...,
        buy_sell: FinamPy.proto.common_pb2.BuySell.ValueType = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        price: builtins.float = ...,
        quantity: builtins.int = ...,
        balance: builtins.int = ...,
        message: builtins.str = ...,
        currency: builtins.str = ...,
        condition: FinamPy.proto.orders_pb2.OrderCondition | None = ...,
        valid_before: FinamPy.proto.common_pb2.OrderValidBefore | None = ...,
        accepted_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["accepted_at", b"accepted_at", "condition", b"condition", "created_at", b"created_at", "valid_before", b"valid_before"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["accepted_at", b"accepted_at", "balance", b"balance", "buy_sell", b"buy_sell", "client_id", b"client_id", "condition", b"condition", "created_at", b"created_at", "currency", b"currency", "message", b"message", "order_no", b"order_no", "price", b"price", "quantity", b"quantity", "security_code", b"security_code", "status", b"status", "transaction_id", b"transaction_id", "valid_before", b"valid_before"]) -> None: ...

global___OrderEvent = OrderEvent

@typing.final
class TradeEvent(google.protobuf.message.Message):
    """Trade event.
    Событие со сделкой.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECURITY_CODE_FIELD_NUMBER: builtins.int
    TRADE_NO_FIELD_NUMBER: builtins.int
    ORDER_NO_FIELD_NUMBER: builtins.int
    CLIENT_ID_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    QUANTITY_FIELD_NUMBER: builtins.int
    PRICE_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    BUY_SELL_FIELD_NUMBER: builtins.int
    COMMISSION_FIELD_NUMBER: builtins.int
    CURRENCY_FIELD_NUMBER: builtins.int
    ACCRUED_INTEREST_FIELD_NUMBER: builtins.int
    security_code: builtins.str
    """Security Code.
    Тикер инструмента.
    """
    trade_no: builtins.int
    """Trade No.
    Номер сделки.
    """
    order_no: builtins.int
    """Order No.
    Номер заявки.
    """
    client_id: builtins.str
    """Trade Account ID.
    Идентификатор торгового счёта.
    """
    quantity: builtins.int
    """Volume in lots.
    Количество, в лотах.
    """
    price: builtins.float
    """Trade Price.
    Цена сделки.
    """
    value: builtins.float
    """Trade currency value.
    Объём сделки в валюте инструмента.
    """
    buy_sell: FinamPy.proto.common_pb2.BuySell.ValueType
    """Transaction direction.
    Направление сделки.
    """
    commission: builtins.float
    """Fee, RUB.
    Комиссия, в рублях.
    """
    currency: builtins.str
    """Trade currency.
    Валюта сделки.
    """
    accrued_interest: builtins.float
    """Accrued interest.
    НКД сделки.
    """
    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Time of trade registration on stock exchange in UTC.
        Время исполнения сделки на бирже. В UTC.
        """

    def __init__(
        self,
        *,
        security_code: builtins.str = ...,
        trade_no: builtins.int = ...,
        order_no: builtins.int = ...,
        client_id: builtins.str = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        quantity: builtins.int = ...,
        price: builtins.float = ...,
        value: builtins.float = ...,
        buy_sell: FinamPy.proto.common_pb2.BuySell.ValueType = ...,
        commission: builtins.float = ...,
        currency: builtins.str = ...,
        accrued_interest: builtins.float = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["created_at", b"created_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["accrued_interest", b"accrued_interest", "buy_sell", b"buy_sell", "client_id", b"client_id", "commission", b"commission", "created_at", b"created_at", "currency", b"currency", "order_no", b"order_no", "price", b"price", "quantity", b"quantity", "security_code", b"security_code", "trade_no", b"trade_no", "value", b"value"]) -> None: ...

global___TradeEvent = TradeEvent

@typing.final
class OrderBookRow(google.protobuf.message.Message):
    """Order book row.
    Строка стакана.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PRICE_FIELD_NUMBER: builtins.int
    QUANTITY_FIELD_NUMBER: builtins.int
    price: builtins.float
    """Price.
    Цена.
    """
    quantity: builtins.int
    """Lots.
    Количество лотов.
    """
    def __init__(
        self,
        *,
        price: builtins.float = ...,
        quantity: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["price", b"price", "quantity", b"quantity"]) -> None: ...

global___OrderBookRow = OrderBookRow

@typing.final
class OrderBookEvent(google.protobuf.message.Message):
    """OrderBook event.
    Событие стакана.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECURITY_CODE_FIELD_NUMBER: builtins.int
    SECURITY_BOARD_FIELD_NUMBER: builtins.int
    ASKS_FIELD_NUMBER: builtins.int
    BIDS_FIELD_NUMBER: builtins.int
    security_code: builtins.str
    """Security Code.
    Тикер инструмента.
    """
    security_board: builtins.str
    """Trading Board.
    Режим торгов.
    """
    @property
    def asks(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___OrderBookRow]:
        """Asks.
        Заявки на продажу.
        """

    @property
    def bids(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___OrderBookRow]:
        """Bids.
        Заявки на покупку.
        """

    def __init__(
        self,
        *,
        security_code: builtins.str = ...,
        security_board: builtins.str = ...,
        asks: collections.abc.Iterable[global___OrderBookRow] | None = ...,
        bids: collections.abc.Iterable[global___OrderBookRow] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["asks", b"asks", "bids", b"bids", "security_board", b"security_board", "security_code", b"security_code"]) -> None: ...

global___OrderBookEvent = OrderBookEvent

@typing.final
class PortfolioEvent(google.protobuf.message.Message):
    """Portfolio event.
    Событие портфеля.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLIENT_ID_FIELD_NUMBER: builtins.int
    CONTENT_FIELD_NUMBER: builtins.int
    EQUITY_FIELD_NUMBER: builtins.int
    BALANCE_FIELD_NUMBER: builtins.int
    POSITIONS_FIELD_NUMBER: builtins.int
    CURRENCIES_FIELD_NUMBER: builtins.int
    MONEY_FIELD_NUMBER: builtins.int
    client_id: builtins.str
    """Trade Account ID.
    Идентификатор торгового счёта.
    """
    equity: builtins.float
    """Current equity, RUB.
    Текущая оценка портфеля в рублях.
    """
    balance: builtins.float
    """Open Equity, RUB.
    Входящая оценка портфеля в рублях.
    """
    @property
    def content(self) -> FinamPy.proto.portfolios_pb2.PortfolioContent:
        """What kind of data portfolio event contains.
        Какие данные находятся в событии портфеля.
        """

    @property
    def positions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[FinamPy.proto.portfolios_pb2.PositionRow]:
        """DEPO positions.
        Позиции DEPO.
        """

    @property
    def currencies(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[FinamPy.proto.portfolios_pb2.CurrencyRow]:
        """Currency positions.
        Валютные позиции.
        """

    @property
    def money(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[FinamPy.proto.portfolios_pb2.MoneyRow]:
        """Money positions.
        Денежные позиции.
        """

    def __init__(
        self,
        *,
        client_id: builtins.str = ...,
        content: FinamPy.proto.portfolios_pb2.PortfolioContent | None = ...,
        equity: builtins.float = ...,
        balance: builtins.float = ...,
        positions: collections.abc.Iterable[FinamPy.proto.portfolios_pb2.PositionRow] | None = ...,
        currencies: collections.abc.Iterable[FinamPy.proto.portfolios_pb2.CurrencyRow] | None = ...,
        money: collections.abc.Iterable[FinamPy.proto.portfolios_pb2.MoneyRow] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["content", b"content"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["balance", b"balance", "client_id", b"client_id", "content", b"content", "currencies", b"currencies", "equity", b"equity", "money", b"money", "positions", b"positions"]) -> None: ...

global___PortfolioEvent = PortfolioEvent

@typing.final
class KeepAliveRequest(google.protobuf.message.Message):
    """Keep-alive request.
    Keep-alive запрос.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    REQUEST_ID_FIELD_NUMBER: builtins.int
    request_id: builtins.str
    """Request ID.
    Идентификатор запроса.
    """
    def __init__(
        self,
        *,
        request_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["request_id", b"request_id"]) -> None: ...

global___KeepAliveRequest = KeepAliveRequest
