# vim:set ff=unix expandtab ts=4 sw=4:

# possible third way to download BibTeX entry by doi can be implemented
# README first
# the api is described here http://help.crossref.org/using_http
# I had to register my email adress to be get some answers.
# other problems are described here: http://blog.martinfenner.org/2013/10/13/broken-dois/
# curl "https://doi.crossref.org/search/doi?pid=mamueller@bgc-jena.mpg.de&format=unixsd&doi=10.1577/H02-043"
"""
Module bibtexc.py for usage of BibTeX entries

Classes:
    - BibtexEntry: dictionary with BibTex entry and functions for converting to different styles

Methods:
    - entry_list_from_file: reads in a file to a list of BibtexEntry objects
    - entry_list_to_file: writes a list of BibtexEntry objects to a file

Exceptions: 
    - DoiNotFoundException: raised if online retrieval of BibTeX entry by doi fails
"""


import re
import yaml
from mendeley import Mendeley
from mendeley.exception import MendeleyException
from string import Template
import string
import unicodedata
import bibtexparser
from bibtexparser.bparser import BibTexParser 
from bibtexparser.customization import homogenize_latex_encoding 
from bibtexparser.customization import convert_to_unicode
import requests
from pathlib import Path
#imports from own package
from . import gv

def online_entry(doi,abstract=True):
    try: 
        # 1st: check on Mendeley, because they provide abstracts
        entry= _entry_from_str(_mendeley_str(doi, abstract))
        return entry
            
    except Exception as e: #fixme mm , maybe find out what exceptions mendeley has und only catch those
        # 2nd: check doi.org directly, no abstracts provided here                  
        try: 
            entry = _direct(doi)
            return entry

        except Exception: #fixme mm , maybe find out what exceptions occure and only catch those
            print("Warning:Could not reach doi.org")
            
            #reraise an exception
            raise DoiNotFoundException(doi) 

class DoiNotFoundException(Exception):
    """Raised if BibTex entry cannot be found online by doi"""
    def __init__(self, doi):
        self.doi = doi

    def __str__(self):
        return("The doi " + self.doi + " could not be resolved.")

############################################################
class BibtexEntry():
    """Stores a BibTeX entry as a dictionary in plain style and provides methods to convert the entry to BibTeX and BibLaTeX.

    Methods:
        - set_key: set the key of a BibTexEntry (stored in entry['ID'])
        - bibtex: return entry as dictionary in BibTeX style
        - biblatex: return entry as dictionary in BibLaTeX stlye
        - as_str: return entry as string in desired format
        - get_abstract: return entry['abstract'] as string in desired format

    Properties:
        - key: the key of a BibtexEntry (stored in entry['ID'])
    """

    @classmethod
    def from_entry_str(cls,entry_str):
        # call normal init
        BE=cls(_entry_from_str(entry_str))
        return(BE)

    @classmethod
    def from_doi(cls,doi,abstract=True):
        try:
            entry=online_entry(doi)
            print("2 ###########################")
            print(entry)
            print("2 ###########################")
            # call normal init
            BE=cls(entry)
            BE.__automatic_key()
            return(BE)
        except DoiNotFoundException:
            return cls(dict())
    def __init__(self, entry ):
        self.entry = entry
        #if entry:
        #    if 'ID' not in self.entry.keys() or self.entry['ID'] == "default":
        #        self.__automatic_key()

       # # 'ID' saves the key (convention by biblatexparser)
        #if 'ID' not in self.entry.keys() or self.entry['ID'] == "default":
        #    self.__automatic_key() # if no key given create automatic key

    #def __init__(self, doi = "", entry = {}, entry_str = "", abstract = False, nochanges = False):
       
       # """Create a BibtexEntry either by doi or by a given dictionary.

       # If doi is given attempt to find the appropriate entry online (first on Mendeley, second on doi.org), in case of failure \
       # raise DoiNotFoundException.
       # If entry is given just copy the entry into the new BibtexEntry.
       # In both cases the key is created automatically as LastnamefirstauthorYearJournalname.

       # If neither doi nor entry are given create an empty entry dictionary.

       # If abstract = True then also the abstract will be incorporated (if possible).
       # """
       # # check if an entry was given as dict        
       # if entry:
       #     cls.from_entry(entry)
       #     self.entry = _entry_from_str(_entry_to_str(entry)) # dictionary that contains the plain BibTeX data
       #         # slightly formatted by first converting it to a string by the bibtexparser
       # # or as str
       # elif entry_str:
       #     self.entry = _entry_from_str(entry_str)

       # else:
       #     #self.entry = {}
       #     if doi:
       #         try: 
       #             # 1st: check on Mendeley, because they provide abstracts
       #             entry = _mendeley(doi, abstract)
       #             if entry: 
       #                 self.entry = entry
       #                 self.__automatic_key()
       #                 return
       #         except Exception: #fixme mm , maybe find out what exceptions mendeley has und only catch those
       #             print("Warning:Could not reach mendeley")
       #             # 2nd: check doi.org directly, no abstracts provided here                  
       #             try: 
       #                 entry = _direct(doi)
       #                 if entry: 
       #                     self.entry = entry
       #                     self.__automatic_key()
       #                     return
       #             except Exception: #fixme mm , maybe find out what exceptions mendeley has und only catch those
       #             print("Warning:Could not reach doi.org")
       #     else:
       #         print("BibtexEntry was called without a bibtex_str, bibtex dict or doi")




    def __eq__(self, other):
        """Override == operator: equality holds iff keys are equal"""
        if isinstance(other, self.__class__):
            return self.key == other.key
        return NotImplemented


    def __ne__(self, other):
        """Override != operator: equality holds iff keys are equal"""
        if isinstance(other, self.__class__):
            return not self == other


    def __hash__(self):
        """Override hash property for consistent use of new == operator and set functionality"""
        # fixme mm 05/19/2018
        # The python standard library reference says https://docs.python.org/3/reference/datamodel.html#object.__hash__
        # that one should not implement a __hash__ function for mutable objects
        # The existence of the set_key method suggests that BibtexEntry objects are mutable
        # so we run the risk of finding the wrong object
        # If we want set functionalyty we need hashability so we should probably sacrifice mutability 
        return hash(self.key)


    def __str__(self):
        return self.entry.__str__()


    @property
    def key(self):
        """Return the key of the entry (stored in entry['ID'])."""
        if 'ID' in self.entry.keys():
            return self.entry['ID']
        else:
            return ""


    def set_key(self, key_str):
        """Set the key of the entry (stored in entry['ID']).

        Removes automatically bad characters from key_str and converts unicode characters.
    
        Arguments:
            - key_str: string that will be converted to the entry's key
        """
        key_str = key_str.replace(' ', '')
        key_str = key_str.replace('.', '')
        key_str = key_str.replace(':', '')
        self.entry['ID'] = _strip_accents(key_str)


    def __automatic_key(self):
        """Generate the key (stored in entry['ID']) as LastnamefirstauthorYearJournalname."""
        # we need the author as unicode: é instead of {\'e}
        if self.entry:
            entry = self.biblatex
            auth = entry['author']
            auth = auth.split(',', 1)[0] # last name of first author
            if 'year' in entry.keys():
                yr = entry['year']
            else:
                yr = ""
            
            # insert either journal, journaltitle or booktitle into key
            if 'journal' in entry.keys():
                jour = entry['journal']
            elif 'journaltitle' in entry.keys():
                jour = entry['journaltitle']
            elif 'booktitle' in entry.keys():
                jour = entry['booktitle']
            else:
                jour = ""
    
            key_str = (auth + yr + jour).replace(" ", "")
            self.set_key(key_str)


    @property
    def bibtex(self):
        """Return entry formatted in BibTeX style as dictionary or 'None'."""
        if self.entry:
            entry_str = _entry_to_str(self.entry)
            parser = BibTexParser()
            parser.customization = homogenize_latex_encoding
            bib_database = bibtexparser.loads(entry_str, parser = parser)
            return bib_database.entries[0]
        else:
            return None


    @property
    def biblatex(self):
        """Return entry formatted in BibLateX style as dictionary or 'None'."""
        entry_str = self.as_str("BibTeX")
        if entry_str:
            parser = BibTexParser()
            parser.customization = convert_to_unicode
            
            bib_database = bibtexparser.loads(entry_str, parser=parser)
        
            # convert 'journal' to 'journaltitle'
            for e in bib_database.entries:
                if 'journal' in e.keys():
                    e['journaltitle'] = e['journal']
                    del e['journal']

#                special_terms = {" &": ' \&'}
#                for key in special_terms.keys():
#                    regexp = re.compile(key)
#                    e['title'] = regexp.sub(special_terms[key], e['title'])
#                    print(e['title'])

            bibtex_string = bibtexparser.dumps(bib_database)
            return _entry_from_str(bibtex_string)
        else:
            return None


    def as_str(self, format_str = "plain"):
        """Return entry as string in desired format.

        Arguments:
            -format_str: 
                - plain (default): plain entry
                - BibTeX: BibTeX format
                - BibLaTeX: BibLaTeX format
        """
        if format_str == "plain":
            return _entry_to_str(self.entry)

        if format_str == "BibTeX":
            return _entry_to_str(self.bibtex)

        if format_str == "BibLaTeX":
            return _entry_to_str(self.biblatex)


    def get_abstract(self, format_str = "plain"):
        """Return entry['abstract'] as string in desired format or empty string.

        Arguments:
            -format_str: 
                - plain (default): plain entry
                - BibTeX: BibTeX format
                - BibLaTeX: BibLaTeX format
        """
        if 'abstract' in self.entry.keys():
            if format_str == "plain":
                return self.entry['abstract']
    
            if format_str == "BibTeX":
                return self.bibtex['abstract']
    
            if format_str == "BibLaTeX":
                return self.biblatex['abstract']
        
        # no abstract available
        return ""


def _strip_accents(s):
    """Convert unicode special characters like 'é' to ASCII (?), like 'e'."""

    return ''.join(c for c in unicodedata.normalize("NFD",s) if unicodedata.category(c)!="Mn")


def _entry_to_str(entry):
    """Convert a BibTeX entry from a dictionary to a string and return it."""
    bib_database = bibtexparser.bibdatabase.BibDatabase()
    bib_database.entries.append(entry)

    bibtex_string = bibtexparser.dumps(bib_database)
    return bibtex_string


def _entry_from_str(entry_str):
    """Convert a BibTeX entry from string to dictionary and return it."""
    parser = BibTexParser()
    bib_database = bibtexparser.loads(entry_str, parser=parser)
    return bib_database.entries[0]

#fixme mm 
# the method seems to be untested 
def _direct_data(doi):
    """Return the data coming directly from doi (as string) or 'None'."""
    url = "http://dx.doi.org/" + doi
    headers = {"accept": "application/x-bibtex"}
    doi_result = requests.get(url, headers = headers).text

    pattern = re.compile(r"<!DOCTYPE.*")
    if None == pattern.match(doi_result):
        # doi was found
        return doi_result
    else:
        # doi was not found
        raise DoiNotFoundException(doi)


#fixme mm 
# the method seems to be untested 
def _direct(doi):
    """Return a BibTex entry as dictionary or 'None', retrieved by doi directly on doi.org."""
    entry_str = _direct_data(doi)
    # if the doi found, entry_str is a string containing the BibTeX entry
    # need to reorganize authors from G. Mesz{\'e}na and ... to Mesz{\'e}na, G. and ...

    # convert the BibTeX entry from string to dictionary
    entry = _entry_from_str(entry_str)

    # convert authors from "G. Meszéna" to "Meszéna, G."
    authors_old = entry['author']
    author_lst_old = authors_old.split(' and ') # split the authors string into a list of single authors          
    author_lst = [] # will contain the converted authors
    for author in author_lst_old:
        # either "G. Meszéna": last_name = "Meszéna" or "E. W. Wilson Jr.": last_name = "Wilson Jr."#
        # or even Van Der Werf
        regexp = re.compile(r"(?P<last_name>((\w|-)+$)|((\w|-)+ (\w|-)+\.$)|(Van.*))")
        reg_result = regexp.search(author)
        last_name = reg_result.group("last_name")
        first_name = regexp.sub("", author).strip() # the rest is the first name, cut leading and trailing whitespaces
        author_lst.append(last_name + ", " + first_name)

    entry['author'] = (" and ").join(author_lst)

    return entry


def _mendeley_data(doi):
    """Returns Mendeley data or 'None', retrieved by doi via Mendeley."""

    config_file_name = gv.resources_path.joinpath('mendeley_user_config.yml').as_posix()

    with open(config_file_name) as f:
        config = yaml.load(f)

    mendeley = Mendeley(config['clientId'], config['clientSecret'])
    session = mendeley.start_client_credentials_flow().authenticate()

    doc = session.catalog.by_identifier(doi=doi, view='bib')

    mendeley_doi = doc.identifiers['doi']
    if doi == mendeley_doi:
        return doc
    else:
        raise DoiNotFoundException()



def _mendeley_str(doi, abstract=False):
    """Return a BibTeX entry as a string or 'None', reetrieved by doi via Mendeley."""
    doc = _mendeley_data(doi)
    # doi could be resolved by Mendeley
    # now create a BibTex entry as a string

    full_names=[a.last_name +", " +a.first_name for a in doc.authors]
    author_string=" and ".join(full_names)
    if abstract:
        t=Template("""\
                      @article{$key,
                               author = {$authors},
                               doi = {$doi},
                               journal = {$source},
                               link = {http://dx.doi.org/$doi},
                               number = {$issue},
                               pages = {$pages},
                               title = {$title},
                               volume = {$volume},
                               year = {$year},
                               abstract = {$abstract}
                      }""")
        entry_str=t.substitute(
               key = "default",
               authors = author_string,
               doi = doi,
               source = doc.source,
               issue = doc.issue,
               pages = doc.pages,
               title = doc.title,
               volume = doc.volume,
               year = doc.year,
               abstract = doc.abstract
           )
    else:
        t=Template("""\
                      @article{$key,
                               author = {$authors},
                               doi = {$doi},
                               journal = {$source},
                               link = {http://dx.doi.org/$doi},
                               number = {$issue},
                               pages = {$pages},
                               title = {$title},
                               volume = {$volume},
                               year = {$year}
                      }""")
    
        entry_str=t.substitute(
               key = "default",
               authors = author_string,
               doi = doi,
               source = doc.source,
               issue = doc.issue,
               pages = doc.pages,
               title = doc.title,
               volume = doc.volume,
               year = doc.year
           )

    return entry_str

#def _mendeley(doi, abstract=False):
#    """Returns a BibTeX entry as dictionary or 'None', retrieved by doi via Mendeley."""
#    entry_str = _mendeley_str(doi, abstract)
#
#    if entry_str:
#        return _entry_from_str(entry_str)
#    else:
#        return None


### public methods ###


def entry_list_from_file(input_file, nochanges = False):
    # fixme mm:
    # nochanges does not seem to be used anywhere any longer.
    # remove it.
    """Return a list of elements of type BibtexEntry read in from input_file."""
    with open(input_file, 'r') as bibtex_file:
#        parser = BibTexParser()
        bib_database = bibtexparser.load(bibtex_file)

    entry_list = []
    for entry in bib_database.entries:
        element = BibtexEntry(entry=entry )
        entry_list.append(element)

    return entry_list


def entry_list_to_file(output_file, bibtex_entry_list, format_str = "plain"):
    """Write list of BibtexEntry to output_file in desired format.

    Attributes:
        - output_file: output file
        - bibtex_entry_list: list of elements of type BibtexEntry
        - format_str: 
            - plain (default): plain entry
            - BibTeX: BibTeX style
            - BibLaTeX: BibLaTeX style
    """


    output_str= ""
    for bibtex_entry in bibtex_entry_list:
        # delete useless tags and abstract
        for key in ('file', 'bdsk-url-1', 'bdsk-url-2', 'pmid', 'n2', 'm3', 'da', 'ty', 'pubmedid', 'bdsk-file-1', \
                    'journal1', 'year1', 'l3', 'comment_out_note', 'idsk-file-1', 'abstract', \
                    'issn', 'keyword', 'date-added', 'date-modified', 'm1', 'cr', 'annote', \
                    'ty', 'catalogue-url', 'eprint', 'contents', 'language', 'note', \
                    'subjects', 'type', 'copyright', 'document_type'):
            if key in bibtex_entry.entry.keys():
                del bibtex_entry.entry[key]

        # remove 'None' entries (happens often for 'number')
        remove_tags = []
        for tag in bibtex_entry.entry.keys():
            if bibtex_entry.entry[tag] in ('None', 'none'):
                remove_tags.append(tag)
        
        for tag in remove_tags:
            del bibtex_entry.entry[tag]

#        special_terms = {"CO\(2\)": 'CO$_2$', "CO2": 'CO$_2$', "yr-1": 'yr$^{-1}$', "MJ-1": 'MJ$^{-1}$', "year−1": 'year$^{-1}$', "ha−1": 'ha$^{-1}$', "\(lai\)": '(LAI)', "\slai\s": ' LAI '}

        # correct CO2 writing
        special_terms = {" CO\$_2\$": ' {CO$_2$}'}
        for key in special_terms.keys():
#            print(key)
            regexp = re.compile(key)
#            print(bibtex_entry.entry['title'])
            bibtex_entry.entry['title'] = regexp.sub(special_terms[key], bibtex_entry.entry['title'])
#            print(bibtex_entry.entry['title'])

        output_str = output_str + bibtex_entry.as_str(format_str)

    with open(output_file, 'wb') as bibtex_file:
        bibtex_file.write(output_str.encode("utf8"))
