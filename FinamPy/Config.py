# Чтобы получить торговый токен:
# 1. Открыть счет в "Финаме" https://open.finam.ru/registration
# 2. Зарегистрироваться в сервисе Comon https://www.comon.ru/
# 3. В личном кабинете Comon получить торговый токен https://www.comon.ru/my/trade-api/tokens
import os

api_key = os.getenv('API_KEY')
client_code = os.getenv('CLIENT_CODE')


client_ids = (client_code,)  # Торговые счета
access_token = api_key  # Торговый токен
