createScanner.py

This script will parse an advanced scanner template
exported from TWS and return a scanner object that 
can be used with ibapi library.

The ElementTree XML library is used to parse the
xml template.

Script should check for included properties within 
certain tags and if they are present - add obtained 
values to scanner subscription object of ibapi.

It is expected that scanner template is used as input.
Since scanner template has extension .stp but is format
ted as xml document - changing extension to .xml is
required.

How to acquire the scanner template from TWS:

In TWS

1. Click New Window -> Scanners -> Advanced market scanner
2. Define the scan and run it to confirm if there are any
results.
3. Click on floppy-disc icon in upper-right part of the
screen to export the template

Output can be used with WEB API's scanner request also.
