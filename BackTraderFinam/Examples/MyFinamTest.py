import logging
from datetime import datetime, timedelta

import backtrader as bt

from BackTraderFinam import FNStore  # Хранилище Finam
from MarketPy.Schedule import MOEXStocks, MOEXFutures  # Расписания торгов фондового/срочного рынков

import telebot
import joblib
import pandas as pd

# noinspection PyShadowingNames,PyProtectedMember
class LRStrategy(bt.Strategy):
    """
    - Отображает статус подключения
    - При приходе нового бара отображает его цены/объем
    - Отображает статус перехода к новым барам
    """
    params = (  # Параметры торговой системы
        ('name', None),  # Название торговой системы
        ('symbols', None),
        ('profit_percent', 0.003),  # Цель прибыли 0.3%
        ('loss_percent', 0.0015),  # Ограничение убытков 0.15%
    )  # Список торгуемых тикеров. По умолчанию торгуем все тикеры
    
    logger = logging.getLogger('BackTraderFinam.MyFinamTest')  # Будем вести лог   

    def __init__(self):
     
        self.model = joblib.load('/home/backtrader/BackTraderTinkoff/Examples/sber1mv2.joblib')
        # self.model = joblib.load('/app/BackTraderFinam/DataExamples/sber1mv2.joblib')
        self.bot = telebot.TeleBot('7186072535:AAEY1bD8D-xpvvFZihsaDoTFI2ujKlxPems')
        
        self.live = False  # Сначала будут приходить исторические данные, затем перейдем в режим реальной торговли
        self.order = None  # Заявка на вход/выход из позиции

    def next(self):        
        """Получение следующего исторического/нового бара"""
                
        if len(self.data) > 100 and self.live:
            len100closes = [self.data.close[-i] for i in range(0, 100)]
            
            df = pd.DataFrame([len100closes], columns=[f'close_{i}' for i in range(1, 101)])            

            df['date'] = bt.num2date(self.data.datetime[0])
            
            # Добавление новых колонок
            df['month'] = df['date'].dt.month
            df['day_of_week'] = df['date'].dt.day_name()  # или df['begin'].dt.weekday для числового представления
            df['hour'] = df['date'].dt.hour
            df.drop(columns=['date'], inplace=True)

            y = self.model.predict_proba(df)[:, 1]
             
            self.logger.info(f'Вероятность роста {y[0]}')
            self.logger.info(f'{self.position}')
            self.logger.info(f'{self.order}')
            
            if self.order:
                return     
                        
            if 0 == 0:                    
                self.order = self.sell()
                self.logger.info(f'{self.order}')              
                
            # Проверка на наличие открытых позиций
            if not self.position and 2 == 3:
                
                # Сигнал на покупку - условие всегда истинно для демонстрации
                if y[0] > 0.14:
                    # cash = self.broker.get_cash()  # Доступный капитал
                    price = self.data.close[0]  # Текущая цена закрытия
                    # size = int(cash / price)  # Размер позиции, который можно купить (без учета комиссии)
            
                    # self.buy(size=size)
                    self.order = self.buy(exectype=bt.Order.Market)
                    
                    # Выполнение покупки
                    self.logger.info(f'ПОКУПКА, Цена: {price:.2f}')
                    
            else:
                # Получаем текущую цену
                price = self.data.close[0]
                
                purchase_price = self.position.price
                print(purchase_price)
                # purchase_price = self.my_pos_price
                # size = self.position.size  # Текущий размер позиции
                
                # Цель достигнута
                if price >= purchase_price * (1 + self.params.profit_percent):
                    self.logger.info('ЦЕЛЬ ДОСТИГНУТА')
                    self.bot.send_message(527704275, f'ЦЕЛЬ ДОСТИГНУТА')
                    # self.order = self.sell(size=size)  # Закрытие позиции
                    self.order = self.sell(exectype=bt.Order.Market)
                    
                # Остановка убытков
                elif price <= purchase_price * (1 - self.params.loss_percent):
                    self.logger.info('СТОП-ЛОСС')
                    self.bot.send_message(527704275, f'СТОП-ЛОСС')
                    # self.order = self.sell(size=size)  # Закрытие позиции
                    self.order = self.sell(exectype=bt.Order.Market)
        else:            
           self.logger.info(f'Поступило только {len(self.data)}, свечей, режим {self.live}')

    def notify_data(self, data, status, *args, **kwargs):
        """Изменение статуса приходящих баров"""
        data_status = data._getstatusname(status)  # Получаем статус (только при live_bars=True)
        self.live = data_status == 'LIVE'  # Режим реальной торговли
        self.logger.info(data_status)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Заявка отправлена/принята - ничего не делаем            
            return

        # Проверка, выполнена ли заявка
        if order.status in [order.Completed]:
            if order.isbuy():
                self.logger.info(f'КУПЛЕНО, ЦЕНА: {order.executed.price:.2f}')
                self.bot.send_message(527704275, f'КУПЛЕНО, ЦЕНА: {order.executed.price:.2f}')
            elif order.issell():
                self.logger.info(f'ПРОДАНО, ЦЕНА: {order.executed.price:.2f}')
                self.bot.send_message(527704275, f'ПРОДАНО, ЦЕНА: {order.executed.price:.2f}')
                
            self.bar_executed = len(self)  # Запоминаем бар исполнения

        # Сброс ордера после выполнения/отмены
        self.order = None

    def notify_trade(self, trade):
        """Изменение статуса позиции"""
        if trade.isclosed:  # Если позиция закрыта
            self.logger.info(f'Позиция закрыта. Прибыль = {trade.pnl:.2f}, С учетом комиссий = {trade.pnlcomm:.2f}')


if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    symbol = 'TQBR.SBER'  # Тикер в формате: <Код режима торгов>.<Тикер>
    # symbol = 'FUT.SiH4'  # Для фьючерсов: <FUT>.<Код тикера><Месяц экспирации: 3-H, 6-M, 9-U, 12-Z>.<Последняя цифра года>
    # symbol = 'FUT.RIH4'
    timeframe = bt.TimeFrame.Minutes  # Минутный временной интервал
    compression = 1  # 1 минута
    fromdate = datetime.today().date() - timedelta(days=1)  # За сегодня
    live_bars = True  # Исторические и новые бары
    schedule = MOEXStocks()  # Расписание торгов фондового рынка
    # schedule = MOEXFutures()  # Расписание торгов срочного рынка

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщения
                        datefmt='%d.%m.%Y %H:%M:%S',  # Формат даты
                        level=logging.DEBUG,  # Уровень логируемых событий NOTSET/DEBUG/INFO/WARNING/ERROR/CRITICAL
                        handlers=[logging.FileHandler('LimitCancel.log'), logging.StreamHandler()])  # Лог записываем в файл и выводим на консоль
    logging.Formatter.converter = lambda *args: datetime.now(tz=store.provider.tz_msk).timetuple()  # В логе время указываем по МСК

    # noinspection PyArgumentList
    cerebro = bt.Cerebro(stdstats=False, quicknotify=True)  # Инициируем "движок" BackTrader. Стандартная статистика сделок и кривой доходности не нужна. События принимаем без задержек
    store = FNStore()  # Хранилище Finam
    broker = store.getbroker()  # Брокер Finam
    # noinspection PyArgumentList
    cerebro.setbroker(broker)  # Устанавливаем брокера
    # data = store.getdata(dataname=symbol, timeframe=timeframe, compression=compression, fromdate=fromdate, live_bars=live_bars)  # TODO Ждем от Финама подписку на бары Исторические и новые минутные бары за сегодня по подписке
    data = store.getdata(dataname=symbol, timeframe=timeframe, compression=compression, fromdate=fromdate, schedule=schedule, live_bars=live_bars)  # Исторические и новые минутные бары за сегодня по расписанию
    cerebro.adddata(data)  # Добавляем данные
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)  # Кол-во акций в штуках для покупки/продажи
    # cerebro.addsizer(bt.sizers.FixedSize, stake=1)  # Кол-во фьючерсов в штуках для покупки/продажи
    cerebro.addstrategy(LRStrategy)  # Добавляем торговую систему с лимитным входом в n%
    cerebro.run()  # Запуск торговой системы
