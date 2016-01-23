# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

customerId = '56241a12de4bf40b17112139'
apiKey = '33fa62096eeddb37f6c8b4f305d51a9a'

# URL for creating a customer
url = 'http://api.reimaginebanking.com/customers?key={}'.format(apiKey)

# Currently the payload is for creating a bank account
# Grab json from Customer

payload = {
    "type": "Savings",
    "nickname": "test",
    "rewards": 10000,
    "balance": 10000,
}
# Create a Savings Account
response = requests.post(
    url,
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
)

if response.status_code == 201:
    print('Customer created')
