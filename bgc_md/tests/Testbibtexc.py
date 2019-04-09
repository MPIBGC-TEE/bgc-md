#!/usr/bin/env python3
#vim:set ff=unix expandtab ts=4 sw=4:

import sys
import unittest
from bgc_md.helpers import remove_indentation
import bgc_md.bibtexc as bibtexc
from bgc_md.bibtexc import DoiNotFoundException, BibtexEntry, online_entry
from testinfrastructure.InDirTest import InDirTest


# only publicly accesible methods are tested, no private ones, they are tested implicitly
class Testbibtexc(unittest.TestCase):

    def setUp(self):
        dict_dict = {"10.1556/Select.2.2001.1-2.14": 
                        {'ID': 'Meszena2002Selection', 
                        'number': '1-2', 
                        'journal': 'Selection', 
                        'ENTRYTYPE': 'article', 
                        'year': '2002', 
                        'doi': '10.1556/Select.2.2001.1-2.14', 
                        'title': 'Evolutionary Optimisation Models and Matrix Games in the Unified Perspective of Adaptive Dynamics', 
                        'link': 'http://dx.doi.org/10.1556/Select.2.2001.1-2.14', 
                        'volume': '2', 
                        'author': 'Meszéna, G. and Kisdi, É. and Dieckmann, U. and Geritz, S. a. H. and Metz, J. a. J.', 
                        'pages': '193-220'},
                    "10.1139/x91-151":
                        {'ID': 'Korol1991CanadianJournalofForestResearch',
                         'number': '7',
                         'journal': 'Canadian Journal of Forest Research',
                         'ENTRYTYPE': 'article',
                         'year': '1991',
                         'doi': '10.1139/x91-151',
                         'title': 'Testing a mechanistic carbon balance model against observed tree growth',
                         'link': 'http://dx.doi.org/10.1139/x91-151',
                         'volume': '21', 'author': 'Korol, R. L. and Running, S. W. and Milner, K. S. and Hunt Jr., E. R.',
                         'pages': '1098-1105'},
                    "10.1029/93GB02725": 
                        {'ID': 'Potter1993GlobalBiogeochemicalCycles',
                         'number': '4',
                         'journal': 'Global Biogeochemical Cycles',
                         'ENTRYTYPE': 'article',
                         'year': '1993',
                         'doi': '10.1029/93GB02725',
                         'title': 'Terrestrial ecosystem production: A process model based on global satellite and surface data',
                         'link': 'http://dx.doi.org/10.1029/93GB02725',
                         'volume': '7',
                         'author': 'Potter, Christopher S. and Randerson, James T. and Field, Christopher B. and Matson, Pamela A. and Vitousek, Peter M. and Mooney, Harold A. and Klooster, Steven A.',
                         'pages': '811-841'},
                    "10.1139/x91-133": 
                        {'ID': 'Meredith1991CanadianJournalofForestResearch',
                         'number': '7',
                         'journal': 'Canadian Journal of Forest Research',
                         'ENTRYTYPE': 'article',
                         'year': '1991',
                         'doi': '10.1139/x91-133',
                         'title': 'Repeated measures experiments in forestry: focus on analysis of response curves',
                         'link': 'http://dx.doi.org/10.1139/x91-133',
                         'volume': '21',
                         'author': 'Meredith, M P and Stehman, S V',
                         'pages': '957-965'}
                    }

        self.entry_dict = {}
        for key, dic in dict_dict.items():
            self.entry_dict[key] = BibtexEntry(entry = dic)
        
#    @unittest.skip
    def test_init(self):

        ## check that Mendeley returns a dictionary with the correct doi
        result = bibtexc.BibtexEntry.from_doi(doi="10.1556/Select.2.2001.1-2.14")
        self.assertEqual(result.entry['doi'].lower(), "10.1556/Select.2.2001.1-2.14".lower())

        ## check that  doi.org returns a dictionary with the correct doi
        result = bibtexc.BibtexEntry.from_doi(doi="10.1139/x91-151")
        self.assertEqual(result.entry['doi'].lower(), "10.1139/x91-151".lower())

    @unittest.skip    
    def test_init_with_abstract(self):
        # fixme: mendeley seems not to be able to find the abstract we have to check this more thouroughly
        # check case 'abstract=True'
        result = bibtexc.BibtexEntry.from_doi(doi="10.1029/93GB02725", abstract=True)
        print("#################################")
        print(result.entry)
        print("#################################")
        self.assertTrue(len(result.entry['abstract']) >0)

    def test_online_entry(self):
        # check on invalid doi, hence DoiNotFoundException
        doi = "kcvbjs__e"
        with self.assertRaises(DoiNotFoundException) as cm:
            entry = online_entry(doi=doi)
        e = cm.exception
        #self.assertEqual(e.__str__(),"The doi " + doi + " could not be resolved.")
        self.assertEqual(e.doi, doi)

    def test_eq_ne_hash(self):
        entry1 = self.entry_dict["10.1139/x91-133"]
        entry2 = self.entry_dict["10.1029/93GB02725"]
        entry3 = self.entry_dict["10.1139/x91-133"]
        self.assertTrue(entry1==entry3)
        self.assertFalse(entry1==entry2)


    def test_set_operations(self):
        entry1 = self.entry_dict["10.1139/x91-133"]
        entry2 = self.entry_dict["10.1029/93GB02725"]
        entry3 = self.entry_dict["10.1139/x91-133"]

        s = set([entry1, entry2, entry3])
        self.assertEqual(len(s),2)


    def test_get_key(self):
        bibtex_entry = self.entry_dict["10.1029/93GB02725"]
        target_string = "Potter1993GlobalBiogeochemicalCycles"
        self.assertEqual(bibtex_entry.key, target_string)
    

    def test_set_key(self):    
        # test also __strip_accents automatically
        bibtex_entry = self.entry_dict["10.1029/93GB02725"]
        key_str = "Pötter :1.993GBC"
        bibtex_entry.set_key(key_str)
        self.assertEqual(bibtex_entry.entry['ID'], "Potter1993GBC")
        
    @unittest.skip 
    # fixme (check the string , It obviousliy changed after the last bibtexparser update)
    def test_biblatex(self):
        bibtex_entry = self.entry_dict["10.1556/Select.2.2001.1-2.14"]
        target_dict = {'ENTRYTYPE': 'article',\
                       'ID': 'Meszena2002Selection',\
                       'author': 'Meszéna, G. and Kisdi, É. and Dieckmann, U. and Geritz, S. a. H. and Metz, J. a. J.',\
                       'doi': '10.1556/Select.2.2001.1-2.14',\
                       'journaltitle': 'Selection',\
                       'link': 'http://dx.doi.org/10.1556/Select.2.2001.1-2.14',\
                       'number': '1-2',\
                       'pages': '193-220',\
                       'title': '{E}volutionary {O}ptimisation {M}odels and {M}atrix {G}ames in the {U}nified {P}erspective of {A}daptive {D}ynamics',\
                       'volume': '2',\
                       'year': '2002'}
        self.assertEqual(bibtex_entry.biblatex, target_dict)

 
    @unittest.skip 
    # fixme (check the string , It obviousliy changed after the last bibtexparser update)
    def test_as_str(self):
        doi = "10.1556/Select.2.2001.1-2.14"
        bibtex_entry = self.entry_dict[doi]
        # check plain style
        result = bibtex_entry.as_str("plain")
        target_string = """\
                           @article{Meszena2002Selection,
                                author = {Meszéna, G. and Kisdi, É. and Dieckmann, U. and Geritz, S. a. H. and Metz, J. a. J.},
                                doi = {10.1556/Select.2.2001.1-2.14},
                                journal = {Selection},
                                link = {http://dx.doi.org/10.1556/Select.2.2001.1-2.14},
                                number = {1-2},
                                pages = {193-220},
                                title = {Evolutionary Optimisation Models and Matrix Games in the Unified Perspective of Adaptive Dynamics},
                                volume = {2},
                                year = {2002}
                            }
                        """ 
        self.assertEqual(remove_indentation(result), remove_indentation(target_string))

        # check BibTeX style
        result = bibtex_entry.as_str("BibTeX")
        target_string = r"""@article{Meszena2002Selection,
                                author = {Mesz{\'e}na, G. and Kisdi, {\'E}. and Dieckmann, U. and Geritz, S. a. H. and Metz, J. a. J.},
                                doi = {10.1556/Select.2.2001.1-2.14},
                                journal = {Selection},
                                link = {http://dx.doi.org/10.1556/Select.2.2001.1-2.14},
                                number = {1-2},
                                pages = {193-220},
                                title = {{E}volutionary {O}ptimisation {M}odels and {M}atrix {G}ames in the {U}nified {P}erspective of {A}daptive {D}ynamics},
                                volume = {2},
                                year = {2002}
                            }
                        """
        self.assertEqual(remove_indentation(result), remove_indentation(target_string))
        
        # check BibLaTeX style
        result = bibtex_entry.as_str("BibLaTeX")
        target_string = """\
                           @article{Meszena2002Selection,
                               author = {Meszéna, G. and Kisdi, É. and Dieckmann, U. and Geritz, S. a. H. and Metz, J. a. J.},
                               doi = {10.1556/Select.2.2001.1-2.14},
                               journaltitle = {Selection},
                               link = {http://dx.doi.org/10.1556/Select.2.2001.1-2.14},
                               number = {1-2},
                               pages = {193-220},
                               title = {{E}volutionary {O}ptimisation {M}odels and {M}atrix {G}ames in the {U}nified {P}erspective of {A}daptive {D}ynamics},
                               volume = {2},
                               year = {2002}
                           }
                        """
        self.assertEqual(remove_indentation(result), remove_indentation(target_string))

    @unittest.skip("They always change the target")
    def test_get_abstract(self):
        bibtex_entry = bibtexc.BibtexEntry.from_doi(doi="10.1029/93GB02725", abstract=True)
        
        # check plain style
        result = bibtex_entry.get_abstract("plain")
        target_string = "This paper presents a modeling approach aimed at seasonal resolution of global climatic and edaphic controls on patterns of terrestrial ecosystem production and soil microbial respiration. We use satellite imagery (Advanced Very High Resolution Radiometer and International Satellite Cloud Climatology Project solar radiation), along with historical climate (monthly temperature and precipitation) and soil attributes (texture, C and N contents) from global (1°) data sets as model inputs. The Carnegie-Ames-Stanford approach (CASA) Biosphere model runs on a monthly time interval to simulate seasonal patterns in net plant carbon fixation, biomass and nutrient allocation, litterfall, soil nitrogen mineralization, and microbial CO2 production. The model estimate of global terrestrial net primary production is 48 Pg C yr−1 with a maximum light use efficiency of 0.39 g C MJ−1PAR. Over 70% of terrestrial net production takes place between 30°N and 30°S latitude. Steady state pools of standing litter represent global storage of around 174 Pg C (94 and 80 Pg C in nonwoody and woody pools, respectively), whereas the pool of soil C in the top 0.3 m that is turning over on decadal time scales comprises 300 Pg C. Seasonal variations in atmospheric CO2 concentrations from three stations in the Geophysical Monitoring for Climate Change Flask Sampling Network correlate significantly with estimated net ecosystem production values averaged over 50°–80° N, 10°–30° N, and 0°–10° N."
        self.assertEqual(result, target_string)

        # check BibTeX style
        result = bibtex_entry.get_abstract("BibTeX")    
        target_string = "This paper presents a modeling approach aimed at seasonal resolution of global climatic and edaphic controls on patterns of terrestrial ecosystem production and soil microbial respiration. We use satellite imagery (Advanced Very High Resolution Radiometer and International Satellite Cloud Climatology Project solar radiation), along with historical climate (monthly temperature and precipitation) and soil attributes (texture, C and N contents) from global (1\textdegree ) data sets as model inputs. The Carnegie-Ames-Stanford approach (CASA) Biosphere model runs on a monthly time interval to simulate seasonal patterns in net plant carbon fixation, biomass and nutrient allocation, litterfall, soil nitrogen mineralization, and microbial CO2 production. The model estimate of global terrestrial net primary production is 48 Pg C yr−1 with a maximum light use efficiency of 0.39 g C MJ−1PAR. Over 70\% of terrestrial net production takes place between 30\textdegree N and 30\textdegree S latitude. Steady state pools of standing litter represent global storage of around 174 Pg C (94 and 80 Pg C in nonwoody and woody pools, respectively), whereas the pool of soil C in the top 0.3 m that is turning over on decadal time scales comprises 300 Pg C. Seasonal variations in atmospheric CO2 concentrations from three stations in the Geophysical Monitoring for Climate Change Flask Sampling Network correlate significantly with estimated net ecosystem production values averaged over 50\textdegree \textendash 80\textdegree  N, 10\textdegree \textendash 30\textdegree  N, and 0\textdegree \textendash 10\textdegree  N."
        target_string = "This paper presents a modeling approach aimed at seasonal resolution of global climatic and edaphic controls on patterns of terrestrial ecosystem production and soil microbial respiration. We use satellite imagery (Advanced Very High Resolution Radiometer and International Satellite Cloud Climatology Project solar radiation), along with historical climate (monthly temperature and precipitation) and soil attributes (texture, C and N contents) from global (1\textdegree ) data sets as model inputs. The Carnegie-Ames-Stanford approach (CASA) Biosphere model runs on a monthly time interval to simulate seasonal patterns in net plant carbon fixation, biomass and nutrient allocation, litterfall, soil nitrogen mineralization, and microbial CO2 production. The model estimate of global terrestrial net primary production is 48 Pg C yr−1 with a maximum light use efficiency of 0.39 g C MJ−1PAR. Over 70\% of terrestrial net production takes place between 30\textdegree N and 30\textdegree S latitude. Steady state pools of standing litter represent global storage of around 174 Pg C (94 and 80 Pg C in nonwoody and woody pools, respectively), whereas the pool of soil C in the top 0.3 m that is turning over on decadal time scales comprises 300 Pg C. Seasonal variations in atmospheric CO2 concentrations from three stations in the Geophysical Monitoring for Climate Change Flask Sampling Network correlate significantly with estimated net ecosystem production values averaged over 50\textdegree \textendash 80\textdegree  N, 10\textdegree \textendash 30\textdegree  N, and 0\textdegree \textendash 10\textdegree  N."
        self.assertEqual(result.strip(), target_string.strip())

        # check BibLaTeX style
        result = bibtex_entry.get_abstract("BibLaTeX")    
        target_string = "This paper presents a modeling approach aimed at seasonal resolution of global climatic and edaphic controls on patterns of terrestrial ecosystem production and soil microbial respiration. We use satellite imagery (Advanced Very High Resolution Radiometer and International Satellite Cloud Climatology Project solar radiation), along with historical climate (monthly temperature and precipitation) and soil attributes (texture, C and N contents) from global (1-degrees) data sets as model inputs. The Carnegie-Ames-Stanford approach (CASA) Biosphere model runs on a monthly time interval to simulate seasonal patterns in net plant carbon fixation, biomass and nutrient allocation, litterfall, soil nitrogen mineralization, and microbial CO2 production. The model estimate of global terrestrial net primary production is 48 Pg C yr-1 with a maximum light use efficiency of 0.39 g C MJ-1 PAR. Over 70% of terrestrial net production takes place between 30-degrees-N and 30-degrees-S latitude. Steady state pools of standing litter represent global storage of around 174 Pg C (94 and 80 Pg C in nonwoody and woody pools, respectively), whereas the pool of soil C in the top 0.3 m that is turning over on decadal time scales comprises 300 Pg C. Seasonal variations in atmospheric CO2 concentrations from three stations in the Geophysical Monitoring for Climate Change Flask Sampling Network correlate significantly with estimated net ecosystem production values averaged over 50-degrees-80-degrees-N, 10-degrees-30-degrees-N, and 0-degrees-10-degrees-N."
        self.assertEqual(result.strip(), target_string.strip())

class TestbibtexcFiles(InDirTest):

    def test_entry_list_from_file(self):

        # create a temporary BibTeX file from which the list is to be read
        file_string = """\
                         @article{Meszena2002Selection,
                          author = {Meszéna, G. and Kisdi, É. and Dieckmann, U. and Geritz, S. A. H. and Metz, J. A. J.},
                          doi = {10.1556/Select.2.2001.1-2.14},
                          journal = {Selection},
                          link = {http://dx.doi.org/10.1556/Select.2.2001.1-2.14},
                          number = {1-2},
                          pages = {193-220},
                          title = {Evolutionary Optimisation Models and Matrix Games in the Unified Perspective of Adaptive Dynamics},
                          volume = {2},
                          year = {2002}
                         }
                         
                         @article{Korol1991CanadianJournalofForestResearch,
                          author = {Korol, R. L. and Running, S. W. and Milner, K. S. and Hunt Jr., E. R.},
                          doi = {10.1139/x91-151},
                          journal = {Canadian Journal of Forest Research},
                          link = {http://dx.doi.org/10.1139/x91-151},
                          month = {jul},
                          number = {7},
                          pages = {1098--1105},
                          publisher = {Canadian Science Publishing},
                          title = {Testing a mechanistic carbon balance model against observed tree growth},
                          volume = {21},
                          year = {1991}
                         }
                      """  
        input_file = "input.bib"
        with open(input_file, "w") as f:
            f.write(file_string)

        bibtex_entry_list = bibtexc.entry_list_from_file(input_file)

        # check first list entry
        target_dict = {'title': 'Evolutionary Optimisation Models and Matrix Games in the Unified Perspective of Adaptive Dynamics', 'journal': 'Selection', 'number': '1-2', 'pages': '193-220', 'author': 'Meszéna, G. and Kisdi, É. and Dieckmann, U. and Geritz, S. A. H. and Metz, J. A. J.', 'year': '2002', 'ID': 'Meszena2002Selection', 'doi': '10.1556/Select.2.2001.1-2.14', 'ENTRYTYPE': 'article', 'link': 'http://dx.doi.org/10.1556/Select.2.2001.1-2.14', 'volume': '2'}
        self.assertEqual(bibtex_entry_list[0].entry, target_dict)

        # check second list entry
        target_dict = {'volume': '21', 'title': 'Testing a mechanistic carbon balance model against observed tree growth', 'doi': '10.1139/x91-151', 'journal': 'Canadian Journal of Forest Research', 'year': '1991', 'publisher': 'Canadian Science Publishing', 'pages': '1098--1105', 'month': 'jul', 'ENTRYTYPE': 'article', 'number': '7', 'author': 'Korol, R. L. and Running, S. W. and Milner, K. S. and Hunt Jr., E. R.', 'link': 'http://dx.doi.org/10.1139/x91-151', 'ID': 'Korol1991CanadianJournalofForestResearch'}
        self.assertEqual(bibtex_entry_list[1].entry, target_dict)

    @unittest.skip("This test is flapping due to changes in the mendeley database")
    #fixme:
    # find a more stable way to test the mendeley implementation or remove it entirely 
    def test_entry_list_to_path(self):
        bibtex_entry_list = []
        bibtex_entry_list.append(bibtexc.BibtexEntry.from_doi(doi="10.1556/Select.2.2001.1-2.14"))
        bibtex_entry_list.append(bibtexc.BibtexEntry.from_doi(doi="10.1139/x91-151"))

        # check plain style
        test_file = "plain.bib"
        bibtexc.entry_list_to_path(test_file, bibtex_entry_list, "plain")

        with open(test_file, "r") as f:
            result = f.read()

        target_string = """\
                           @article{Meszena2002Selection,
                            author = {Meszéna, G. and Kisdi, É. and Dieckmann, U. and Geritz, S. a. H. and Metz, J. a. J.},
                            doi = {10.1556/Select.2.2001.1-2.14},
                            journal = {Selection},
                            link = {http://dx.doi.org/10.1556/Select.2.2001.1-2.14},
                            number = {1-2},
                            pages = {193-220},
                            title = {Evolutionary Optimisation Models and Matrix Games in the Unified Perspective of Adaptive Dynamics},
                            volume = {2},
                            year = {2002}
                           }
                          
                          @article{Korol1991CanadianJournalofForestResearch,
                           author = {Korol, R. L. and Running, S. W. and Milner, K. S. and Hunt Jr., E. R.},
                           doi = {10.1139/x91-151},
                           journal = {Canadian Journal of Forest Research},
                           link = {http://dx.doi.org/10.1139/x91-151},
                           number = {7},
                           pages = {1098-1105},
                           title = {Testing a mechanistic carbon balance model against observed tree growth},
                           volume = {21},
                           year = {1991}
                          }
                        """
        self.maxDiff = None
        self.assertEqual(remove_indentation(result), remove_indentation(target_string))

        # check BibTeX style
        test_file = "BibTeX.bib"
        bibtexc.entry_list_to_path(test_file, bibtex_entry_list, "BibTeX")

        with open(test_file, "r") as f:
            result = f.read()

        target_string = r"""@article{Meszena2002Selection,
                             author = {Mesz{\'e}na, G. and Kisdi, {\'E}. and Dieckmann, U. and Geritz, S. a. H. and Metz, J. a. J.},
                             doi = {10.1556/Select.2.2001.1-2.14},
                             journal = {Selection},
                             link = {http://dx.doi.org/10.1556/Select.2.2001.1-2.14},
                             number = {1-2},
                             pages = {193-220},
                             title = {{E}volutionary {O}ptimisation {M}odels and {M}atrix {G}ames in the {U}nified {P}erspective of {A}daptive {D}ynamics},
                             volume = {2},
                             year = {2002}
                            }
                           
                            @article{Korol1991CanadianJournalofForestResearch,
                             author = {Korol, R. L. and Running, S. W. and Milner, K. S. and Hunt Jr., E. R.},
                             doi = {10.1139/x91-151},
                             journal = {Canadian Journal of Forest Research},
                             link = {http://dx.doi.org/10.1139/x91-151},
                             number = {7},
                             pages = {1098-1105},
                             title = {{T}esting a mechanistic carbon balance model against observed tree growth},
                             volume = {21},
                             year = {1991}
                            }
                        """

        self.assertEqual(remove_indentation(result), remove_indentation(target_string))

        # check BibLaTeX style
        test_file = "BibLaTeX.bib"
        bibtexc.entry_list_to_path(test_file, bibtex_entry_list, "BibLaTeX")

        with open(test_file, "r") as f:
            result = f.read()

        target_string = """\
                           @article{Meszena2002Selection,
                            author = {Meszéna, G. and Kisdi, É. and Dieckmann, U. and Geritz, S. a. H. and Metz, J. a. J.},
                            doi = {10.1556/Select.2.2001.1-2.14},
                            journaltitle = {Selection},
                            link = {http://dx.doi.org/10.1556/Select.2.2001.1-2.14},
                            number = {1-2},
                            pages = {193-220},
                            title = {{E}volutionary {O}ptimisation {M}odels and {M}atrix {G}ames in the {U}nified {P}erspective of {A}daptive {D}ynamics},
                            volume = {2},
                            year = {2002}
                           }
                          
                           @article{Korol1991CanadianJournalofForestResearch,
                            author = {Korol, R. L. and Running, S. W. and Milner, K. S. and Hunt Jr., E. R.},
                            doi = {10.1139/x91-151},
                            journaltitle = {Canadian Journal of Forest Research},
                            link = {http://dx.doi.org/10.1139/x91-151},
                            number = {7},
                            pages = {1098-1105},
                            title = {{T}esting a mechanistic carbon balance model against observed tree growth},
                            volume = {21},
                            year = {1991}
                           }
                        """

        self.assertEqual(remove_indentation(result), remove_indentation(target_string))



