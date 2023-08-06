import requests
number = '01988762475'
url_4 = "https://www.billieln.xyz/billieln/v2/xJIvyxB8Isw1cLbNgQUcelbKwg2ezUFVT9us1vyILqY%3D"
headers_4 = {
                        "Appcode":"BillieLN",
                        "Content-Type":"application/json",
                        "Accept-Encoding":"gzip, deflate",
                        "User-Agent":"okhttp/5.0.0-alpha.2"}
data_4 = '{"mobile":"'+number+'","appCode":"BillieLN"}'
resp_4 = requests.post(url_4, headers=headers_4, data=data_4)
print(resp_4.text)