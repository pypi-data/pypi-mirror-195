# Lifetimer

[![PyPI version](https://img.shields.io/pypi/v/lifetimer)](https://pypi.org/project/lifetimer/)
[![Python Versions](https://img.shields.io/pypi/pyversions/lifetimer)](https://pypi.org/project/lifetimer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a lifespan timer that allows you to watch the seconds tick down to the time you set for yourself.

It's for anyone who wants to feel the time dwindle, push themselves to get up to speed on their studies and work.

## Installation

```sh
pip install lifetimer
```

## Usage

When installed, you have to set your last date and time of your life through `lifetimer` or `lifetimer init` commands.

If you want to change the settings, use `lifetimer init` command.

```sh
$ lifetimer init
Please, enter your last date and time of your life.
Year: 2100
Month [12]: 3
Day [31]: 6
Hour [23]: 17
Minute [59]: 58
Second [59]: 50
```

After settings, when you want to check your lifespan, just type `lifetimer` command.

```sh
$ lifetimer
🕛 You have 2,455,857,087 seconds to live.
```
