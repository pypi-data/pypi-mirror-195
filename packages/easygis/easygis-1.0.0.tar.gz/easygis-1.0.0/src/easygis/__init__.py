__version__= "1.0.0"
__author__ = 'toandao'
from . import easygis

def country(country='vie'):
    return easygis.easygis(country)