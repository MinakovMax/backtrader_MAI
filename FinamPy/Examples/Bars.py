import logging  # Выводим лог на консоль и в файл
from datetime import datetime, timezone, timedelta  # Дата и время, временнАя зона, временной интервал
from time import time
import os.path

import pandas as pd

from FinamPy import FinamPy  # Работа с сервером TRANSAQ

from FinamPy.proto.candles_pb2 import DayCandleInterval, IntradayCandleInterval
from FinamPy.proto.google.type.date_pb2 import Date
from google.protobuf.json_format import MessageToDict


logger = logging.getLogger('FinamPy.Bars')  # Будем вести лог. Определяем здесь, т.к. возможен внешний вызов ф-ии
datapath = os.path.join('FinamPy', '')  # Путь сохранения файла истории
delimiter = '\t'  # Разделитель значений в файле истории. По умолчанию табуляция
dt_format = '%d.%m.%Y %H:%M'  # Формат представления даты и времени в файле истории. По умолчанию русский формат
min_bar_open_utc = datetime(1990, 1, 1, tzinfo=timezone.utc)  # Дата, когда никакой тикер еще не торговался


# noinspection PyShadowingNames
def load_candles_from_file(class_code='TQBR', security_code='SBER', tf='D1') -> pd.DataFrame:
    """Получение бар из файла

    :param str class_code: Код режима торгов
    :param str security_code: Код тикера
    :param str tf: Временной интервал https://ru.wikipedia.org/wiki/Таймфрейм
    """
    filename = f'{datapath}{class_code}.{security_code}_{tf}.txt'
    file_exists = os.path.isfile(filename)  # Существует ли файл
    if file_exists:  # Если файл существует
        logger.info(f'Получение файла {filename}')
        file_bars = pd.read_csv(filename, sep=delimiter, parse_dates=['datetime'], date_format=dt_format, index_col='datetime')
        logger.info(f'Первый бар    : {file_bars.index[0]:{dt_format}}')
        logger.info(f'Последний бар : {file_bars.index[-1]:{dt_format}}')
        logger.info(f'Кол-во бар    : {len(file_bars)}')
        return file_bars
    else:  # Если файл не существует
        logger.warning(f'Файл {filename} не найден')
        return pd.DataFrame()


# noinspection PyShadowingNames
def get_candles_from_provider(fp_provider=FinamPy(), class_code='TQBR', security_code='SBER', tf='D1', next_bar_open_utc=min_bar_open_utc) -> pd.DataFrame:
    """Получение бар из провайдера

    :param FinamPy fp_provider: Провайдер Finam
    :param str class_code: Код режима торгов
    :param str security_code: Код тикера
    :param str tf: Временной интервал https://ru.wikipedia.org/wiki/Таймфрейм
    :param datetime next_bar_open_utc: Первый возможный бар по UTC
    """
    time_frame, intraday = fp_provider.timeframe_to_finam_timeframe(tf)  # Временной интервал Finam, внутридневной интервал
    logger.info(f'Получение истории {class_code}.{security_code} {tf} из Finam')
    td = timedelta(days=(30 if intraday else 365))  # Максимальный запрос за 30 дней для внутридневных интервалов и 1 год (365 дней) для дневных и выше
    interval = IntradayCandleInterval(count=500) if intraday else DayCandleInterval(count=500)  # Нужно поставить максимальное кол-во бар. Максимум, можно поставить 500
    todate_utc = datetime.utcnow().replace(tzinfo=timezone.utc)  # Будем получать бары до текущей даты и времени UTC
    from_ = getattr(interval, 'from')  # Т.к. from - ключевое слово в Python, то получаем атрибут from из атрибута интервала
    to_ = getattr(interval, 'to')  # Аналогично будем работать с атрибутом to для единообразия
    first_request = next_bar_open_utc == min_bar_open_utc  # Если файл не существует, то первый запрос будем формировать без даты окончания. Так мы в первом запросе получим первые бары истории
    new_bars = []  # Список новых бар
    while True:  # Будем получать бары пока не получим все
        todate_min_utc = min(todate_utc, next_bar_open_utc + td)  # До какой даты можем делать запрос
        if intraday:  # Для интрадея datetime -> Timestamp
            from_.seconds = int(next_bar_open_utc.timestamp())  # Дата и время начала интервала UTC
            if not first_request:  # Для всех запросов, кроме первого
                to_.seconds = int(todate_min_utc.timestamp())  # Дата и время окончания интервала UTC
                if from_.seconds == to_.seconds:  # Если дата и время окончания интервала совпадает с датой и временем начала
                    break  # то выходим из цикла получения бар
        else:  # Для дневных интервалов и выше datetime -> Date
            date_from = Date(year=next_bar_open_utc.year, month=next_bar_open_utc.month, day=next_bar_open_utc.day)  # Дата начала интервала UTC
            from_.year = date_from.year
            from_.month = date_from.month
            from_.day = date_from.day
            if not first_request:  # Для всех запросов, кроме первого
                date_to = Date(year=todate_min_utc.year, month=todate_min_utc.month, day=todate_min_utc.day)  # Дата окончания интервала UTC
                if date_to == date_from:  # Если дата окончания интервала совпадает с датой начала
                    break  # то выходим из цикла получения бар
                to_.year = date_to.year
                to_.month = date_to.month
                to_.day = date_to.day
        if first_request:  # Для первого запроса
            first_request = False  # далее будем ставить в запросы дату окончания интервала
        logger.debug(f'Запрос с {next_bar_open_utc} по {todate_min_utc}')
        candles = (fp_provider.get_intraday_candles(class_code, security_code, time_frame, interval) if intraday else
                   fp_provider.get_day_candles(class_code, security_code, time_frame, interval))  # Получаем ответ на запрос бар
        if not candles:  # Если бары не получены
            logger.error('Ошибка при получении истории: История не получена')
            return pd.DataFrame()  # то выходим, дальше не продолжаем
        candles_dict = MessageToDict(candles, always_print_fields_with_no_presence=True)  # Переводим в словарь из JSON
        if 'candles' not in candles_dict:  # Если бар нет в словаре
            logger.error(f'Ошибка при получении истории: {candles_dict}')
            return pd.DataFrame()  # то выходим, дальше не продолжаем
        new_bars_dict = candles_dict['candles']  # Получаем все бары из Finam
        if len(new_bars_dict) > 0:  # Если пришли новые бары
            # Дату/время UTC получаем в формате ISO 8601. Пример: 2023-06-16T20:01:00Z
            # В статье https://stackoverflow.com/questions/127803/how-do-i-parse-an-iso-8601-formatted-date описывается проблема, что Z на конце нужно убирать
            first_bar_open_dt = fp_provider.utc_to_msk_datetime(
                datetime.fromisoformat(new_bars_dict[0]['timestamp'][:-1])) if intraday else \
                datetime(new_bars_dict[0]['date']['year'], new_bars_dict[0]['date']['month'], new_bars_dict[0]['date']['day'])  # Дату и время первого полученного бара переводим из UTC в МСК
            last_bar_open_dt = fp_provider.utc_to_msk_datetime(
                datetime.fromisoformat(new_bars_dict[-1]['timestamp'][:-1])) if intraday else \
                datetime(new_bars_dict[-1]['date']['year'], new_bars_dict[-1]['date']['month'], new_bars_dict[-1]['date']['day'])  # Дату и время последнего полученного бара переводим из UTC в МСК
            logger.debug(f'Получены бары с {first_bar_open_dt} по {last_bar_open_dt}')
            for new_bar in new_bars_dict:  # Пробегаемся по всем полученным барам
                dt = fp_provider.utc_to_msk_datetime(
                    datetime.fromisoformat(new_bar['timestamp'][:-1])) if intraday else \
                    datetime(new_bar['date']['year'], new_bar['date']['month'], new_bar['date']['day'])  # Дату и время переводим из UTC в МСК
                open_ = fp_provider.dict_decimal_to_float(new_bar['open'])
                high = fp_provider.dict_decimal_to_float(new_bar['high'])
                low = fp_provider.dict_decimal_to_float(new_bar['low'])
                close = fp_provider.dict_decimal_to_float(new_bar['close'])
                volume = new_bar['volume']  # Объем в штуках
                new_bars.append({'datetime': dt, 'open': open_, 'high': high, 'low': low, 'close': close, 'volume': volume})
            last_bar_open_utc = fp_provider.msk_to_utc_datetime(last_bar_open_dt, True) if intraday else last_bar_open_dt.replace(tzinfo=timezone.utc)  # Дата и время открытия последнего бара UTC
            next_bar_open_utc = last_bar_open_utc + timedelta(minutes=1) if intraday else last_bar_open_utc + timedelta(days=1)  # Смещаем время на возможный следующий бар UTC
        else:  # Если новых бар нет
            next_bar_open_utc = todate_min_utc + timedelta(minutes=1) if intraday else todate_min_utc + timedelta(days=1)  # то смещаем время на возможный следующий бар UTC
        if next_bar_open_utc > todate_utc:  # Если пройден весь интервал
            break  # то выходим из цикла получения бар
    if len(new_bars) == 0:  # Если новых бар нет
        logger.info('Новых записей нет')
        return pd.DataFrame()  # то выходим, дальше не продолжаем
    pd_bars = pd.DataFrame(new_bars)  # Переводим список бар в pandas DataFrame
    pd_bars.index = pd_bars['datetime']  # В индекс ставим дату/время
    pd_bars = pd_bars[['datetime', 'open', 'high', 'low', 'close', 'volume']]  # Отбираем нужные колонки. Дата и время нужна, чтобы не удалять одинаковые OHLCV на разное время
    logger.info(f'Первый бар    : {pd_bars.index[0]:{dt_format}}')
    logger.info(f'Последний бар : {pd_bars.index[-1]:{dt_format}}')
    logger.info(f'Кол-во бар    : {len(pd_bars)}')
    return pd_bars


# noinspection PyShadowingNames
def save_candles_to_file(fp_provider=FinamPy(), class_code='TQBR', security_codes=('SBER',), tf='D1',
                         skip_first_date=False, skip_last_date=False, four_price_doji=False):
    """Получение новых бар из провайдера, объединение с имеющимися барами в файле (если есть), сохранение бар в файл

    :param FinamPy fp_provider: Провайдер Finam
    :param str class_code: Код режима торгов
    :param tuple security_codes: Коды тикеров в виде кортежа
    :param str tf: Временной интервал https://ru.wikipedia.org/wiki/Таймфрейм
    :param bool skip_first_date: Убрать бары на первую полученную дату
    :param bool skip_last_date: Убрать бары на последнюю полученную дату
    :param bool four_price_doji: Оставить бары с дожи 4-х цен
    """
    _, intraday = fp_provider.timeframe_to_finam_timeframe(tf)  # Временной интервал Finam, внутридневной интервал
    for security_code in security_codes:  # Пробегаемся по всем тикерам
        file_bars = load_candles_from_file(class_code, security_code, tf)  # Получаем бары из файла
        if file_bars.empty:  # Если файла нет
            next_bar_open_utc = min_bar_open_utc  # Берем дату, когда никакой тикер еще не торговался
        else:  # Если получили бары из файла
            last_date: datetime = file_bars.index[-1]  # Дата и время последнего бара по МСК
            next_bar_open_utc = fp_provider.msk_to_utc_datetime(last_date + timedelta(minutes=1), True) if intraday else \
                last_date.replace(tzinfo=timezone.utc) + timedelta(days=1)  # Смещаем время на возможный следующий бар по UTC
        pd_bars = get_candles_from_provider(fp_provider, class_code, security_code, tf, next_bar_open_utc)  # Получаем бары из провайдера
        if pd_bars.empty:  # Если бары не получены
            logger.info('Новых бар нет')
            continue  # то переходим к следующему тикеру, дальше не продолжаем
        if not file_bars.empty and skip_first_date:  # Если файла нет, и убираем бары на первую дату
            len_with_first_date = len(pd_bars)  # Кол-во бар до удаления на первую дату
            first_date = pd_bars.index[0].date()  # Первая дата
            pd_bars.drop(pd_bars[(pd_bars.index.date == first_date)].index, inplace=True)  # Удаляем их
            logger.warning(f'Удалено бар на первую дату {first_date}: {len_with_first_date - len(pd_bars)}')
        if skip_last_date:  # Если убираем бары на последнюю дату
            len_with_last_date = len(pd_bars)  # Кол-во бар до удаления на последнюю дату
            last_date = pd_bars.index[-1].date()  # Последняя дата
            pd_bars.drop(pd_bars[(pd_bars.index.date == last_date)].index, inplace=True)  # Удаляем их
            logger.warning(f'Удалено бар на последнюю дату {last_date}: {len_with_last_date - len(pd_bars)}')
        if not four_price_doji:  # Если удаляем дожи 4-х цен
            len_with_doji = len(pd_bars)  # Кол-во бар до удаления дожи
            pd_bars.drop(pd_bars[(pd_bars.high == pd_bars.low)].index, inplace=True)  # Удаляем их по условия High == Low
            logger.warning(f'Удалено дожи 4-х цен: {len_with_doji - len(pd_bars)}')
        if len(pd_bars) == 0:  # Если нечего объединять
            logger.info('Новых бар нет')
            continue  # то переходим к следующему тикеру, дальше не продолжаем
        if not file_bars.empty:  # Если файл существует
            pd_bars = pd.concat([file_bars, pd_bars]).drop_duplicates(keep='last').sort_index()  # Объединяем файл с данными из Finam, убираем дубликаты, сортируем заново
        pd_bars = pd_bars[['open', 'high', 'low', 'close', 'volume']]  # Отбираем нужные колонки. Дата и время будет экспортирована как индекс
        filename = f'{datapath}{class_code}.{security_code}_{tf}.txt'
        logger.info('Сохранение файла')
        pd_bars.to_csv(filename, sep=delimiter, date_format=dt_format)
        logger.info(f'Первый бар    : {pd_bars.index[0]}')
        logger.info(f'Последний бар : {pd_bars.index[-1]}')
        logger.info(f'Кол-во бар    : {len(pd_bars)}')
        logger.info(f'В файл {filename} сохранено записей: {len(pd_bars)}')


if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    start_time = time()  # Время начала запуска скрипта
    fp_provider = FinamPy()  # Подключаемся ко всем торговым счетам

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщения
                        datefmt='%d.%m.%Y %H:%M:%S',  # Формат даты
                        level=logging.DEBUG,  # Уровень логируемых событий NOTSET/DEBUG/INFO/WARNING/ERROR/CRITICAL
                        handlers=[logging.FileHandler('Bars.log'), logging.StreamHandler()])  # Лог записываем в файл и выводим на консоль
    logging.Formatter.converter = lambda *args: datetime.now(tz=fp_provider.tz_msk).timetuple()  # В логе время указываем по МСК

    class_code = 'TQBR'  # Акции ММВБ
    security_codes = ('SBER',)  # Для тестов
    # security_codes = ('SBER', 'VTBR', 'GAZP', 'NMTP', 'LKOH', 'BSPB', 'FESH', 'ALRS', 'YNDX', 'BELU',
    #                   'GMKN', 'MTLR', 'HYDR', 'MAGN', 'SNGSP', 'NVTK', 'ROSN', 'TATN', 'SBERP', 'CHMF',
    #                   'MGNT', 'RTKM', 'TRNFP', 'MTSS', 'FEES', 'SNGS', 'NLMK', 'PLZL', 'RNFT', 'MOEX',
    #                   'DVEC', 'TGKA', 'MTLRP', 'RUAL', 'TRMK', 'IRAO', 'SMLT', 'AFKS', 'AFLT', 'PIKK')  # TOP 40 акций ММВБ
    # class_code = 'SPBFUT'  # Фьючерсы (FUT)
    # security_codes = ('SiM4', 'RIM4')  # Формат фьючерса: <Тикер><Месяц экспирации><Последняя цифра года> Месяц экспирации: 3-H, 6-M, 9-U, 12-Z
    # security_codes = ('USDRUBF', 'EURRUBF', 'CNYRUBF', 'GLDRUBF', 'IMOEXF')  # Вечные фьючерсы ММВБ

    skip_last_date = True  # Если получаем данные внутри сессии, то не берем бары за дату незавершенной сессии
    # skip_last_date = False  # Если получаем данные, когда рынок не работает, то берем все бары
    save_candles_to_file(fp_provider, class_code, security_codes, 'D1', skip_last_date=skip_last_date, four_price_doji=True)  # Дневные бары
    # save_candles_to_file(fp_provider, class_code, security_codes, 'M60', skip_last_date=skip_last_date)  # Часовые бары
    # save_candles_to_file(fp_provider, class_code, security_codes, 'M15', skip_last_date=skip_last_date)  # 15-и минутные бары
    # save_candles_to_file(fp_provider, class_code, security_codes, 'M5', skip_last_date=skip_last_date)  # 5-и минутные бары
    # save_candles_to_file(fp_provider, class_code, security_codes, 'M1', skip_last_date=skip_last_date, four_price_doji=True)  # Минутные бары

    fp_provider.close_channel()  # Закрываем канал перед выходом

    logger.info(f'Скрипт выполнен за {(time() - start_time):.2f} с')
