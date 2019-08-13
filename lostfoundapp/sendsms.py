import requests
url = "https://www.fast2sms.com/dev/bulk"
payload = "sender_id=FSTSMS&message=test&language=english&route=p&numbers=9442066341,9487266341"
headers = {
'authorization': "OfXT3txn4D8LCmqaZlwB7dcoePNVWJibhFRugv9EHAIySQ1zG6rdQBNTMhIYl1K8Xg93tPaAs0xnRFpy",
'Content-Type': "application/x-www-form-urlencoded",
'Cache-Control': "no-cache",
}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)