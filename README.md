txcloudflare
============

txcloudflare is a Python+Twisted interface to CloudFlare using the CloudFlare
client API v1.0 over HTTPS+JSON. The API documentation can be found here:

http://www.cloudflare.com/docs/client-api.html

This library is feature-complete at time of release, please see the /examples/
folder for detailed bare examples on all operations.

All operations are fully asynchronous and will be simple to anyone who is
familiar with Twisted.

If you have txverifyssl installed the CloudFlare SSL certificate will be fully
authenticated and verified. See:

https://github.com/meeb/txverifyssl

txcloudflare was Developed and tested with Python 2.7 and Twisted 11.1, although
it should work given the features used (but not tested) with Python >= 2.7 and
Twisted >= 9.0.

You can install (and use --upgrade to upgrade) the latest version via "pip"
directly from github:

```bash
$ pip install git+git://github.com/meeb/txcloudflare.git@master
```

Or you can install it manually:

```bash
$ python setup.py install
```

Please do report, fork or otherwise notify me of any bugs or issues.

CloudFlare host API support may be added if there is demand for it.
