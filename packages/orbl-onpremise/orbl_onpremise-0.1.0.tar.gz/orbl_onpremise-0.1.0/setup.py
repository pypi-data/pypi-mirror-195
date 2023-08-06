# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orbl_onpremise',
 'orbl_onpremise.asm',
 'orbl_onpremise.auth',
 'orbl_onpremise.compare',
 'orbl_onpremise.entries',
 'orbl_onpremise.groups_profiles',
 'orbl_onpremise.licenses',
 'orbl_onpremise.liveness',
 'orbl_onpremise.origins',
 'orbl_onpremise.profiles',
 'orbl_onpremise.spaces',
 'orbl_onpremise.statistics',
 'orbl_onpremise.tokens',
 'orbl_onpremise.tokens.access',
 'orbl_onpremise.tokens.streams',
 'orbl_onpremise.users',
 'orbl_onpremise.whoami']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0', 'websockets>=10.0,<11.0']

setup_kwargs = {
    'name': 'orbl-onpremise',
    'version': '0.1.0',
    'description': 'A Python package for interacting with ORBL on-premise API',
    'long_description': '# Python API client for ORBL on-premise API\n\n_________________\n\nThis library is mirror of official ORBL on-premise API in terms of methods and interfaces.\n\nFor your convenience, you can make API calls using sync or async (asyncio) interface.\n\n## Installation\n\n```sh\npip install orbl_onpremise\n```\n\nNote that it is always recommended pinning version of your installed packages.\n\n## Usage example (sync)\n\nAn example of how to create an origin:\n\n```python\nfrom orbl_onpremise import Client\n\n\nif __name__ == \'__main__\':\n    # api_token is just str with your API token\n    api_token = "abcd012345"\n    # Now create instance of Client. There should be only one per process.\n    client = Client(base_url="http://localhost:8080", api_token=api_token)\n    # Issue API request to create an origin\n    client.origins.create(name="test_name")\n\n```\n\nNow that we have our origin created, we can create profile inside that origin:\n\n```python\nfrom orbl_onpremise import Client\n\n\ndef create_profiles_example(client: Client):\n    origin_id = 1  # you can inspect response from `client.origins.create`\n    with open("image.png", "rb") as f:\n        response = client.profiles.create(\n            image=f,\n            origin_id=origin_id\n        )\n    print("Profiles Create Response:\\n", response.json(), flush=True)\n\n\nif __name__ == \'__main__\':\n    # api_token is just str with your API token\n    api_token = "abcd012345"\n    # Now create instance of Client. There should be only one per process.\n    client = Client(base_url="http://localhost:8080", api_token=api_token)\n    # Issue API request to create a profile\n    create_profiles_example(client)\n\n```\n\nNow that we have our origin & profile created, we can search for profile:\n\n```python\nfrom orbl_onpremise import Client\n\n\ndef search_profiles_example(client: Client):\n    with open("image.png", "rb") as f:\n        response = client.profiles.search(\n            image=f,\n            identify_asm=True\n        )\n    print("Profiles Search Response:\\n", response.json(), flush=True)\n\n\nif __name__ == \'__main__\':\n    # api_token is just str with your API token\n    api_token = "abcd012345"\n    # Now create instance of Client. There should be only one per process.\n    client = Client(base_url="http://localhost:8080", api_token=api_token)\n    # Issue API request to search profiles\n    search_profiles_example(client)\n\n```\n\n_For more examples and usage, please refer to the [docs](https://orbl-onpremise.github.io/orbl-onpremise-python/)._\n\n## Development setup\n\nTo install all the development requirements:\n\n```sh\npip install --upgrade pip\npip install poetry\npoetry install --no-root\n```\n\nTo run linters & test suite:\n\n```sh\n./scripts/test.sh\n```\n\n## Release History\n* 0.1.0\n    * Initial version of package\n\n## License\n\nDistributed under the MIT license. See ``LICENSE`` for more information.\n\n## Contributing\n\n1. Fork it (<https://github.com/yourname/yourproject/fork>)\n2. Create your feature branch (`git checkout -b feature/fooBar`)\n3. Commit your changes (`git commit -am \'Add some fooBar\'`)\n4. Push to the branch (`git push origin feature/fooBar`)\n5. Create a new Pull Request\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
