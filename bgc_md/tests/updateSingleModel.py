# vim:set ff=unix expandtab ts=4 sw=4:
from pathlib import Path
from bgc_md.Model import Model
from bgc_md.reports import report_from_model

# we could make this a commandline tool that takes one argument
# the yaml_file_name
yaml_file_name="../data/SoilModels/Zelenev2000MicrobialEcology.yaml"
target_dir_path=Path(yaml_file_name).parent
html_dir_path = target_dir_path.joinpath("html")
model=Model.from_file(yaml_file_name)
html_file_path = html_dir_path.joinpath(model.yaml_file_path.stem,"Report.html")
html_dir_path.mkdir(exist_ok=True,parents=True)
rel = report_from_model(model) 
rel.write_pypandoc_html(html_file_path)

