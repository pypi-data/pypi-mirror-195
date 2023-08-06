# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['openai_python_cache']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.0,<0.28.0']

setup_kwargs = {
    'name': 'openai-python-cache',
    'version': '0.1.0',
    'description': 'A thin cache wrapper around the OpenAI Python bindings.',
    'long_description': '# openai_python_cache\n\nA thin cache wrapper around the OpenAI Python bindings.\n\n## Motivation\n\nI\'m experimenting with a large-ish dataset locally that gets injected into GPT\nprompts. Responses are not perfect, and occassionally I have to tweak some\nof my data. This means that I\'m making API calls for results that are okay,\nbecause it\'s iterating over the entire dataset.\n\nThis solves the issue by cache-ing OpenAI responses in a local SQLite3 database.\n**Only ChatCompletion is supported** at this time because it\'s the only API I use.\n\nThis is a quick and dirty solution. I\'d go a level lower and inject this\nbehaviour directly in the requestor, but I don\'t have time to figure that\npart out (yet?)!\n\n## Installation\n\n```sh\n# Using pip:\n$ pip install openai_python_cache\n\n# Using poetry:\n$ poetry add openai_python_cache\n```\n\n## Usage\n\n```python\nimport os\nimport openai\nfrom openai_python_cache.api import ChatCompletion\nfrom openai_python_cache.provider import Sqlite3CacheProvider\n\nopenai.api_key = os.environ.get("OPENAI_API_KEY")\n\n# Create a cache provider\ncache_provider = Sqlite3CacheProvider()\n\n# Use the ChatCompletion class from `openai_python_cache`\ncompletion = ChatCompletion.create(\n    model="gpt-3.5-turbo",\n    messages=[\n        {\n            "role": "user",\n            "content": "Tell the world about the ChatGPT API in the style of a pirate.",\n        }\n    ],\n    # Inject the cache provider. Requests will NOT be cached if this is not\n    # provided!\n    cache_provider=cache_provider,\n)\n\nprint(completion)\n```\n\n## Demo\n\n```python\nimport os\nimport time\nimport openai\nfrom openai_python_cache.api import ChatCompletion\nfrom openai_python_cache.provider import Sqlite3CacheProvider\n\nopenai.api_key = os.environ.get("OPENAI_API_KEY")\n\ncache_provider = Sqlite3CacheProvider()\n\nparams = {\n    \'model\': "gpt-3.5-turbo",\n    \'messages\': [\n        {\n            "role": "user",\n            "content": "Testing cache!",\n        }\n    ]\n}\n\n# First request, cache miss. This will result in an API call to OpenAI, and\n# the response will be saved to cache.\nc0start = time.time()\nChatCompletion.create(cache_provider, **params)\nc0end = time.time() - c0start\nprint(f"First request is a cache miss. It took {c0end} seconds!")\n# >>> First request is a cache miss. It took 1.7009928226470947 seconds!\n\n# Second request, cache hit. This will NOT result in an API call to OpenAI.\n# The response will be served from cache.\nc1start = time.time()\nChatCompletion.create(cache_provider, **params)\nc1end = time.time() - c1start\nprint(f"Second request is a cache hit. It took {c1end} seconds!")\n# >>> Second request is a cache hit. It took 0.00015616416931152344 seconds!\n```\n',
    'author': 'Ray Chen',
    'author_email': 'ray@raychen.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
