from bgc_md.ModelList import ModelList
from bgc_md.reports import create_overview_report

from pathlib import Path
p=Path("..","bgc_md","data","tested_records")
ml=ModelList.from_dir_path(p)
for m in ml:
    print(m)
create_overview_report(ml,target_dir_path=Path("output",output_file_name='list.html'))
