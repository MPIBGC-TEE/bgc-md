        header = [Text(""), Text("Model"), Text(" Variables"), Text(" Parameters"), Text(" Constants"), Text("Component"), Text("Description"), Text("Expressions"), Text("fv/fs"), Text("Right hand side of ODE"), Text("Source")]
        table_format = list("lcccclcccl")
        header_row = TableRow(header)
        T = Table("Summary of the models in the database of Carbon Allocation in Vegetation models", header_row, table_format)
         
        #compar_keys=["state_vector_derivative"]
        #for index, model in enumerate(self):
        #    print(type(model))
        #    print(model.name)
        #    ## collect data for plots
        #    ##data_list = [model.name]
    
        #    #
        #    #
        #    ## create table
        #    #dir_name = model.yaml_file_path.stem
        #    #dir_path =target_dir_path.joinpath(dir_name)
        #    ## the link is relative to target dir since this file is created there 
        #    #report_link = str(dir_path.relative_to(target_dir_path).joinpath("Report.html"))
    
        #    #l = [Text(model.name)]         
        #    #rel2 += Text('<tbody>\n')
        #    #parity = ['odd','even'][(index+1) % 2]
        #    #rel2 += Text('<tr class="$p">\n', p=parity, i=index)
    
        #    #image_string = ""
        #    #reservoir_model = model.reservoir_model
        #    #if reservoir_model:
        #    #    dir_path.mkdir(parents=True,exist_ok=True)
        #    #    image_file_name="Thumbnail.svg"
        #    #    image_file_path = dir_path.joinpath(image_file_name)
        #    #    fig = reservoir_model.figure(thumbnail=True)
        #    #    fig.savefig(image_file_path.as_posix(), transparent=True)
        #    #    plt.close(fig)
        #    #    # the link is relative to target dir since thi file is created there 
        #    #    image_string = '<img src="' + str(image_file_path.relative_to(target_dir_path)) + '"> '
    
        #    #rel2 += Text('<td align="left">$image_string</td>', image_string=image_string)
        #    #rel2 += Text('<td align="left"><a href="$rl" target="_blank">$mn</a></td>\n', rl=report_link, mn=model.name)
    
        #    #l.append(Text(str(len(model.variables))))
        #    #rel2 += Text('<td align="center" onclick="ausklappen(\'comp_table_$i\');ausklappen(\'rhs_$i\')">$n</td>\n', i=index, n=str(len(model.variables)))
    
        #    #l += [Text(" ")]*5
        #    #rel2 += Text('<td align="center" onclick="ausklappen(\'comp_table_$i\');ausklappen(\'rhs_$i\')">$n</td>\n', i=index, n=str(len(model.parameters)))
        #    #rel2 += Text('<td align="center" onclick="ausklappen(\'comp_table_$i\');ausklappen(\'rhs_$i\')"></td>\n', i=index)
    
        #    #fv_fs_entry = Text(" ")
        #    #for row_dic in model.df.rows_as_dictionary:
        #    #    if row_dic['name'] in ('f_v', 'f_s'):
        #    #        if 'exprs' in row_dic.keys() and row_dic['exprs']:
        #    #            fv_fs_entry = exprs_to_element(row_dic['exprs'], model.symbols_by_type)
        #    #l.append(fv_fs_entry)
    
        #    #l.append(Math("$eq", eq=model.rhs))
        #    #rest = Text('<td align="center" style="vertical-align:middle" onclick="ausklappen(\'comp_table_$i\');ausklappen(\'rhs_$i\')"><div id="rhs_$i" style="display:none">', i=index) + Math("$eq", eq=model.rhs) + Text("</div></td>\n")
        #    #l.append(Citation(model.bibtex_entry, parentheses=False))
        #    #rest += Text('<td align="left" onclick="ausklappen(\'comp_table_$i\');ausklappen(\'rhs_$i\')">', i=index) + Citation(model.bibtex_entry, parentheses=False) + Text("</td>\n</tr>\n")
        #    #row = TableRow(l)
        #    #T.add_row(row)
    
        #    #rel2 += Text('<td align="center" onclick="ausklappen(\'comp_table_$i\');ausklappen(\'rhs_$i\')">', i=index) + fv_fs_entry
        #    #rel2 += Text('\n<div id="comp_table_$i" style="display:none">\n',i=index)
        #    #comp_t = Text('<table>\n<tr class="header">\n<th align="center">Component</th>\n<th align="left">Description</th>\n<th align="center">Expressions</th>\n</tr>\n</thead>\n')
        #    #comp_t += Text("<tbody>\n")
        #    #is_comp = False
        #    #for row_dic in model.df.rows_as_dictionary:
        #    #    if row_dic['category'] in ('components') and row_dic['name'] not in ('fv', 'fs'):
        #    #        is_comp = True
        #    #        l = [Newline()]*4
    
        #    #        l.append(Math("$sv", sv=sympify(row_dic['name'], locals=model.symbols_by_type)))
        #    #        comp_t += Text('<tr>\n<td align="center">') +Math("$sv", sv=sympify(row_dic['name'], locals=model.symbols_by_type)) + Text("</td>\n")
    
        #    #        if row_dic['desc']:
        #    #            l.append(Text("$d" , d=row_dic['desc']))
        #    #            comp_t += Text('<td align="left">$d</td>\n',d=row_dic['desc'])
        #    #        else:
        #    #            l.append(Text("-"))
        #    #            comp_t += Text('<td align="left">-</td>\n')
    
        #    #        if row_dic['exprs']:
        #    #            l.append(exprs_to_element(row_dic['exprs'], model.symbols_by_type))
        #    #            comp_t += Text('<td align="center">') + exprs_to_element(row_dic['exprs'], model.symbols_by_type) + Text("</td>\n")
        #    #        else:
        #    #            l.append(Text("-"))
        #    #            comp_t += Text('<td align="center">-</td>\n')
    
        #    #        l += [Newline()]*3
    
        #    #        row = TableRow(l)
        #    #        T.add_row(row)                    
        #    #        comp_t += Text("</tr>\n")
    
        #    #comp_t += Text("</tbody>\n</table>\n</td>\n")
        #    #if is_comp:
        #    #    rel2 += comp_t
        #    #rel2 += Text("</div>\n")
        #    #rel2 += rest
    
    
