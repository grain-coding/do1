import time
import pyupbit
import datetime

access = "2ZcsVBZUU9sjfmUEANJlaJBuTya26TmJ20mNzBQw"
secret = "vT4Y3vGzZpgj9OlgN2e2jX9oCksxCxgqfpnrDSSn"

def get_target_price("KRW-eth", 0.4):
    
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv("KRW-eth", interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * 0.4
    return target_price

def get_start_time("KRW-eth"):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv("KRW-eth", interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15("KRW-eth"):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv("KRW-eth", interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance("KRW-eth"):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == "KRW-eth":
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price("KRW-eth"):
    """현재가 조회"""
    return pyupbit.get_orderbook("KRW-eth"="KRW-eth")["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-eth")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-eth", 0.4)
            ma15 = get_ma15("KRW-eth")
            current_price = get_current_price("KRW-eth")
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order(""KRW-eth"", krw*0.9995)
        else:
            eth = get_balance("ETH")
            if eth > 0.00008:
                upbit.sell_market_order(""KRW-eth"", eth*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)