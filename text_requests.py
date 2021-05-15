import requests
resp = requests.get("http://home.uchicago.edu/~svaikunt", allow_redirects=False)
print("history")
print(resp.headers['Location'])
print(resp.url)
print(resp.history)
for res in resp.history:
    print(res.url, res.status_code)

someurl = "http://home.uchicago.edu/~svaikunt"
response = requests.get(someurl)
if response.history:
    print("Request was redirected")
    for resp in response.history:
        print(resp.status_code, resp.url)
    print("Final destination:")
    print(response.status_code, response.url)
else:
    print("Request was not redirected")
