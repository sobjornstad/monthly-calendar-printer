Monthly LaTeX Calendar README

A simple command-line utility to generate blank, full-page monthly calendars
for printing and posting on your fridge, bulletin board, or desk.

Requirements & Dependencies
===========================

* Python 2.7 series
* Some distribution of LaTeX, and the packages geometry, mathpazo, microtype,
  and tabularx.
* Some kind of PDF viewer; the script will try to open the PDF in whatever
  program is associated with PDF files on your system (using xdg-open on
  Linux).


Running
=======

Usage is `python genday.py YEAR [OUTPUT_FILENAME]`. The year should be an integer such as `2015`. The output filename is optional; if omitted, your PDF viewer will be opened on a temporary file so you can print and then discard it.


Problems? Bugs?
================

Please send mail to `contact@sorenbjornstad.com`.
