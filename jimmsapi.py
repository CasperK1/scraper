import requests

cookies = {
    'JW.S': 'yf7ifsyJIgklaHEqucmMF9/Pv9JuILGfx4jFU7N7nbESgQtC48TNM7o1x5qxjtS2WNZacZ4Mf/FcOQQ+liMmuHss3lsldNCjzZhcDeVfTeI=',
    'JW.CurrentUICulture': 'fi',
    'cf_clearance': 'kW8DP8Cb1VEWOB16yuwoyRQAg1KV0viuS4U7nEVu_Ig-1716201463-1.0.1.1-FgFWZV5inQ5UBZ_tptEXR_LemLJDl1fycGcnJMtgjQ1KsnkJ1wCATOuJqUp_QIZsWIPTN3QhqVDAe0CLGvGbjQ',
    '_vwo_uuid_v2': 'D8F517C9F656DD9959679A75412CB4167^|5f36d79f4948c6ae970b4c6382f6073e',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
    'Cookie': 'JW.S=yf7ifsyJIgklaHEqucmMF9/Pv9JuILGfx4jFU7N7nbESgQtC48TNM7o1x5qxjtS2WNZacZ4Mf/FcOQQ+liMmuHss3lsldNCjzZhcDeVfTeI=; JW.CurrentUICulture=fi; cf_clearance=kW8DP8Cb1VEWOB16yuwoyRQAg1KV0viuS4U7nEVu_Ig-1716201463-1.0.1.1-FgFWZV5inQ5UBZ_tptEXR_LemLJDl1fycGcnJMtgjQ1KsnkJ1wCATOuJqUp_QIZsWIPTN3QhqVDAe0CLGvGbjQ; _vwo_uuid_v2=D8F517C9F656DD9959679A75412CB4167^|5f36d79f4948c6ae970b4c6382f6073e',
}

data = {
    "Page": 1,
    "Items": 50,
    "OrderBy": 10,
    "OrderDir": 0,
    "SearchGroup": None,
    "SearchQuery": "rtx 4090",
    "SearchIsChanged": True,
    "MinPrice": 0,
    "MaxPrice": 0,
    "Filters": {
        "Vendor": ["^"],
        "VendorIsChanged": False,
        "Group": ["^000-1N0^"],
        "GroupIsChanged": True,
        "Property": None,
        "PropertyIsChanged": None
    }
}

response = requests.post(
    'https://www.jimms.fi/api/product/newbetasearch?1716201876968',
    cookies=cookies,
    headers=headers,
    json=data
)

print(response.json())
