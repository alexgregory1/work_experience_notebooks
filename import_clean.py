import os, pathlib
import pandas as pd
import warnings

root = pathlib.Path("data")

region_sizes = {"Country" : "ctry",
                "Region" : "rgn",
                "Upper-Tier Local Authority" : "utla",      #153 in England
                "Lower-Tier Local Authority" : "ltla",      #296 in England
                "Middle-Layer Super Output Area" : "msoa",  #2000-6000 households; 5000-15000 persons
                "Lower-Layer Super Output Area" : "lsoa",   #400-1200 households; 1000-3000 persons
                "Output Area" : "oa"}                       #40-250 households; 100-625 persons

region_indices = {3 : "ctry", #how many are per country
                  10 : "rgn",
                  174 : "utla",
                  331 : "ltla",
                  7264 : "msoa",
                  35672 : "lsoa",
                  188800 : "oa"}

regions = list(region_sizes.values())

def import_data(region : str, target_groups : list = None, target_codes: list = None): 
    '''Imports target census data\n
    Parameters:\n
        region, should be string of one of the following: ctry, rgn, utla, ltla, msoa, lsoa, oa\n
        target_groups, should be a list of strings of the descriptions of the data values as found at https://www.nomisweb.co.uk/census/2021/bulk\n
        target_codes, should be a list of strings of the codes of the data values as found at https://www.nomisweb.co.uk/census/2021/bulk\n
    Note: one of the two target parameters must be passed\n

    Returns dictionary of "Data type code" : Pandas DataFrame'''
    if target_groups == None and target_codes == None:
        raise ValueError("Need specified groups to import")
    
    region = str(region)
    if region not in regions:
        regions_error = '\n'.join(f"{key}  :  {val}" for key, val in region_sizes.items())
        raise ValueError(f"Region code must be one of the following: \nRegion  :  Region Code\n{regions_error}")
    
    codes = pd.read_csv(root / "census_codes.csv")
    codes["Filename"] = (
    codes["Filename"].str.split(".")
    .apply(lambda x: x[0])
    )

    if target_groups:
        valid_target_groups = [group for group in target_groups if group in codes["Description"].values]
        if len(valid_target_groups) == 0:
            raise ValueError("Inputs not found in code database, ensure the group names are as found on https://www.nomisweb.co.uk/census/2021/bulk")
        erroneous_groups = [group for group in target_groups if group not in valid_target_groups]
        output_erroneous_groups = '\n'.join(erroneous_groups)
        if len(erroneous_groups) > 0:
            warnings.warn(f"The following groups were not imported as they are invalid: {output_erroneous_groups}\nEnsure the group names are as found on https://www.nomisweb.co.uk/census/2021/bulk")
        
    if target_codes:
        valid_target_codes = [code for code in target_codes if code in codes["Code"].values]
        if len(valid_target_codes) == 0:
            raise ValueError("Inputs not found in code database, ensure codes are in the form 'TSXXX' where X's are digits, as found on https://www.nomisweb.co.uk/census/2021/bulk")
        erroneous_codes = [code for code in target_codes if code not in valid_target_codes]
        output_erroneous_codes = '\n'.join(erroneous_codes)
        if len(erroneous_codes) > 0:
            warnings.warn(f"The following codes were not imported as they are invalid: {output_erroneous_codes}\nEnsure codes are in the form 'TSXXX' where X's are digits, as found on https://www.nomisweb.co.uk/census/2021/bulk")
    
    if target_groups:
        target_codes = target_codes if target_codes is not None else []
        for group in valid_target_groups:
            valid_target_codes.append(codes.loc[codes["Description"] == group,"Code"].item())

    data = {}
    for code in valid_target_codes:
        folder = codes.loc[codes["Code"] == code, "Filename"].item()
        try:
            data.update({code : pd.read_csv(root / folder / f"{folder}-{region}.csv").drop(columns="date")})
        except FileNotFoundError:
            warnings.warn(f"File {folder}-{region}.csv not found in data/{folder}")
    
    return data

def import_all_data(region : str):
    '''Imports all installed census data\n
    Parameters:\n
        region, should be string of one of the following: ctry, rgn, utla, ltla, msoa, lsoa, oa\n
    Returns dictionary of "Data type code" : Pandas DataFrame
    '''
    region = str(region)
    if region not in regions:
        regions_error = '\n'.join(f"{key}  :  {val}" for key, val in region_sizes.items())
        raise ValueError(f"Region code must be one of the following: \nRegion  :  Region Code\n{regions_error}")

    codes = pd.read_csv(root / "census_codes.csv")
    codes["Filename"] = (
    codes["Filename"].str.split(".")
    .apply(lambda x: x[0])
    )
    
    data = {}
    for code in codes["Code"].values:
        folder = codes.loc[codes["Code"] == code, "Filename"].item()
        try:
            data.update({code : pd.read_csv(root / folder / f"{folder}-{region}.csv").drop(columns="date")})
        except FileNotFoundError:
            warnings.warn(f"File {folder}-{region}.csv not found in data/{folder}")
    
    return data

def cleanup_all(data : dict, remove_geography : bool = True, remove_geography_code : bool = True):
    '''
    Removes the specified columns from all dataframes\n
    Parameters:\n
        data, data to be cleaned, dictionary of "Data type code" : Pandas DataFrame\n
        remove_geography, whether to remove geography column, bool\n
        remove_geography-code, whether to remove geography code column, bool\n
        
    Returns dictionary of "Data type code" : Pandas DataFrame
    '''
    for key in data.keys():
        dataframe = data[key]
        try:
            if remove_geography:
                dataframe = dataframe.drop(columns="geography")
        except KeyError:
            pass
        try:
            if remove_geography_code:
                dataframe = dataframe.drop(columns="geography code")
        except KeyError:
            pass
        data[key] = dataframe
    return data

def cleanup(dataframe, columns : list):
    '''Removes specified columns from dataframe\n
    Parameters:\n
        dataframe, Pandas DataFrame to be cleaned\n
        columns, list of strings of column names to be removed\n
    '''
    if type(columns) is not list:
        raise ValueError("Parameter 'columns' must be a list")
    elif len([column for column in columns if type(column) is str]) == 0:
        raise ValueError("Parameter 'columns' must be a list of strings")  
    for column in columns:
        try:
            dataframe = dataframe.drop(columns=column)
        except KeyError:
            warnings.warn(f"Column {column} does not exist ")
    return dataframe

def factor_in_age(df):
    df_age = import_data(region_indices[len(df.index)], target_codes=["TS004"])["TS004"]
    df_age_totals_column = [column for column in list(df_age.columns) if "Total" in column][0]
    df_totals_column = [column for column in list(df.columns) if "Total" in column][0]
    df["Not Accounted For"] = df_age[df_age_totals_column] - df[df_totals_column]
    df[df_totals_column] = df_age[df_age_totals_column]
    df.rename(columns={df_totals_column:"Total"}, inplace=True)
    return df