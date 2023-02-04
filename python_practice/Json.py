import json

# some JSON format string
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse jason into python object
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"])

# a Python object (dict):
p = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert python object into JSON:
q = json.dumps(p)

# the result is a JSON string:
print(q)

r = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

print(json.dumps(r))