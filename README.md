# nhlapi
[Documentation](https://docs.sbstp.ca/nhlapi/)

This library was created to simplify querying the NHL's API from Python. It's as simple as this:

```python
from nhlapi import NHLAPI, SyncClient

api = NHLAPI(SyncClient)
t = api.teams()
print(t)
```

See the [documentation](https://docs.sbstp.ca/nhlapi/) for more information.

## License
This library is licensed under the [Zlib license](LICENSE) which is a permissive license that permits commerical and non FOSS uses.
