createScanner.py

This script will parse an advanced scanner template
exported from TWS and return a scanner object that 
can be used with Scanner object of ibapi library.

The ElementTree XML library is used to parse the
xml template.

Script assigns values of specific tags as properties
for Scanner object and checks if there are additional
filters.

It is expected that default extensio of a template
.stp is changed to .xml manually.

How to acquire the scanner template from TWS:

In TWS

1. Click New Window -> Scanners -> Advanced market scanner
2. Define the scan and run it to confirm if there are any
results.
3. Click on floppy-disc icon in upper-right part of the
screen to export the template

Output can be used with WEB API's scanner request also.
