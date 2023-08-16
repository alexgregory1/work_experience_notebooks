import pandas as pd

def prob_calc(dataframe):
    probabilities = pd.DataFrame(dataframe)
    total = dataframe.loc[:,dataframe.columns[1]]
    
    count = 2

    # Iterates through columns in dataframe
    for num in range(len(dataframe.columns)-2):
        column = dataframe.loc[:,dataframe.columns[count]]
        cell_count = 0
        # Iterates through items in each column
        for row in column:
            #Divides current cell by the item at the start of the row
            probabilities.loc[:, dataframe.columns[count]].at[cell_count] = row / total[cell_count]
            cell_count += 1
        count += 1
    
    return probabilities