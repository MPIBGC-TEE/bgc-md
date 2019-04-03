
#pseudo website report.

from mocks import ModelDescriptorMock 
def realy_cite(be):
    print("This is a real citation")
    return str(be)

def cite(either_bibtex_or_error):
    if either_bibtex_or_error.is_left:
        return "Instead of a bibtex_entry i got the message"+either_bibtex_or_error.value
    else:
        return either_bibtex_or_error.flat_map(realy_cite)


b1=ModelDescriptorMock(doi_org_available=False,doi_present=True,local_bibtex_entry_available=True).bibtex_entry()

b2=ModelDescriptorMock(doi_org_available=False,doi_present=True,local_bibtex_entry_available=False).bibtex_entry()

report= cite(b1)+cite(b2)
print(report)

