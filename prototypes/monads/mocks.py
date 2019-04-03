from either import Left,Right
import attr
@attr.s
class ModelDescriptorMock(object):
    doi_org_available=attr.ib(default=False)
    doi_present=attr.ib(default=True)
    local_bibtex_entry_available=attr.ib(default=True)


    def local_bibtex_entry(self):
        # mock 
        if self.local_bibtex_entry_available:
            return Right({"author":"Markus"})
        else:
            return Left("No local BibtexEntry")
    def bibtex_entry(self):
        lbe=self.local_bibtex_entry()
        return lbe
        #if lbe.is_left:



