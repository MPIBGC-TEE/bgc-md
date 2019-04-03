from either import Left,Right
import attr
@attr.s
class ModelDescriptorMock(object):
        doi_org_available=False
        doi_present=True
        local_bibtex_entry_available=True
    def local_bibtex_entry(self):
        # mock 
        if self.local_bibtex_entry_available:
            return Right({"author":"Markus"})
        else:
            return Left("No local BibtexEntry")
    def bibtex_entry(self):
        return Right({"author":"Markus"})

