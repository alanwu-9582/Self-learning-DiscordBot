import requests
import twstock


company_name = "台積電"

try:
    stock_id = int(company_name)

except:
    stock_id = None
    for code, name in codes.items():
        if company_name in name:
            stock_id = code
            break

if stock_id == None:
    print(f"無法獲取 {company_name} 的資訊")

else:
    url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_id}.tw"
    response = requests.get(url)
    data = response.json()

    if "msgArray" in data:
        msg = data["msgArray"][0]
        name = msg["n"]
        now_price = float(msg["z"])
        last_price = float(msg["y"])
        data_date = msg["d"]
        print(f"{name} ({stock_id}): 目前股價 {now_price}，資料日期 {data_date} 漲跌 ({now_price-last_price})")

    else:
        print("無法獲取股票資訊")