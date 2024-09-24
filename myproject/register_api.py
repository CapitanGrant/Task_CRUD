from requests import post

url = "http://127.0.0.1:8000/api/register/"
data = {
    "title": "Pay water",
    "description": "Magnit",
    "completed": "False",
}

response = post(url, data=data)

if response.status_code == 201:
    print("Task created successfully:", response.json())
else:
    print("Error:", response.json())
