import requests

res = requests.get("https://prices.azure.com/api/retail/prices?currencyCode='USD'&api-version=2021-10-01-preview&$filter=skuid eq 'DZH318Z0BQ50/02C8'")

for elem in res["Items"]:
    x = res["Items"][elem]["retailPrice"]
    print(x)

def myFunc(x):
    x = x+1
    return x
    

if __name__ == "__main__":
    myFunc(1)