# vim:set ff=unix expandtab ts=4 sw=4:

# from pathlib import Path
import re
# from sympy import flatten
import yaml
# import copy
# import builtins
#from mendeley import Mendeley
#from mendeley.exception import MendeleyException
# from Latex import Latex
# from helpers import pp
from string import Template
import unicodedata
import bibtexparser
from bibtexparser.bparser import BibTexParser 
from bibtexparser.customization import homogeneize_latex_encoding 
from bibtexparser.customization import convert_to_unicode
import requests

class DoiNotFoundException(Exception):
    def __init__(self, doi):
        self.doi = doi

    def __str__(self):
        return("the doi " + self.doi + " could not be resolved")
    

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize("NFD",s) if unicodedata.category(c)!="Mn")
    # return unicodedata.normalize("NFD",s) # why not just this way?


def clean_key(key):
    key = key.replace(' ', '_')
    key = key.replace('.', '')
    key = key.replace(':', '')
    return strip_accents(key)


def bibtex_entry_from_str(entry_str):
    # converts a BibTeX entry from string to dictionary

    parser = BibTexParser()
    bib_database = bibtexparser.loads(entry_str, parser=parser)
    return(bib_database.entries[0])


def bibtex_entry_str(entry):
    # converts a BibTeX entry from string to dictionary

    bib_database = bibtexparser.bibdatabase.BibDatabase()
    bib_database.entries.append(entry)

    bibtex_string = bibtexparser.dumps(bib_database)
    return bibtex_string


#def mendeley_data_by_doi(doi):
#    # returns Mendeley data or 'None'
#
#    with open('mendeley_user_config.yml') as f:
#        config = yaml.load(f,Loader=yaml.FullLoader)
#    mendeley = Mendeley(config['clientId'], config['clientSecret'])
#    session = mendeley.start_client_credentials_flow().authenticate()
#
#    try:
#        doc = session.catalog.by_identifier(doi=doi, view='bib')
#    except MendeleyException:
#        return None
#
#    mendeley_doi = doc.identifiers['doi']
#    if doi == mendeley_doi:
#        return doc
#
#    # either an error or doi could not be resolved
#    return None
#
#
#def mendeley_bibtex_entry_str_by_doi(doi):
#    # returns a BibTeX entry as a string or 'None'
#
#    doc = mendeley_data_by_doi(doi)
#    if doc:
#        # doi could be resolved by Mendeley
#        # now create a BibTex entry as a string
#
#        full_names=[a.last_name +", " +a.first_name for a in doc.authors]
#        author_string=" and ".join(full_names)
#        key_str=clean_key(doc.authors[0].last_name+str(doc.year)+(doc.source))
#
#        t=Template("""\
#@article{$key,
# author = {$authors},
# doi = {$doi},
# journal = {$source},
# link = {http://dx.doi.org/$doi},
# number = {$issue},
# pages = {$pages},
# title = {$title},
# volume = {$volume},
# year = {$year}
#}""")
#        entry_str=t.substitute(
#                   key=key_str,
#                   authors=author_string,
#                   doi=doi,
#                   source=doc.source,
#                   issue=doc.issue,
#                   pages=doc.pages,
#                   title=doc.title,
#                   volume=doc.volume,
#                   year=doc.year                   
#               )
#
#        return entry_str
#
#
#def mendeley_bibtex_entry_by_doi(doi):
#    # returns a BibTeX entry as dictionary or 'None'
#
#    entry_str = mendeley_bibtex_entry_str_by_doi(doi)
#
#    if entry_str:
#        return bibtex_entry_from_str(entry_str)
#    else:
#        return None


def direct_data_by_doi(doi):
    # returns the data coming directly from doi or 'None'

    url = "http://dx.doi.org/" + doi
    headers = {"accept": "application/x-bibtex"}
    doi_result = requests.get(url, headers = headers).text

    pattern = re.compile(r"<!DOCTYPE.*")
    if None == pattern.match(doi_result):
        # doi was found
        return doi_result
    else:
        # doi was not found
        return None


def direct_bibtex_entry_by_doi(doi):
    # returns a BibTex entry as dictionary or 'None'

    entry_str = direct_data_by_doi(doi) 
    if entry_str: # doi found, entry_str is a string containing the BibTeX entry
        # need to reorganize authors from G. Mesz{\'e}na and ... to Mesz{\'e}na, G. and ...
        # then build the correct key

        # covert the BibTeX entry from string to dictionary
        entry = bibtex_entry_from_str(entry_str)

        # convert authors from "G. Meszéna" to "Meszéna, G."
        authors_old = entry['author']
        author_lst_old = authors_old.split(' and ') # split the authors string into a list of single authors          
        author_lst = [] # will contain the converted authors
        for author in author_lst_old:
            # either "G. Meszéna": last_name = "Meszéna" or "E. W. Wilson Jr.": last_name = "Wilson Jr."
            regexp = re.compile(r"(?P<last_name>((\w|-)+$)|((\w|-)+ (\w|-)+\.$))")
            reg_result = regexp.search(author)
            last_name = reg_result.group("last_name")
            first_name = regexp.sub("", author).strip() # the rest is the first name, cut leading and trailing whitespaces
            author_lst.append(last_name + ", " + first_name)

        entry['author'] = (" and ").join(author_lst)

        # generate citation key (same as in Mendeley case)
        auth = entry['author']
        auth = auth.split(',', 1)[0] # last name of first author
        yr = entry['year']
        
        # insert either journal, journaltitle or booktitle into key
        if 'journal' in entry.keys():
            jour = entry['journal']
        elif 'journaltitle' in entry.keys():
            jour = entry['journaltitle']
        elif 'booktitle' in entry.keys():
            jour = entry['booktitle']
        else:
            jour = ""

        key_str = auth + yr + jour
        key_str = strip_accents(key_str.replace(" ", "_")) # no accents or spaces in key

        entry['ID'] = key_str
        return(entry)
    else:
        return None


def direct_bibtex_entry_str_by_doi(doi):
    # returns a BibTeX entry as a dictionary or 'None'

    entry = direct_bibtex_entry_by_doi(doi)
    if entry:
        return bibtex_entry_str(entry)
    else:
        return None


def storable_bibtex_entry_by_doi(doi):
    # returns a dictionary with the BibTex entry or 'None'

    ## 1st: check on Mendeley, because they provide abstracts
    #entry = mendeley_bibtex_entry_by_doi(doi)
    #if entry: 
    #    return entry

    # 2nd: check doi.org directly
    entry = direct_bibtex_entry_by_doi(doi)
    if entry: 
        return entry

    # doi could not be resolved
    raise DoiNotFoundException(doi)


def printable_bibtex_entry(entry):
    # converts a dictionary BibTeX entry to LaTeX format

    entry_str = bibtex_entry_str(entry)
    parser = BibTexParser()
    parser.customization = homogeneize_latex_encoding
    bib_database = bibtexparser.loads(entry_str, parser = parser)
    return(bib_database.entries[0])


def printable_bibtex_entry_by_doi(doi):
    # returns a BibTex entry in LaTeX format as dictionary or 'None'

    entry = storable_bibtex_entry_by_doi(doi)
    if entry:
        return(printable_bibtex_entry(entry))
    else:
        return None


def biblatex_entry_by_doi(doi):
    # returns a BibLateX entry as dictionary or 'None'

    entry = printable_bibtex_entry_by_doi(doi)
    if entry:
        entry_str =  bibtex_entry_str(entry)
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        
        bib_database = bibtexparser.loads(entry_str, parser=parser)
    
        # convert 'journal' to 'journaltitle'
        for e in bib_database.entries:
            if 'journal' in e.keys():
                e['journaltitle'] = e['journal']
                del e['journal']

        bibtex_string = bibtexparser.dumps(bib_database)
        return bibtex_entry_from_str(bibtex_string)
    else:
        return None
    return(bibtex_string)
