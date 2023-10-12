import json
data = {
    "name" : "John Doe",
    "age"  : 38,
    "city" : "New York"
}

print(json.dumps(data))
print(json.dumps({123.123 : 123}))
