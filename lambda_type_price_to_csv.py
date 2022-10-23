# -*- coding: utf-8 -*-
"""
This function generates price of lambda type by regions.
 
"""

import pandas as pd
import time
import requests
t = time.time()

TIME_MS = int(t * 1000)


HEADERS = {"Accept-Encoding": "gzip, deflate, br",
           "Origin": "https://aws.amazon.com",
           "Sec-Fetch-Mode": "cors",
           "Sec-Fetch-Site": "cross-site",
           "Cache-Control": "no-cache",
           "Sec-Fetch-Dest": "empty",
           }

PRICE_BY_REGION_URL = 'https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/lambda/USD/current/lambda.json?timestamp={value}'.format(value=TIME_MS) 

REGION_CODE_URL = 'https://b0.p.awsstatic.com/locations/1.0/aws/current/locations.json?timestamp={value}'.format(value=TIME_MS)


'''
Get lambda type price for each region.
The response doesn't return region code with it.
'''
def get_price_by_region ():
    resp = requests.get(PRICE_BY_REGION_URL, headers=HEADERS)

    region_price_dict = resp.json()
    
    
    price_list=[]

    for key, val in region_price_dict['regions'].items():
        for key1, val2 in val.items():
            price_list.append([key, key1, val2['price']])
            
    return (price_list)


'''
Get region code and region name.
'''
def get_region_code ():
    resp = requests.get(REGION_CODE_URL, headers=HEADERS)

    region_code_dict = resp.json()
    
    region_list =[]

    for k,v in region_code_dict.items():
        region_list.append([k,v['code']])

            
    return (region_list)
   

'''
merge region_list and price_list so that price_list now as has region_code.
End result will have:
    Region Name, Lambda type, price, region_code
'''
def price_to_csv (price_list,code_list):
    df_price_list = pd.DataFrame (price_list, columns = ['Region Name', 'Lambda Type', 'Price'])
    
    df_code_list = pd.DataFrame(code_list, columns = ['Region Name', 'RegionCode'])
    
    df_price_by_code = df_price_list.merge(df_code_list)
    
    df_price_by_code.to_csv('./lambda_price_by_region_code.csv',index=False)


def main():        
    price_list = get_price_by_region()
    code_list = get_region_code()
    price_to_csv(price_list,code_list)

if __name__ == '__main__':
    main()
