# Overview

Welcome to the KYROS Insights Coding Project! <br>
We are happy to have you take part in this mini-coding project.

## Background

For most [loyalty programs](https://www.investopedia.com/terms/l/loyalty-program.asp), members can earn points on purchases, and use those points to redeem on rewards. Sometimes, after a certain period of inactivity, those earned points can expire.

Every time a member earns or redeems points, or has their points expire, these transactions are recorded in a transactional database to be used for further analysis.

For this coding project, you are tasked with creating a First-In, First-Out [FIFO](https://www.investopedia.com/terms/f/fifo.asp) algorithm that allocates points redeemed and expired to points earned. You are provided an example transactional dataset and you are required to write logic in Python to produce the desired output.

Next Steps:
- [Installation Requirements](#installation-requirements)
- [Getting Started](#getting-started)
- [Submisson Guidelines](#submission-guidelines)
- [Submitting Your Work](#submitting-your-work)
- [Glossary](#glossary)

Details about the FIFO algorithm are described in the [Description of FIFO Algorithm](#description-of-fifo-algorithm) section.

Details about the required outputs are described in the [Submisson Guidelines](#submission-guidelines) section.

For any questions or concerns, please feel free to [Contact Us](mailto:robert.chin@kyrosinsights.com).


# Installation Requirements

* [Python](https://www.python.org): 3.6 or newer
* [Git](https://git-scm.com/): 1.7.0 or newer
* Repository is cloned on your local machine
    -   For more information, visit the [Azure DevOps website](https://docs.microsoft.com/en-us/azure/devops/repos/git/clone?view=azure-devops&tabs=command-line) to find out how to clone this repository onto your local machine.

Installing packages required is easily done using
`pip`. Assuming it is installed, just run the following from the command-line in the location of the cloned repository:

``` bash
pip install -r requirements.txt
```

# Getting Started

To get started:
1. [Installation Requirements](#installation-requirements) are installed
2. Create a new [branch](https://docs.microsoft.com/en-us/azure/devops/repos/git/branches?view=azure-devops&tabs=command-line) on your local machine
    -   The branch must have the prefix test/
        - For example: test/CandidateA
    -   All work must be completed on the branch 
3. Review the [Description of Inputs](#description-of-inputs)
4. Review the [Description of the FIFO Algorithm](##description-of-the-fifo-algorithm)

## Description of Inputs

| Type          | Location                                   | Comments              |
| ------------- |------------------------------------------- | --------------------- |
| Input Data    | [data/df_input.csv](data/df_input.csv)    |                       |
| Python Code   | [fifo/fifo.py](fifo/fifo.py)              | Updated for submission|


## Input Data Schema

| Position | Column Name    | PK / FK | Type*         | Comments        |
| -------- | -------------- | ------- | ------------- | --------------- |
| 1        | id             | FK      | int64         | Member ID       |
| 2        | transactionID  | PK      | int64         | Transaction ID  |
| 3        | transactionDate|         | datetime64[ns]| Transaction Date|
| 4        | transactionType|         | object        | *See table below|
| 5        | value*         |         | int64         |                 |

> _*Data types listed here are using Pandas Datatypes._ 

>_Value_ is always positive in the input dataset. Transactions flagged as _Redeemed Points_ or _Expired Points_ are used to reduce a member's _Earned Points_.

The data includes different categories for the column _transactionType_.

| transactionType   | Description                   |
| ----------------- | ----------------------------- |
| earn_air          | Earned Points on Air          |
| earn_other        | Earned Points on Other        |
| earn_lodging      | Earned Points on Lodging      |
| earn_package      | Earned Points on Package      |
| earn_credit_card  | Earned Points on Credit Card  |
| rdm_package       | Redeemed Points on Package    |
| rdm_lodging       | Redeemed Points on Lodging    |
| exp               | Expired Points                |

## Description of the FIFO Algorithm
 
To describe the logic for FIFO algorithm, we will use the example input below.

- For Member ID = 1, this member earns 100 points based on an air transaction in August 31, 2011 (Transaction ID = 1)
- During November 1, 2011, Member ID  = 1 redeems 50 of those points on a lodging reward (Transaction ID = 2)
    >- Because Member ID  = 1 has 100 _Earned Points_, the FIFO algorithm would allocate 50 _Redeemed Points_ to 50 out of 100 _Earned Points_ 
    >- Transaction ID = 2 would be allocated to Transaction ID = 1
    >- 50 _Earned Points_ would be remaining for Transaction ID = 1
- Member ID  = 1 then earns 25 and 50 points on package and lodging, respectively during November 9, 2011 and November 13, 2011 (Transaction ID = 3 and 4)
- Finally, because Member ID  = 1 was inactive for an extended period of time, the remainder of his points expired on April 30, 2016 (Transaction ID = 5)
    >- The FIFO Algorithm would allocate the 125 _Expired Points_ as followed:
    >- 50 _Expired Points_ would be allocated to the remaining 50 _Earned Points_ from Transaction ID = 1
    >- 25 _Expired Points_ would be allocated to the 25 _Earned Points_ from Transaction ID = 3
    >- 50 _Expired Points_ would be allocated to the 50 _Earned Points_ from Transaction ID = 4

- This exercise is then repeated for Member ID = 2


### Example of FIFO Algorithm

#### Example Input:
|id|transactionID|transactionDate    |transactionType |value|
|- |------------ |------------------ |--------------- |---- |
|1 |1            |2011-08-31 00:00:00|earn_air        |100  |
|1 |2            |2011-11-01 00:00:00|rdm_lodging     |50   |
|1 |3            |2011-11-09 00:00:00|earn_package    |25   |
|1 |4            |2011-11-13 00:00:00|earn_lodging    |50   |
|1 |5            |2016-04-30 01:00:00|exp             |125  |
|2 |6            |2011-11-01 00:00:00|earn_credit_card|15   |
|2 |7            |2011-11-09 00:00:00|earn_other      |22   |
|2 |8            |2011-11-13 00:00:00|rdm_package     |20   |


#### Example Output:
|id|transactionID_earn|transactionDate_earn|transactionType_earn|value_earn|transactionID_burn|transactionDate_burn|transactionType_burn|value_burn|fifo|
|- |----------------- |------------------- |------------------- |--------- |----------------- |------------------- |------------------- |--------- |--- |
|1 |1                 |2011-08-31 00:00:00 |earn_air            |100       |2                 |2011-11-01 00:00:00 |rdm_lodging         |50        |50  |
|1 |1                 |2011-08-31 00:00:00 |earn_air            |100       |5                 |2016-04-30 01:00:00 |exp                 |125       |50  |
|1 |3                 |2011-11-09 00:00:00 |earn_package        |25        |5                 |2016-04-30 01:00:00 |exp                 |125       |25  |
|1 |4                 |2011-11-13 00:00:00 |earn_lodging        |50        |5                 |2016-04-30 01:00:00 |exp                 |125       |50  |
|2 |6                 |2011-11-01 00:00:00 |earn_credit_card    |15        |8                 |2011-11-13 00:00:00 |rdm_package         |20        |15  |
|2 |7                 |2011-11-09 00:00:00 |earn_other          |22        |8                 |2011-11-13 00:00:00 |rdm_package         |20        |5   |  

>**Hint**: Zoom out to see the full table if it appears truncated.

# Submission Guidelines

To make a submission, the [fifo/fifo.py](fifo/fifo.py) code must be updated. The following steps give you a rough outline of what must be updated.  

## Step 1: Update the FIFO Arguments dictionary
```python
# Update this dictionary with Key/Value pairs that are used in the fifo function.
FIFO_ARGS = {}
```
- Use the dictionary provided to pass arguments to the fifo function
- These arguments would be used as part of your submission

>**Note**: Use the DATA_PATH when referencing the Input File

## Step 2: Update the FIFO Code
```python
def fifo(FIFO_ARGS):

    # TO DO: IMPORT INPUT FILE USING THE DATA_PATH ARGUMENT
    # TO DO: INSERT FIFO LOGIC
    # UPDATE OUTPUT AND ENSURE THAT OUTPUT FOLLOWS SUBMISSION GUIDELINES
    df_out = pd.DataFrame({"A": []})

    return df_out
```
>**Note**: This is the function that will be tested against!

- The function must be able to import the input data file
- Include any comments as you update the fifo function as these will be evaulated, for example pseudo-code
- Ensure coding clarity by conforming to PEP standards


## Step 3: Ensure that the output follow the following specifications

### Requirements for Outputs

| Position | Column Name         | PK / FK | Type*         |
| -------- | ------------------- | ------- | ------------- |
| 1        | id                  | FK      | int64         |
| 2        | transactionID_earn  | PK{1}   | int64         |
| 3        | transactionDate_earn|         | datetime64[ns]|
| 4        | transactionType_earn|         | object        |
| 5        | value_earn          |         | int64         |
| 6        | transactionID_burn  | PK{2}   | int64         |
| 7        | transactionDate_burn|         | datetime64[ns]|
| 8        | transactionType_burn|         | object        |
| 9        | value_burn          |         | int64         |
| 10       | fifo                |         | int64         |


>_*Data types listed here are using Pandas Datatypes._ 

- For this algorithm, you are required to show the original values, as well as a column for the FIFO allocation of points burned (i.e. Redeemed Points and Expired Points) to points earned. For the Redeemed and Expired values, you are to group them into the same column
- The output should only contain the records of _Points Earned_ and the associated FIFO allocation greater than 0 (i.e _fifo_ > 0)
- An example can be found in the previous section [Example Output](####example-output).

### Additional Requirements for Outputs

- Function must output a `pandas` Dataframe
- Output `pandas` Dataframe must be sorted by <br>
```python
[
    "id", 
    "transactionDate_burn", 
    "transactionID_burn", 
    "transactionDate_earn",
    "transactionID_earn"
]
```


## Step 4: Finalizing the Repository

- Update the [Requirements](requirements.txt) file for any additional packages used
- Include any supporting documents if necessary

## Limitations

- Packages not found in PyPi cannot be used.

# Submitting Your Work

Once you are ready to submit your work, [commit](https://docs.microsoft.com/en-us/azure/devops/repos/git/gitquickstart?view=azure-devops&tabs=command-line) and push the changes on your test branch to the remote server. 

This will automatically trigger a process that checks your outputs, and returns a resulting Succeeded/Failed result. An e-mail will also be sent to the candidate indicating the result.

>**Hint**: Navigating to the Repository home page and selecting your branch will display the status of the checking process. 
Additonally, the user can check the error messages associated with a Failed result. 

>**Note**: This process takes about 5 minutes to check.

You are allowed unlimited attempts for this project. To submit additional attempts, a new commit would need to be pushed to the remote server.

This project is expected to be completed within one week, however, extensions will be allowed for specific circumstances. 

Upon completion, we will reach out to you with next steps.

For any questions or concerns, please feel free to [Contact Us](mailto:robert.chin@kyrosinsights.com).

# Glossary

FIFO = First-In, First Out <br>
PK = Primary Key <br>
FK = Foreign Key <br>
Burn = Redeemed and Expired Points