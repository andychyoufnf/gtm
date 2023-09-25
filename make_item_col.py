import pandas as pd
import numpy as np
import sys



excel = "24S ST"
df = pd.read_excel(f"{excel}.xlsx")
output = []

for i, row in df.iterrows():
    row = row.to_list()
    item_split = row[2].split(' ')
    item = item_split[0]
    item_nm = item_split[1].replace("(","").replace(")","")
    row.insert(3, item)
    row.insert(4, item_nm)
    output.append(row)

columns = ['parent_prdt_kind_nm_excel', 'prdt_kind_nm_excel', 'item_nm_excel', 'item', 'item_nm', 'domain1_nm', 'domain2_nm', 'repr_cd', 'part_cd', 'prdt_nm', 'prdt_nm_eng', 'color_cd', 'plan_price', 'fit_nm', 'fab_nm', 'fab_description1', 'fab_description2', 'fab_nm_shoes', 'fab_description_shoes', 'dsgnr_nm', 'dsgnr_mtrls_nm', 'dsgnr_goods_nm', 'dsgnr_td_nm', 'dsgnr_plan_nm', 'description', 'sesn_nonsesn']


dw = pd.DataFrame(output, columns=columns)
dw.to_excel(f"./{excel}_with_item.xlsx", index=False)


    
