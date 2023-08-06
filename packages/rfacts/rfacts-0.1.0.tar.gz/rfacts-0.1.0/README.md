# rfacts
### a very simple wrapper around requests/aiohttp for uselessfacts.jsph.pl
#### provides 1 object that implements 2 methods, and 5 attributes.
&nbsp;
### the `fact` classmethods `get` and `aget` each take one argument, and return a `fact` instance:
* #### `language` - Type[str] - the language for the fact to be fetched, can be `en` or `de`
&nbsp;
### each instance of `fact` has the following attributes:
* #### `id` - Type[str] - the id of the fact
* #### `source` - Type[str] - the source for the fact
* #### `permalink` - Type[str] - the permanent link to this fact
* #### `text` - Type[str] - the text of the fact itself
* #### `language` - Type[str] - the language of the fact
* #### `_raw` - Type[dict] - the raw json returned from the api
&nbsp;
### examples:
```
from rfacts import fact

def main() -> None:
    x = fact.get()
    print(x.text)

if __name__ == "__main__":
    main()
```

```
from rfacts import fact
import asyncio

async def main() -> None:
    x = await fact.aget()
    print(x.text)

if __name__ == "__main__":
    asyncio.run(main())
```