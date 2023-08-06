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
 'tiktoken>=0.2.0,<0.3.0',
 'turbo-text-transformer-prompts>=0.1.8,<0.2.0']

entry_points = \
{'console_scripts': ['ttt = ttt.__main__:main']}

setup_kwargs = {
    'name': 'turbo-text-transformer',
    'version': '0.1.6',
    'description': '',
    'long_description': '# Turbo Text Transformer\n\nTurbo Text Transformer is a Python command-line tool for generating text using OpenAI\'s GPT-3 and other models. It includes a modular model system that allows for easy integration of new models and customization of existing ones.\n\nIncludes templates, look in the [Turbo Text Transformer Prompts](https://github.com/fergusfettes/turbo-text-transformer-prompts) repository for more documentation and to find a list of the templates!\n\n## Installation\n\nTo install Turbo Text Transformer, you can use pip:\n\n```sh\npip install turbo-text-transformer\n```\n\nor clone the repository and install it manually:\n\n```sh\ngit clone https://github.com/fergusfettes/turbo-text-transformer.git\ncd turbo-text-transformer\npoetry install\n```\n\n## Usage\n\nThe basic syntax for running TTT is as follows:\n\n```bash\nttt <prompt> [options]\n```\n\nHere, `<prompt>` is the text that you want to transform. You can use the `--prompt_file` option to load the prompt from a file instead of typing it out on the command line, or you can cat some text in:\n\n```\ncat some_file.txt | ttt\n```\n\nfor example, to generate this readme I did\n\n```\ncat pyproject.toml ttt/__main__.py | ttt -t readme > README.md\n```\n\nwhere I\'m using the \'readme\' template, which is a template for generating a readme file.\n\n### Options\n\nThere are several options you can use with the `ttt` command:\n\n- `--format/-f`: Output format (default: "clean"). Valid options are "clean", "json", or "logprobs".\n- `--echo_prompt/-e`: Echo the prompt in the output.\n- `--list_models/-l`: List available models.\n- `--prompt_file/-P`: File to load for the prompt.\n- `--template_file/-t`: Template file to apply to the prompt.\n- `--template_args/-x`: Extra values for the template.\n- `--chunk_size/-c`: Max size of chunks.\n- `--summary_size/-s`: Size of chunk summaries.\n- `--model/-m`: Name of the model to use (default: "gpt-3.5-turbo").\n- `--number/-N`: Number of completions.\n- `--logprobs/-L`: Show logprobs for completion.\n- `--max_tokens/-M`: Max number of tokens to return.\n- `--temperature/-T`: Temperature, [0, 2]-- 0 is deterministic, >0.9 is creative.\n- `--force/-F`: Force chunking of prompt.\n\n## Configuration\n\nBefore using Turbo Text Transformer, you need to set up a configuration file. This should happen automatically when you run the `ttt` command for the first time.\n\nThis will create a configuration file in your home directory. See the documentation for each model to learn how to obtain an API key.\n\n```~/.config/ttt/openai.yaml\napi_key: sk-<your api key here>\nengine_params:\n  frequency_penalty: 0\n  logprobs: null\n  max_tokens: 1000\n  model: davinci\n  n: 4\n  presence_penalty: 0\n  stop: null\n  temperature: 0.9\n  top_p: 1\nmodels:\n- babbage\n- davinci\n- gpt-3.5-turbo-0301\n- text-davinci-003\netc.\n```\n\n## Examples\n\nHere are some examples of how to use Turbo Text Transformer:\n\n```\n# Generate text with the default model\nttt "Once upon a time, there was a"\n\n# Generate text with a specific model\nttt -m text-davinci-003 "The meaning of life is"\n\n# Generate multiple completions\nttt -n 5 "I like to eat"\n\n# Show logprobs\nttt "I like to eat" -f logprobs\n\n# Use the JSON format\nttt -f json "I like to eat"\n```\n\nIf you put in the \'logprobs\' flag, it will try to color the terminal output based on the logprobs. This is a bit janky at the moment.\n\nYou can also tell it to output a formatted json file with the `-f json` flag. This is useful for piping into other programs.\n\n```\nttt -f json "The cat sat on the"\n```\n\nIf you want to input more text freely, just use it without a prompt and you can write or paste directly into stdin.\n\n## Chunking\n\nIf you dump in a tonne of text, it will try to chunk it up into smaller pieces:\n\n```\ncat song-of-myself.txt | ttt -t poet -x \'poet=Notorious B.I.G.\' > song_of_biggie.txt\n```\n\n(Note, this is an incredibly wasteful way to extract the text from a website, but at current prices should only cost ~$0.30 so, unhinged as it its, its probably about parity with clicking and dragging.)\n\n### Models\n\nTurbo Text Transformer includes support for text generation with all the openai models. Have a look at the model list with `ttt -l`.\n\n## Contributing\n\nIf you find a bug or would like to contribute to Turbo Text Transformer, please create a new GitHub issue or pull request.\n\n## Inspiration/Similar\n\nInspired by [Loom](https://github.com/socketteer/loom) (more to come on this front-- aiming for a command-line-loom)\nand [Shell-GPT](https://github.com/TheR1D/shell_gpt) (very similar, but I have a lot more features and support for catting)\n\n## License\n\nTurbo Text Transformer is released under the MIT License. See `LICENSE` for more information.\n',
    'author': 'fergus',
    'author_email': 'fergusfettes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fergusfettes/turbo-text-transformer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.8',
}


setup(**setup_kwargs)
