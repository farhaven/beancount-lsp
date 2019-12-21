# Beancount LSP

This is an implementation of the [LSP](https://langserver.org) protocol for beancount files.

At the moment, the server only supports completion of account names. Pretty printing of beancount files and other similar things are not supported.

I have tested this server with a moderately large beancount file (roughly 60 transactions/month for 5 years) using `acme-lsp` and the ACME text editor.

## Requirements
* Python 3

## Setup
Create a Python virtualenv and install `beancount-lsp`s dependencies:

```shell
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

## Configuration for `acme-lsp`
I use the following configuration for `acme-lsp`:

```
ProxyNetwork = "unix"
ProxyAddress = "/tmp/ns.farhaven.:0/acme-lsp.rpc"
AcmeNetwork = "unix"
AcmeAddress = "/tmp/ns.farhaven.:0/acme"
RootDirectory = "/"
FormatOnPut = true
CodeActionsOnPut = ["source.organizeImports"]

[Servers]
	[Servers.beancount]
	Command = ["/path/to/repo/venv/bin/python", "/path/to/repo/langserver.py"]

[[FilenameHandlers]]
Pattern = '\.beancount$'
ServerKey = "beancount"
```

You will need to adjust the paths for the beancount langserver.