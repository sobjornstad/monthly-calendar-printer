#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Monthly LaTeX calendar - Print simple blank monthly calendars using LaTeX
# Copyright (c) 2015 Soren Bjornstad.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import calendar
import os
import shutil
import subprocess
import sys
import tempfile
import time


##### Constants #####
THE_MONTHS = ("January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December")

LATEXHEADER = r"""
\documentclass{article}
\usepackage[landscape, margin=0.5in]{geometry}
\usepackage{mathpazo}
\usepackage[letterspace=50]{microtype}
\usepackage{tabularx}

\newcommand{\dayformat}[1]{\hfil{{#1}}\hfil}
\newcommand{\daytitles}{
  \dayformat{Sunday} & \dayformat{Monday} & \dayformat{Tuesday} &
  \dayformat{Wednesday} & \dayformat{Thursday} & \dayformat{Friday} &
  \dayformat{Saturday}\\\hline
}
\newcommand{\cday}[1]{\hfill\textbf{#1}}
\newcommand{\monthtop}[1]{{\Huge #1}\smallskip}
\newcommand{\monthbottom}[1]{\smallskip\hfill{\Huge #1}}

\setlength\parindent{0pt}
\pagestyle{empty}

\begin{document}
\Large
"""

LATEXFOOTER = r"""
\end{document}
"""

LATEXINNER = r"""
\monthtop{%s}\par
\begin{tabularx}{\textwidth}{|X|X|X|X|X|X|X|}\hline
  \daytitles
%s
\end{tabularx}\par
\monthbottom{%s}
\clearpage
"""

def usage_msg():
    print("""Monthly LaTeX calendar
Copyright (c) 2015, 2018 Soren Bjornstad.
MIT license; see source for details.

Usage: genday YEAR [OUTPUT FILENAME]
If an output filename is omitted, the calendar will be created in a
temporary folder and opened directly in your PDF viewer.""")


##### Begin main code #####
# parse arguments
if not 2 <= len(sys.argv) <= 3:
    usage_msg()
    sys.exit(1)
try:
    year = int(sys.argv[1])
except ValueError:
    usage_msg()
    sys.exit(1)
if len(sys.argv) == 3:
    target = sys.argv[2]
else:
    target = None

# build LaTeX code
monthTables = []
for month in range(1,13):
    startday, largestDay = calendar.monthrange(year, month)
    blanks = startday + 1 # in startday, 0 = Monday
    blanks = 0 if blanks == 7 else blanks

    # calculate how far we will go beyond the end of a five-week calendar
    # (0-2 days)
    numOverflows = largestDay - 28 - (7-blanks)
    numOverflows = 0 if numOverflows < 0 else numOverflows

    days = []
    for i in range(blanks):
        days.append(r"&")

    # following check: if blanks == 0, row will be incremented as soon as we
    # start the loop, as the onCol condition will be met
    row = -1 if blanks == 0 else 0
    clineIsAdded = False

    # For each day in the month...
    for i in range(1, largestDay+1):
        # increment row counter if we're on Sunday
        onCol = ((blanks + i-1) % 7)
        if onCol == 0:
            row += 1

        # add division line (e.g., between 24/31) if we're on the overflow row
        if row == 5 and not clineIsAdded:
            days.append(r"\cline{1-%i}" % numOverflows)
            clineIsAdded = True

        # Now output this day (or potentially more).
        if i == largestDay:
            # We've reached the end of the calendar; pad out with &.
            days.append(r"\cday{%i} " % i)
            left = 7 - ((i + blanks) % 7)
            if left != 7: # if left is 7, then really there are none left
                for i in range(left):
                    days.append("&")
            if row == 3:
                # In this obscure case, February starts on a Sunday and is not
                # a leap year; we need a blank row to match other months' size.
                days.append(r"\\[1in]\hline&&&&&&\\[1in]\hline")
                break
            # smaller skip if there will need to be an overflow row added
            if row >= 4 and numOverflows > 0:
                days.append(r"\\[0.375in]\hline")
            else:
                days.append(r"\\[1in]\hline")
        elif (i + blanks) % 7: # in the middle of a row; add day
            days.append(r"\cday{%i} &" % i)
        else: # at the end of a row; add day and line break
            days.append(r"\cday{%i}\\" % i)
            if row >= 4 and numOverflows > 0:
                # Don't add an hline! We add the section we need with \cline.
                days.append(r"[0.375in]")
            else:
                days.append(r"[1in]\hline")
            days.append('\n')

    # Add this month's LaTeX code to the list.
    monthTables.append(''.join(days))


# Create a temporary file, write LaTeX code to it, call LaTeX, and open the
# resulting PDF file in a previewer.
tdir = tempfile.mkdtemp()
oldcwd = os.getcwd()
os.chdir(tdir)

fnamebase = "index"
tfile = os.path.join(tdir, '.'.join([fnamebase, 'tex']))
with open(tfile, 'w') as f:
    f.write(LATEXHEADER)
    for i in range(len(monthTables)):
        monthStr = THE_MONTHS[i] + " " + str(year)
        f.write(LATEXINNER % (monthStr, monthTables[i], monthStr))
    f.write(LATEXFOOTER)
r = subprocess.call(['pdflatex', tfile])
if r:
    print("Error executing latex! Please see the error above.")
    sys.exit(2)

ofile = os.path.join(tdir, '.'.join([fnamebase, 'pdf']))

if target is None:
    if sys.platform.startswith('linux'):
        subprocess.call(["xdg-open", ofile])
    elif sys.platform == "darwin":
        os.system("open %s" % ofile)
    elif sys.platform == "win32":
        os.startfile(ofile)
    else:
        print("Unable to automatically open the output. Please"
              "browse manually to %s." % ofile)
    os.chdir(oldcwd)
    time.sleep(5) # give time for PDF viewer to open file
    shutil.rmtree(tdir, True)
else:
    shutil.copy(ofile, target)
    shutil.rmtree(tdir, True)
