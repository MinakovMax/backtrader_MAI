import logging
from datetime import datetime, timedelta

import backtrader as bt

from BackTraderFinam import FNStore  # Хранилище Finam
from MarketPy.Schedule import MOEXStocks, MOEXFutures  # Расписания торгов фондового/срочного рынков

import telebot
import joblib
import pandas as pd
import os

# noinspection PyShadowingNames,PyProtectedMember
class LRStrategyDocker(bt.Strategy):
    """
    - Отображает статус подключения
    - При приходе нового бара отображает его цены/объем
    - Отображает статус перехода к новым барам
    """
    params = (  # Параметры торговой системы
        ('name', None),  # Название торговой системы
        ('symbols', None),
        ('profit_percent', 0.009),  # Цель прибыли 0.3%
        ('loss_percent', 0.0015),  # Ограничение убытков 0.15%
    )  # Список торгуемых тикеров. По умолчанию торгуем все тикеры
    
    logger = logging.getLogger('BackTraderFinam.TeleBotSberDocker')  # Будем вести лог   

    def __init__(self):
     
        # self.model = joblib.load('/home/backtrader/BackTraderTinkoff/Examples/sber1mv2.joblib')
        self.model = joblib.load('/app/BackTraderFinam/Examples/sber1mv2.joblib')
        telebot_key = os.getenv('TELEBOT_KEY')
        self.bot = telebot.TeleBot(telebot_key)
        self.open_price = 0        
        self.live = False  # Сначала будут приходить исторические данные, затем перейдем в режим реальной торговли
        self.order = None  # Заявка на вход/выход из позиции
        self.logger.info("__init__ выполняется.")

    def next(self):        
        """Получение следующего исторического/нового бара"""
        self.logger.info("Метод next выполняется.")
        
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
            self.logger.info(f'Уверенность модели: {y[0]}')
            self.bot.send_message(527704275, f'Уверенность модели: {y[0]}')
            
            # Проверка на наличие открытых позиций
            if self.open_price == 0:                
                # Сигнал на покупку - условие всегда истинно для демонстрации
                if y[0] > 0.10:
                    price = self.data.close[0]  # Текущая цена закрытия
                    
                    self.open_price = price
                    self.logger.info(f'Хорошая вероятность роста сбербанка при цене {price}, цель {price * (1 + self.params.profit_percent):.2f}')
                    self.bot.send_message(527704275, f'Хорошая вероятность роста сбербанка при цене {price}, цель {price * (1 + self.params.profit_percent):.2f}')
            else:
                # Получаем текущую цену
                price = self.data.close[0]                   
                # Цель достигнута
                if price >= self.open_price * (1 + self.params.profit_percent):
                    result = self.open_price * (1 + self.params.profit_percent)
                    self.logger.info(f'Цель достигнута результат {result}')
                    self.bot.send_message(527704275, f'Цель достигнута результат {result}')
                    self.open_price = 0
                    
                # Остановка убытков
                elif price <= self.open_price * (1 - self.params.loss_percent):
                    result = self.open_price * (1 - self.params.loss_percent)
                    
                    self.logger.info(f'Стоп-лосс {result}')
                    self.bot.send_message(527704275, f'Стоп-лосс {result}')
                    self.open_price = 0                    
        else:            
           self.logger.info(f'Поступило только {len(self.data)}, свечей, режим {self.live}')

    def notify_data(self, data, status, *args, **kwargs):
        """Изменение статуса приходящих баров"""
        data_status = data._getstatusname(status)  # Получаем статус (только при live_bars=True)
        self.live = data_status == 'LIVE'  # Режим реальной торговли
        self.logger.info(data_status)




if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    symbol = 'TQBR.SBER'  # Тикер в формате: <Код режима торгов>.<Тикер>
    # symbol = 'FUT.SiH4'  # Для фьючерсов: <FUT>.<Код тикера><Месяц экспирации: 3-H, 6-M, 9-U, 12-Z>.<Последняя цифра года>
    # symbol = 'FUT.RIH4'
    timeframe = bt.TimeFrame.Minutes  # Минутный временой интервал
    compression = 1  # 1 минута
    fromdate = datetime.today().date() - timedelta(days=1)  # За сегодня
    live_bars = True  # Исторические и новые бары
    schedule = MOEXStocks()  # Расписание торгов фондового рынка
    # schedule = MOEXFutures()  # Расписание торгов срочного рынка

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщения
                        datefmt='%d.%m.%Y %H:%M:%S',  # Формат даты
                        level=logging.DEBUG,  # Уровень логируемых событий NOTSET/DEBUG/INFO/WARNING/ERROR/CRITICAL
                        handlers=[logging.FileHandler('TeleBotSberDocker.log'), logging.StreamHandler()])  # Лог записываем в файл и выводим на консоль
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
    cerebro.addstrategy(LRStrategyDocker)  # Добавляем торговую систему с лимитным входом в n%
    cerebro.run()  # Запуск торговой системы
