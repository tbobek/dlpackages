# dlpackages

## Motivation

When working on an offline PC (perhaps in a company that has restrictions for 
online connectivity for good reasons) it is not easy to install packages 
together with all dependencies (recursively). The currently existing methods 
with synaptic download scripts are not usable from a windows office PC. This
method here only uses html pages from packages.ubuntu.com/... to determine the
dependencies, urls and the downloads. 

## Purpose 

Downloads ubuntu packages and recursively all dependend packages that can 
subsequently installed to a PC not connected to the internet. 

## Prerequisites

The script is written in python3 and makes use of some packages: 
* BeautifulSoup - for scanning the DOM tree of webpages to extract the urls of 
the different packages
* requests - to get the website contents 
* subprocess - to execute the script with all the `wget` statements
* termcolor - to print out the errors in a nice red color

## Usage

By means of the command 
```
python3 dlpackages.py packagename
```
you will get a script `packagename_dl.sh` with all wget statements. It is executed at
the end of the collecting of all sub-packages. 

Please feel free to enhance the script. 

## TODO
* generate a log of all packages that couldn't be loaded
* provide the downloading for other ubuntu versions and architectures. Currently only bionic beaver and amd64 are supported. 

