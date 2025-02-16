## Introduction

Sakuya AC has the following features:
1. Discord Chat sync
2. G Limiter
3. Plugin Support
etc.

This guide will help you to install Sakuya AC on your server

## Quick Start Guide

1. Clone the git repository
```bash
git clone git@github.com:the-indian-dev/sakuya-ac
```

2. You will need Python 3.9 or above to run Sakuya AC
Please make sure you have correct version of Python

3. Install the dependencies

- For Windows
```bash
py -m pip install -r requirements.txt
```
- For Debian, Ubuntu etc.
```bash
sudo apt install python3-aiohttp
```
- For Arch Linux
```bash
sudo pacman -S python-aiohttp
```

4. Setup Configuration
- Open `config.py` in a text editor
- Start YSF Server and put its IP in `SERVER_HOST` and Port in `SERVER_PORT`.
  The Proxy will run at the port given at `PROXY_PORT`

5. Run the Proxy
```bash
python proxy.py
```
You can now connect to the Proxy server at the port you specified in `PROXY_PORT`

- Advanced Configuration is documented [here](/user/advanced.md)

## Installing Plugins

!> Plugins can be harmful to your computer, please install from trusted sources.
  We are NOT responsible for installing plugins from untrusted sources.

1. Download plugin from a trusted source
2. Put the plugin in the `plugins` directory
  - If the plugin is a `.py` file, put it in the `plugins` directory
  - If the plugin is a `.zip` file, extract it and put it in the `plugins` directory
3. Set the `ENABLED` variable in the plugin file to `True`
4. Run the proxy

## Reporting Issues

1. Please set logging level to `DEBUG` in `config.py`
2. Please provide the replay .yfs file for the issue
3. Provide steps to reproduce the bug
4. Start a new issue on our Github repository.
