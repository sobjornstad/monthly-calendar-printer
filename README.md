A simple command-line utility to generate blank, full-page monthly calendars
for printing and posting on your fridge, bulletin board, or desk.

Requirements & Dependencies
===========================

* Python 2.7+ or 3
* Some distribution of LaTeX, with `pdflatex` available on the system path,
  and the packages `geometry`, `mathpazo`, `microtype`, and `tabularx`.
* Some kind of PDF viewer; the script will try to open the PDF in whatever
  program is associated with PDF files on your system (using xdg-open on
  Linux).


Running
=======

Usage is `python genday.py YEAR [OUTPUT FILENAME]`.
If you make the file executable, you can also use `./genday.py`.
The year should be an integer such as `2015`.
The output filename is optional;
    if omitted, your PDF viewer will be opened on a temporary file
    so you can print and then discard it.


Problems? Bugs?
================

Please send mail to `contact@sorenbjornstad.com` or create a GitHub issue.
