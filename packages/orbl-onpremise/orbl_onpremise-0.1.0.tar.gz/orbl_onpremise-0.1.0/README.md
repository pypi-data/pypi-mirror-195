# Python API client for ORBL on-premise API

_________________

This library is mirror of official ORBL on-premise API in terms of methods and interfaces.

For your convenience, you can make API calls using sync or async (asyncio) interface.

## Installation

```sh
pip install orbl_onpremise
```

Note that it is always recommended pinning version of your installed packages.

## Usage example (sync)

An example of how to create an origin:

```python
from orbl_onpremise import Client


if __name__ == '__main__':
    # api_token is just str with your API token
    api_token = "abcd012345"
    # Now create instance of Client. There should be only one per process.
    client = Client(base_url="http://localhost:8080", api_token=api_token)
    # Issue API request to create an origin
    client.origins.create(name="test_name")

```

Now that we have our origin created, we can create profile inside that origin:

```python
from orbl_onpremise import Client


def create_profiles_example(client: Client):
    origin_id = 1  # you can inspect response from `client.origins.create`
    with open("image.png", "rb") as f:
        response = client.profiles.create(
            image=f,
            origin_id=origin_id
        )
    print("Profiles Create Response:\n", response.json(), flush=True)


if __name__ == '__main__':
    # api_token is just str with your API token
    api_token = "abcd012345"
    # Now create instance of Client. There should be only one per process.
    client = Client(base_url="http://localhost:8080", api_token=api_token)
    # Issue API request to create a profile
    create_profiles_example(client)

```

Now that we have our origin & profile created, we can search for profile:

```python
from orbl_onpremise import Client


def search_profiles_example(client: Client):
    with open("image.png", "rb") as f:
        response = client.profiles.search(
            image=f,
            identify_asm=True
        )
    print("Profiles Search Response:\n", response.json(), flush=True)


if __name__ == '__main__':
    # api_token is just str with your API token
    api_token = "abcd012345"
    # Now create instance of Client. There should be only one per process.
    client = Client(base_url="http://localhost:8080", api_token=api_token)
    # Issue API request to search profiles
    search_profiles_example(client)

```

_For more examples and usage, please refer to the [docs](https://orbl-onpremise.github.io/orbl-onpremise-python/)._

## Development setup

To install all the development requirements:

```sh
pip install --upgrade pip
pip install poetry
poetry install --no-root
```

To run linters & test suite:

```sh
./scripts/test.sh
```

## Release History
* 0.1.0
    * Initial version of package

## License

Distributed under the MIT license. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
