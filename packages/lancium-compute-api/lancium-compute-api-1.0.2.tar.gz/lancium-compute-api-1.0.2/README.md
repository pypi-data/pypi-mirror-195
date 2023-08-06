# lancium-library

This is the Python library for Lancium Compute's API. 

# Notes: 
* Must upgrade requests module if you are running Python 3.10 or later.

`pip3 --install --upgrade requests`

* If switching from Python3.9 and under to Python3.10 and over, must uninstall and reinstall the library with the version of pip corresponding to the version of Python you are on.

## Setting up a Lancium Compute Account

Please head to `https://portal.lancium.com/` to sign-up for a Lancium Compute account and retrieve an API key.

## Using the Python Library

Simply `pip install lancium-compute-api`.

Create an API key for your Lancium Compute account and export the key prior to using any modules like so:

`export LANCIUM_API_KEY=$KEY_FROM_WEBSITE`

## Python Modules

* `lancium.api.Job`
* `lancium.api.JobInput`
* `lancium.api.Data`
* `lancium.api.Image`
* `lancium.api.Resources`

## Lancium Compute Library / API Documentation
Documentation for the Lancium Library and API can be found here:

* https://docs.lanciumcompute.com/


## Support

Please contact support@lancium.com for support.

