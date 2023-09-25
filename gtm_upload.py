import pandas as pd
import numpy as np
from tkinter import Tk, Label, Entry
from tkinter.filedialog import askopenfilenames
import sys
from sqlalchemy import create_engine

'''
---------------------- SET PARAMETER ----------------------
'''

# EXCEL SETTING
# COLUMN_LIST = ['parent_prdt_kind_nm_excel', 'prdt_kind_nm_excel', 'item_nm_excel', 'domain1_nm', 'domain2_nm', 'repr_cd', 'part_cd', 'prdt_nm', 'prdt_nm_eng', 'color_cd', 'plan_price', 'fit_nm', 'fab_nm', 'fab_description1', 'fab_description2', 'fab_nm_shoes', 'fab_description_shoes', 'dsgnr_nm', 'dsgnr_mtrls_nm', 'dsgnr_goods_nm', 'dsgnr_td_nm', 'dsgnr_plan_nm', 'description', 'sesn_nonsesn'] 
COLUMN_LIST = ['parent_prdt_kind_nm_excel', 'prdt_kind_nm_excel', 'item_nm_excel', 'item', 'item_nm', 'domain1_nm', 'domain2_nm', 'repr_cd', 'part_cd', 'prdt_nm', 'prdt_nm_eng', 'color_cd', 'plan_price', 'fit_nm', 'fab_nm', 'fab_description1', 'fab_description2', 'fab_nm_shoes', 'fab_description_shoes', 'dsgnr_nm', 'dsgnr_mtrls_nm', 'dsgnr_goods_nm', 'dsgnr_td_nm', 'dsgnr_plan_nm', 'description', 'sesn_nonsesn']

# 기본 설정
BRAND_CODE = 'ST' # V I M ST
RAW_TABLE = 'temp_dw_23s_gtm_excel'
FILE_NAME = f'23S ST_with_item.xlsx'

# DB 설정
# 운영계
REDSHIFT_ENGINE = create_engine("postgresql://data_user:Duser2022!#@prd-dt-redshift.conhugwtudej.ap-northeast-2.redshift.amazonaws.com:5439/fnf")
# 개발계
LOCAL_POSTGRESQL_ENGINE = create_engine("postgresql+psycopg2://postgres:1111@172.0.2.93:5432/postgres")
AWS_POSTGRESQL_ENGINE = create_engine("postgresql+psycopg2://postgres:fnf##)^2020!@fnf-process.ch4iazthcd1k.ap-northeast-2.rds.amazonaws.com:35430/postgres")
'''
-----------------------------------------------------------
'''


def open_files():
    # 파일 GUI로 선택
    Tk().withdraw()
    open_file_name = askopenfilenames()
    return open_file_name


def read_excel2df(open_file_name):
    # 1. 엑셀 파일에서 데이터프레임 추출
    df = pd.read_excel(open_file_name, header=None, skiprows=[0]) 

    # 2. 추출한 데이터프레임에 컬럼명 할당
    df.columns = COLUMN_LIST

    # 3. 추출한 데이터프레임에 브랜드코드 컬럼 추가
    df['brd_cd'] = BRAND_CODE
    return df

def update_df2redshift(dataframe, raw_table):
    # 4. 데이터프레임을 DB에 업로드
    dataframe.to_sql(name = f'{raw_table}',
                    con = REDSHIFT_ENGINE,
                    schema = 'gtm',
                    if_exists = 'append',
                    index = False,
                    chunksize=1000,
                    method='multi'
                    )
    

if __name__ == '__main__':
    try:
        # 파일명은 파일이 저장된 곳으로 변경 필요
        file = f"./{FILE_NAME}"
        df = read_excel2df(file)
        print(df)
        update_df2redshift(df, RAW_TABLE)
        print('-------------------END-------------------')
    
    except Exception  as e:
        print(e)