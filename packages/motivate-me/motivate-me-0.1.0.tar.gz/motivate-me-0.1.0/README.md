# Motivate Me
This simple Python package leverages ChatGPT to provide motivation to help you out.

This README file serves as the package's documentation.

## Installation
Install using `pip`:

```bash
pip install motivate-me
```

## Usage
Ensure that your OpenAI key is an environmental variable. You can do this a few ways:

1. Placing it in your `.env` file and sourcing it (`. .env`)
2. Exporting the key: `export OPENAI_API_KEY="your_key"`

Assuming your OpenAI key is in your environmental variables:

```
>>> import os
>>> from motivate_me import motivate
>>> motivate(os.environ['OPEN_AI_KEY'])
Believe in yourself and your abilities, success is within your reach. Keep pushing forward with determination and watch your achievements unfold.
```

This will print out a motivational one-liner. We can change this to a quote by passing in `type = "quote"` as a parameter

```
>>> motivate(os.environ['OPEN_AI_KEY'], type = "quote")
"Don't be a pessimist, it won't work anyway!" - Yogi Berra.
```

You can also increase the number of (maximum) characters for the quote by passing in `n_words` (default: 30):

```
>>> motivate(os.environ['OPEN_AI_KEY'], n_words = 100)
```

Note that this may not necessarily give you a 100 word quote; this just increases the number of words that can be allocated in a quote.