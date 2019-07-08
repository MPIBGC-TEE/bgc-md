from pathlib import Path
from bgc_md.resolve.predefinedTypes import CompartmentalMatrix,InternalFlux
from bgc_md.resolve.helpers import populated_namespace_from_path
ns=populated_namespace_from_path( Path('models','Model1','Source.py') )
print(ns['__annotations__'])
