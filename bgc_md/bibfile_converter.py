#!/usr/bin/python3
# vim:set ff=unix expandtab ts=4 sw=4:
"""
Usage: bibfile_converter.py [options] input_file output_file mode

Convert a raw BibTeX file (input_file) to a clean one (output_file) formatted by 'mode', useless tags are omitted.
! Check output_file and edit it manually if neccessary. !
! Tag manually edited entries with '_edited = {true}' in the output_file to keep them untouched. !

Values for 'mode':
    plain: do not change the format
    BibTeX (default): convert entries to BibTeX format
    BibLaTeX: convert entries to BibLaTeX format

Options:
    -h: show this help
"""

import re
import getopt, sys # instead of getopt also argparse possible
# from bibtexc import * # leaves out module's private methods (_method_name)
import bibtexc
from bibtexc import DoiNotFoundException
from string import *


# get the command line parameters and options
try:
    (options, arguments) = getopt.getopt(sys.argv[1:], 'h')
except getopt.GetoptError:
    print("\nInvalid option.")
    print(__doc__)
    raise SystemExit(0)

# check if help is called
if ('-h', '') in options:
    print(__doc__)
    raise SystemExit(0)

try:
    input_file = arguments[0]
    output_file = arguments[1]
    mode = arguments[2]
except IndexError:
    print("\nCommand line argument missing.")
    print(__doc__) 
    raise SystemExit(0)

# check if mode is set correct
if mode not in ('plain', 'BibTeX', 'BibLaTeX'):
    print("\nInvalid value for mode: " + mode)
#    print("Using mode=BibTeX by default")
#    mode = "BibTeX"
    print(__doc__)
#    raise SystemExit(0)

# read in output file (if it exists) and save the entries that contain '_edited' tag to keep manually edited entries unchanged
edited_entries_dict = {}
original_entries_keys = []
try:
    bibtex_entry_list_original = bibtexc.entry_list_from_file(output_file, nochanges=True)
    for bibtex_entry in bibtex_entry_list_original:
        original_entries_keys.append(bibtex_entry.key)
        if '_edited' in bibtex_entry.entry.keys():
            print("Keeping manually edited entry: " + bibtex_entry.key)
            # dictionary stores entries to keep: key -> whole entry
            edited_entries_dict[bibtex_entry.key] = bibtex_entry
        if '_attention' in bibtex_entry.entry.keys():
            print("Attention at entry " + bibtex_entry.key + ": " + bibtex_entry.entry['_attention'])
except FileNotFoundError:
    pass

# read in input file (if it exists)
try:
    bibtex_entry_list = bibtexc.entry_list_from_file(input_file)
except FileNotFoundError:
    print("\nInput file not found.\n")
    raise SystemExit(0)

# count processed and untouched entries and entries without doi
processed = 0
untouched = 0
no_doi = 0
for index, bibtex_entry in enumerate(bibtex_entry_list):
    # if entry was manually edited, keep it, otherwise build a new one
    if bibtex_entry.key in edited_entries_dict.keys():
        bibtex_entry_list[index] = edited_entries_dict[bibtex_entry.key]
        untouched +=1
    else:
        # if doi tag given then get entry online, otherwise just process the one from the input file
        processed += 1
        if 'doi' in bibtex_entry.entry.keys(): # doi given
            # convert potentially wrong doi = 'http://*' to correct doi = '10.*'
            regexp = re.compile(r"(?P<doi>(10\.).*$)") 
            result = regexp.search(bibtex_entry.entry['doi'])
            if result:
                bibtex_entry.entry['doi'] = result.group('doi')

            # try to retrieve entry online by doi
            try:
                # save the key given in the input file to restore it after fetching the new entry by doi changed it
                save_key =  bibtex_entry.key

                new_bibtex_entry = bibtexc.BibtexEntry(doi=bibtex_entry.entry['doi'])
                bibtex_entry = new_bibtex_entry

                # restore saved key
#                print(bibtex_entry.key + "  " + save_key)
                if save_key and save_key != "default":
                    bibtex_entry.set_key(save_key)
            except DoiNotFoundException:
                # doi not found online
                # delete doi entry, because probably invalid doi
                # announce entry with this doi

                print("\n--- Entry could not be found online by DOI " + bibtex_entry.entry['doi'] +" ---\n")
                print(bibtex_entry.entry)
                print("\n--- End entry ---")
                del bibtex_entry.entry['doi']
        else:
            no_doi += 1

        bibtex_entry_list[index] = bibtex_entry

# write output file
bibtexc.entry_list_to_file(output_file, bibtex_entry_list, mode)

print("\n%d entries processed to %s style." % (processed, mode))
print("Additional %d manually edited entries left untouched." % (untouched))
print("%d entries had no 'doi' tag and were not fetched online." % (no_doi))
print("\nTotal entries in %s: %d\n" % (output_file, processed + untouched))

trunk = output_file.split(".",1)[0]
with open(trunk + '_test.tex', 'w')as f:
    f.write(r"""
\documentclass[american]{article}
%------------------------
\usepackage[utf8]{inputenc}
\usepackage[american]{babel}
\usepackage{csquotes}
\usepackage[natbib=true,backend=biber, sorting=nyt,style=apa]{biblatex}
\DeclareLanguageMapping{american}{american-apa}
\addbibresource{""" + output_file + r"""}
\usepackage{subscript}
\newcommand\mathplus{+}
\usepackage{color}

\begin{document}
\title{Testfile for """ + output_file + r"""}
\author{Holger Metzler\footnote{Theoretical Ecosystem Ecology, Department of Biogeochemical Processes, Max Planck Institute for Biogeochemistry, Hans-Kn\"oll-Str. 10, 07745 Jena, Germany}\\{\footnotesize \texttt{hmetzler@bgc-jena.mpg.de}}}
\date{\today}
\maketitle
""")

    for entry in bibtex_entry_list:
        if entry.key not in original_entries_keys:
            f.write("{\color{red}\cite{" + entry.key + "}}\n")
            print("New entry: " + entry.key)
        else:
            f.write("\cite{" + entry.key + "}\n")

    f.write(r"""
\printbibliography
\end{document}
""")


