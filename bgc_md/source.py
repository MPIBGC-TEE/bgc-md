from bgc_md.Model  import Model
from bgc_md.ReportInfraStructure import Text,Math,Table,TableRow
from collections import OrderedDict
model=Model.from_file('data/all_records/Castanho2013Biogeosciences.yaml')
df=model.section_pandas_df('additional_variables')
