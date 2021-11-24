#!/usr/bin/env python3
import requests
import sys

PRICE_URL = "https://api.coingecko.com/api/v3/simple/price"


def adjust_rounding(data):
    if data < 1:
        return round(data, 8)
    elif data < 10:
        return round(data, 6)
    else:
        return round(data, 4)


def main(symbols):
    SUPPORT_SLUGS = {
        "ATOM": "cosmos",
        "OSMO": "osmosis",
        "SCRT": "secret",
        "AKT": "akash-network",
        "UST": "terrausd",
        "JUNO": "juno-network",
        "ION": "ion",
        "XPRT": "persistence",
        "DVPN": "sentinel",
        "REGEN": "regen",
        "IOV": "starname",
        "NGM": "e-money",
        "IXO": "ixo",
        "BCNA": "bitcanna",
        "BTSG": "bitsong",
        "XKI": "ki",
        "LIKE": "likecoin",
        "EEUR": "e-money-eur",
        "BAND": "band-protocol",
    }

    slugs = []
    for symbol in symbols:
        if symbol not in SUPPORT_SLUGS:
            raise Exception(f"Unsupported {symbol} symbol")
        slugs.append(SUPPORT_SLUGS[symbol])

    prices = requests.get(
        PRICE_URL,
        params={"ids": ",".join(slugs), "vs_currencies": "USD"},
    ).json()
    result = [(px["usd"], slug) for slug in slugs for (key, px) in list(prices.items()) if slug == key]

    return ",".join([str(adjust_rounding(px[0])) for px in result])


if __name__ == "__main__":
    try:
        print(main([*sys.argv[1:]]))
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

