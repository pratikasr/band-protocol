#!/usr/bin/env python3
import requests
import json
import sys

class GetAssetPrices(object):
    def __init__(self, symbol):
        self.symbol = symbol

    def _handelDataSourceFailureForGoldSilver(self):
        # do something here
        return None
    
    def _handelDataSourceFailureForOil(self):
        # do something here
        return None

    def _makeRequest(self, requestType, url, headers={}, payload={}):
        if requestType not in ["GET", "POST"]:
            return {"result": "error", "message": "Invalid requestType"}
        try:
            response = requests.request(
                requestType, url, headers=headers, data=payload)
            response = response.json()
            data = {
                "result": "success",
                "responseData": response
            }
        except Exception as e:
            data = {"result": "error",
                    "message": "do something here", "responseData": None}
        return data

    def _getGoldSilverPrice(self):
        requestType = "GET"
        urlGoldSilver = "https://data-asg.goldprice.org/dbXRates/USD"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Cookie': 'lagrange_session=8a6ba1ba-dbda-4d01-b490-8e61cb308ea0'
        }
        payload = json.dumps({})
        data = self._makeRequest(
            requestType=requestType,
            url=urlGoldSilver,
            headers=headers,
            payload=payload
        )
        if data["result"] == "success" and data["responseData"] != None:
            data = data["responseData"]
            if (
                isinstance(data.get("items"), list) == True and
                "xauPrice" in data["items"][0] and
                "xagPrice" in data["items"][0]
            ):
                # GOLD
                if self.symbol == "XAU":
                    return data["items"][0]["xauPrice"]

                # SILVER
                if self.symbol == "XAG":
                    return data["items"][0]["xagPrice"]
            return self._handelDataSourceFailureForGoldSilver()
        return self._handelDataSourceFailureForGoldSilver()

    def _getOilPrice(self):
        requestType = "POST"
        urlOil = "https://asia-southeast2-price-caching.cloudfunctions.net/query-price"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "source": "oil",
            "symbols": [
                "oil"
            ]})
        data = self._makeRequest(
            requestType=requestType,
            url=urlOil,
            headers=headers,
            payload=payload
        )
        if data["result"] == "success" and data["responseData"] != None:
            data = data["responseData"]
            if isinstance(data, list) == True and len(data)==1:
                #  OIL
                return data[0]
            return self._handelDataSourceFailureForOil()
        return self._handelDataSourceFailureForOil()

    def getPrices(self):
        if self.symbol in ["XAU", "XAG"]:
            return self._getGoldSilverPrice()
        elif self.symbol in ["OIL"]:
            return self._getOilPrice()
        return None


def main(symbol):
    return GetAssetPrices(symbol[0]).getPrices()


if __name__ == "__main__":
    try:
        print(main([*sys.argv[1:]]))
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


