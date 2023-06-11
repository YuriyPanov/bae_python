import pandas as pd
import numpy as np

def export_to_csv(tickets_info, file_name):
    tickets_for_df = {'Дата' : [], 'Сидячий' : [], 'Купе' : [], 'Плацкартный' : [], 'СВ' : []}
    for data in tickets_info:
        tickets_for_df['Дата'].append(data)
        tickets_for_df['Сидячий'].append(tickets_info[data]['Сидячий'])
        tickets_for_df['Купе'].append(tickets_info[data]['Купе'])
        tickets_for_df['Плацкартный'].append(tickets_info[data]['Плацкартный'])
        tickets_for_df['СВ'].append(tickets_info[data]['СВ'])

    tickets_df = pd.DataFrame.from_dict(tickets_for_df)
    tickets_df["Дата"] = pd.to_datetime(tickets_df["Дата"])

    tickets_df.loc[tickets_df['Сидячий'] == -1, 'Сидячий'] = np.nan
    tickets_df.loc[tickets_df['Купе'] == -1, 'Купе'] = np.nan
    tickets_df.loc[tickets_df['Плацкартный'] == -1, 'Плацкартный'] = np.nan
    tickets_df.loc[tickets_df['СВ'] == -1, 'СВ'] = np.nan
    tickets_df.to_csv(file_name, encoding = "utf-8-sig")  
    return tickets_df