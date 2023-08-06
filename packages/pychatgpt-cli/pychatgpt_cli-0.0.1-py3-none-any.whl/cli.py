#!/usr/bin/env python
import json
from pathlib import Path

import click
import openai
from rich import print


CUR = Path(__file__).parent
USER_HOME = Path('~').expanduser()


@click.command()
@click.argument("prompt")
def main(prompt):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", messages=[{"role": "user", "content": prompt}])
    print(completion.choices[0].message.content)
    with open(CUR.parent / "gptlog.txt", 'a') as f:
        f.write(json.dumps(completion))


if __name__ == '__main__':
    main()