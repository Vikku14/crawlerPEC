# API https://api.m.ox.ac.uk/contact/search?q={q}&medium={email or phone}&match=approximate
import requests
import string
import json
alphabet_list = list(string.ascii_lowercase)

# fetch email list
email_list = list()
for alpha in alphabet_list:
    URL = 'https://api.m.ox.ac.uk/contact/search?q={}&medium=email&match=approximate'.format(alpha)
    response = requests.get(URL)
    if response.status_code == 200:
        print("fetching details of staff based on Emails")
        for res in response.json()['persons']:
            email_list.append(res)

    else:
        print("Error ")
        print(response.status_code)

# Serializing json
json_object = json.dumps(email_list, indent = 4)

# Writing to sample.json
with open("emails.json", "a") as outfile:
    outfile.write(json_object)


# fetch phone list
phone_list = list()
for alpha in alphabet_list:
    URL = 'https://api.m.ox.ac.uk/contact/search?q={}&medium=phone&match=approximate'.format(alpha)
    response = requests.get(URL)
    if response.status_code == 200:
        print("fetching details of staff based on PhoneNos")
        for res in response.json()['persons']:
            phone_list.append(res)
    else:
        print("Error ")
        print(response.status_code)

# Serializing json
json_object = json.dumps(phone_list, indent = 4)

# Writing to sample.json
with open("phones.json", "a") as outfile:
    outfile.write(json_object)
