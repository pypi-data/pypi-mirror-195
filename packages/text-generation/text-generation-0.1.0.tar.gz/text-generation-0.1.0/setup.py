# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_generation']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0',
 'huggingface-hub>=0.12.1,<0.13.0',
 'pydantic>=1.10.5,<2.0.0']

setup_kwargs = {
    'name': 'text-generation',
    'version': '0.1.0',
    'description': 'Hugging Face Text Generation Python Client',
    'long_description': '# Text Generation\n\nThe Hugging Face Text Generation Python library provides a convenient way of interfacing with a\n`text-generation-inference` instance running on your own infrastructure or on the Hugging Face Hub.\n\n## Get Started\n\n### Install\n\n```shell\npip install text-generation\n```\n\n### Usage\n\n```python\nfrom text_generation import InferenceAPIClient\n\nclient = InferenceAPIClient("bigscience/bloomz")\ntext = client.generate("Why is the sky blue?").generated_text\nprint(text)\n# \' Rayleigh scattering\'\n\n# Token Streaming\ntext = ""\nfor response in client.generate_stream("Why is the sky blue?"):\n    if not response.token.special:\n        text += response.token.text\n\nprint(text)\n# \' Rayleigh scattering\'\n```\n\nor with the asynchronous client:\n\n```python\nfrom text_generation import InferenceAPIAsyncClient\n\nclient = InferenceAPIAsyncClient("bigscience/bloomz")\nresponse = await client.generate("Why is the sky blue?")\nprint(response.generated_text)\n# \' Rayleigh scattering\'\n\n# Token Streaming\ntext = ""\nasync for response in client.generate_stream("Why is the sky blue?"):\n    if not response.token.special:\n        text += response.token.text\n\nprint(text)\n# \' Rayleigh scattering\'\n```\n',
    'author': 'Olivier Dehaene',
    'author_email': 'olivier@huggingface.co',
    'maintainer': 'Olivier Dehaene',
    'maintainer_email': 'olivier@huggingface.co',
    'url': 'https://github.com/huggingface/text-generation-inference',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
