import requests
import datetime as dt

date = dt.date(2018, 1, 1)
year = date.year
month = date.month

if (month < 10):
    month = f'0{month}'
    day = date.day
if (day < 10):
    day = f'0{day}'

file_code = f"{year}{month}{day}"
file_path = f'data/HOPE/{year}/{month}'
file_name = f'/{file_code}.cdf'
file_location = file_path + file_name
url = f'https://spdf.gsfc.nasa.gov/pub/data/rbsp/rbspb/l2/ect/hope/spinaverage/rel04/{year}'#/rbspb_rel04_ect-hope-sci-l2sa_{file_code}_v6.3.0.cdf'  # setting up target URL
r = requests.get(url)  # using the request module, handle a http get request to the URL
body = r.content
print(r.status_code)
print(body)