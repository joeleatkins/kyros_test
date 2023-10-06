# this program tracks the individuals loyalty points as they earn, use, and lose them
# we will document each section



# A - load inputs ----
# load libraries
import pandas as pd
import os

# load path and program name
os.chdir('c:\\Users\\Yoel\\test\\JoelAtkins\\data')

# read and set DATA_PATH
# reading the path and name separately seems ineffecient, but I'm trying to stay close the instructions
with open("path.py","r") as txtfile:
    FILE_PATH=txtfile.read()
exec(FILE_PATH)
FILE = DATA_PATH + '/' + DATA_NAME



# B - Create a dictionary with Key/Value pairs that are used in the fifo function ----
FIFO_ARGS = {'input_file': FILE,
             'earn' : ['earn_air','earn_other','earn_lodging','earn_package','earn_credit_card'],
             'burn' : ['rdm_package','rdm_lodging','exp']}



# C - FIFO algorithm ---------
def fifo(input_file,earn,burn):

#    earn = ['earn_air','earn_other','earn_lodging','earn_package','earn_credit_card']
#    burn = ['rdm_package','rdm_lodging','exp']

    # IMPORT INPUT FILE USING THE DATA_PATH ARGUMENT
    transactions = pd.read_csv(input_file)
    transactions.sort_values(by=["id","transactionDate", "transactionID"])

    # INSERT FIFO LOGIC
    # first split data into two - and rename the columns so we can join them later
    # also add a row at the end that we won't use so that we can increment to it when we finish the last row
    burn_tr = transactions.loc[transactions['transactionType'].isin(burn)]
    new_burn = transactions.iloc[[0]]
    burn_tr = pd.concat([burn_tr, new_burn], ignore_index=True)
    burn_tr.loc[burn_tr.shape[0]-1,'id'] = 1e10
    burn_tr = burn_tr.rename(columns={'transactionID': 'transactionID_burn',
                                      'transactionDate': 'transactionDate_burn',
                                      'transactionType': 'transactionType_burn',
                                      'value': 'value_burn'})
                
    # also, only keep ones that burn some points
    earn_tr = transactions.loc[transactions['transactionType'].isin(earn)]
    earn_tr = earn_tr.rename(columns={'transactionID': 'transactionID_earn',
                                      'transactionDate': 'transactionDate_earn',
                                      'transactionType': 'transactionType_earn',
                                      'value': 'value_earn'})

    # combine the two files
    
    # first add placeholders - we'll keep these when there's no burning
    earn_tr.insert(5,'transactionID_burn','none')
    earn_tr.insert(6,'transactionDate_burn','none')
    earn_tr.insert(7,'transactionType_burn','none')
    earn_tr.insert(8,'value_burn',0)
    earn_tr.insert(9,'fifo',0)
        
    # initialize some parameters
    row_earn = 0
    row_burn = 0
    id_carryover = 0
    counter = 0
    
    # loop through earn transactions as that is our base
    while row_earn < earn_tr.shape[0]:
        # default to set fifo to value earn, we'll overwrite it later if we have a corresponding burn record
        earn_tr.loc[row_earn,'fifo'] == earn_tr.loc[row_earn,'value_earn']
        # if the row ids are different and there are more rows, let's go to the next burn row 
        while earn_tr.loc[row_earn,'id'] > burn_tr.loc[row_burn,'id'] | row_burn < burn.shape[0]:
            row_burn = row_burn + 1

        # if we have remaining burn rows, let's consider them
        if earn_tr.loc[row_earn,'id'] == burn_tr.loc[row_burn,'id']:
            # set large carryovers if it's a new id - this means that we won't limit the earn or burn value
            if earn_tr.loc[row_earn,'id'] != id_carryover:
                earn_carryover = 1e9
                burn_carryover = 1e9
            # copy the relevant columns
            earn_tr.loc[row_earn,'transactionID_burn'] = burn_tr.loc[row_burn,'transactionID_burn']
            earn_tr.loc[row_earn,'transactionDate_burn'] = burn_tr.loc[row_burn,'transactionDate_burn']
            earn_tr.loc[row_earn,'transactionType_burn'] = burn_tr.loc[row_burn,'transactionType_burn']
            earn_tr.loc[row_earn,'value_burn'] = burn_tr.loc[row_burn,'value_burn']
            # fifo is the smaller of the earned, the carryover earned if we repeated the row, the burn,
            # or the carryover burn if we repeated a row
            earn_tr.loc[row_earn,'fifo'] = min(earn_tr.loc[row_earn,'value_earn'],earn_carryover,
                                               burn_tr.loc[row_burn,'value_burn'],burn_carryover)
            # if we earned more than we burned, let's repeat the earn row and carry over the remaining
            # earned points and go to the next burn row
            if min(earn_tr.loc[row_earn,'value_earn'],earn_carryover) > min(burn_tr.loc[row_burn,'value_burn'],burn_carryover):
                earn_carryover = min(earn_carryover,earn_tr.loc[row_earn,'value_earn']) - earn_tr.loc[row_earn,'fifo']
                burn_carryover = 1e9
                row_burn = min(transactions.shape[0]-1,row_burn+1) 
                # and make a new row for the rest of the earn
                earn_tr.loc[row_earn+0.5] = earn_tr.loc[row_earn]
                earn_tr = earn_tr.sort_index().reset_index(drop = True)
                counter = counter+1
                # and reset its values since we didn't work on it yet           
                earn_tr.loc[row_earn+1,'transactionID_burn'] = 'none'
                earn_tr.loc[row_earn+1,'transactionDate_burn'] = 'none'
                earn_tr.loc[row_earn+1,'transactionType_burn'] = 'none'
                earn_tr.loc[row_earn+1,'value_burn'] = 0
                earn_tr.loc[row_earn+1,'fifo'] = 0
            # if we burned more than we earned, let's repeat the burn row and carry over the remaining
            # burned points
            elif min(earn_tr.loc[row_earn,'value_earn'],earn_carryover) < min(burn_tr.loc[row_burn,'value_burn'],burn_carryover):
                burn_carryover = min(burn_carryover,burn_tr.loc[row_burn,'value_burn']) - earn_tr.loc[row_earn,'fifo']
                earn_carryover = 1e9
            # if we exactly used all the earned points, let's also go to the next burn row
            else:
                burn_carryover = 1e9
                earn_carryover = 1e9
                row_burn = min(burn_tr.shape[0]-1,row_burn+1)                
        id_carryover = earn_tr.loc[row_earn,'id']
        row_earn = row_earn + 1
    
    # UPDATE OUTPUT AND ENSURE THAT OUTPUT FOLLOWS SUBMISSION GUIDELINES
    fifo_df = earn_tr

    return fifo_df


points = fifo(**FIFO_ARGS)

# we only want rows where some points were burned
points_thin = points.loc[points['value_burn'] > 0]
points_thin.sort_values(by=["id","transactionDate_burn", "transactionID_burn","transactionDate_earn","transactionID_earn"])

points_thin.to_csv('C:/Users/Yoel/test/JoelAtkins/data/df_output.csv')
