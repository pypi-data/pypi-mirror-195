# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turbo_chat']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0',
 'openai>=0.27.0,<0.28.0',
 'pydantic>=1.10.5,<2.0.0',
 'tenacity>=8.2.2,<9.0.0']

setup_kwargs = {
    'name': 'turbo-chat',
    'version': '0.1.1',
    'description': 'Idiomatic way to build chatgpt apps using async generators in python',
    'long_description': '# turbo-chat\n\n> Idiomatic way to build chatgpt apps using async generators in python\n\n## Installation\n\n```bash\npip install turbo-chat\n```\n\n## Example\n\n```python\nfrom turbo_chat import *\n\n# Horoscope app\n@turbo()\nasync def horoscope(context: dict):\n\n    yield System(content="You are a fortune teller")\n    yield User(content=f"My zodiac sign is {context[\'zodiac\']}")\n\n    input = yield GetUserInput(message="What do you want to know?")\n    yield User(content=input)\n\n    value = yield Generate(settings={"temperature": 0.9})\n    print(f"generated: {value}")\n\n# Testing\napp = horoscope({"zodiac": "pisces"})\n\noutput, done = await run(app)\nassert isinstance(output, GetUserInput)\nassert not done\n\nuser_input = "Tell me my fortune"\noutput, done = await run(app, user_input)\nassert isinstance(output, str)\nassert done\n```\n\n![turbo](https://user-images.githubusercontent.com/931887/222912628-8662fad0-091f-4cb8-92f3-6cce287716e9.jpg)\n',
    'author': 'Diwank Singh Tomer',
    'author_email': 'singh@diwank.name',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
