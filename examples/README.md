txcloudflare examples
=====================

These examples require valid CloudFlare account details to be stored in
environment variables to complete. For example under any decent *NIX shell:

```bash
$ export TXCFEMAIL="email@address"
$ export TXCFAPI="apitoken"
```

Some of the examples additionally require a zone/domain name to work with:

```bash
$ export TXCFDOMAIN="somedomain.com"
```

The tests will interact with the live account specified in the environment
variables. It is not advised to play with these examples on a live account
unless you know what you're doing.

Once txcloudflare is installed and the environment variables are set you can run
any of examples from the command line, for example:

```bash
$ python zone_list.py
```
