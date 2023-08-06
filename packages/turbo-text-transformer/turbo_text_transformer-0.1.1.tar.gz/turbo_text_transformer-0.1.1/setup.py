# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ttt']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'colored>=1.4.4,<2.0.0',
 'openai>=0.27.0,<0.28.0',
 'pyyaml>=6.0,<7.0',
 'tiktoken>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['ttt = ttt.__main__:main']}

setup_kwargs = {
    'name': 'turbo-text-transformer',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Turbo Text Transformer\n\nTurbo Text Transformer is a Python command-line tool for generating text using OpenAI\'s GPT-3 and other models. It includes a modular model system that allows for easy integration of new models and customization of existing ones.\n\nBest used in combination with the [Turbo Text Transformer Prompts](https://github.com/fergusfettes/turbo-text-transformer-prompts) repository!\n\n## Configuration\n\nConfigs are in the `.config` folder, put your api key in there\n\n```~/.config/ttt/openai.yaml\napi_key: sk-<your api key here>\nengine_params:\n  frequency_penalty: 0\n  logprobs: null\n  max_tokens: 1000\n  model: davinci\n  n: 4\n  presence_penalty: 0\n  stop: null\n  temperature: 0.9\n  top_p: 1\nmodels:\n- babbage\n- davinci\n- gpt-3.5-turbo-0301\n- text-davinci-003\netc.\n```\n\n## Installation\n\nTo install Turbo Text Transformer, you can use pip:\n\n```sh\npip install turbo-text-transformer\n```\n\nor clone the repository and install it manually:\n\n```sh\ngit clone https://github.com/fergusfettes/turbo-text-transformer.git\ncd turbo-text-transformer\npoetry install\n```\n\n## Usage\n\nYou can use Turbo Text Transformer by running the `ttt` command in your terminal:\n\n```sh\nttt --model davinci --prompt "Hello, GPT-3!"\n```\n\nThe above example will generate text using the davinci model and the prompt "Hello, GPT-3!".\n\n### Options\n\nThere are several options you can use with the `ttt` command:\n\n* `--model` or `-m`: The name of the model to use. Default is "davinci".\n* `--prompt` or `-p`: The prompt to use for text generation.\n* `--list_models` or `-l`: List available models.\n- `--echo_prompt, -e`: Whether to echo the prompt in the output.\n- `--format, -f FORMAT`: The format of the output. Can be "clean", "json", or "logprobs". Defaults to "clean".\n- `--number, -n NUMBER`: The number of completions to generate. Defaults to 1.\n- `--logprobs, -L LOGPROBS`: Whether to show logprobs for each completion. Defaults to False.\n- `--max_tokens, -M MAX_TOKENS`: The maximum number of tokens to return. Defaults to None.\n\n## Configuration\n\nBefore using Turbo Text Transformer, you need to set up a configuration file. This should happen automatically when you run the `ttt` command for the first time:\nThis will create a configuration file in your home directory. You\'ll also be prompted to enter API keys for the transformer models you want to use. See the documentation for each model to learn how to obtain an API key.\n\n## Examples\n\nHere are some examples of how to use Turbo Text Transformer:\n\n```\n# Generate text with the default model\nttt -p "Once upon a time, there was a"\n\n# Generate text with a specific model\nttt -m gpt-2-medium "The meaning of life is"\n\n# Generate multiple completions\nttt -n 5 "I like to eat"\n\n# Show logprobs\nttt -L 1 "I like to eat"\n\n# Use the JSON format\nttt -f json "I like to eat"\n```\n\nYou can also tell it to output a formatted json file with the `-f json` flag. This is useful for piping into other programs.\n\n```\nttt -f json "The cat sat on the"\n```\n\nand you can pipe txt in-- for example, I generated this readme with the following command:\n\n```\ncat pyproject.toml ttt/__main__.py | tttp -f readme | ttt -m gpt-3.5-turbo -f clear > README.md\n```\n\nIf you want to input more text freely, just use it without a prompt and you can write or paste directly into stdin.\n\n### Models\n\nTurbo Text Transformer includes support for text generation with all the openai models. Have a look at the model list with `ttt -l`.\n\n## Contributing\n\nIf you find a bug or would like to contribute to Turbo Text Transformer, please create a new GitHub issue or pull request.\n\n## License\n\nTurbo Text Transformer is released under the MIT License. See `LICENSE` for more information.\n',
    'author': 'fergus',
    'author_email': 'fergusfettes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
