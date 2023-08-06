## How to use

```python
from python_hbk.Hbk import Hbk

my_hbk = Hbk("test.hbk")
for name, address, length in my_hbk.get_bookmarks():
    print(f"{name=}, {address=}, {length=}")

print(my_hbk.to_json())
```

## Output
```
name='Test float', address='0000016A', length=4
name='Test double', address='0000016E', length=8
name='Test string', address='00000176', length=72
name='Test float array [0]', address='00000241', length=4
...
name='Test double array [15]', address='000002C7', length=8

[
  {
    "name": "Test float",
    "address": "0000016A",
    "length": 4
  },
  {
    "name": "Test double",
    "address": "0000016E",
    "length": 8
  },
  {
    "name": "Test string",
    "address": "00000176",
    "length": 72
  },
  {
    "name": "Test float array [0]",
    "address": "00000241",
    "length": 4
  },
  ...
  {
    "name": "Test double array [15]",
    "address": "000002C7",
    "length": 8
  }
]

```