# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 17:21:59 2020

@author: alain
"""

# # Some simple new features (percentages)
# df['DAYS_EMPLOYED_PERC'] = df['DAYS_EMPLOYED'] / df['DAYS_BIRTH']
# df['INCOME_CREDIT_PERC'] = df['AMT_INCOME_TOTAL'] / df['AMT_CREDIT']
# df['INCOME_PER_PERSON'] = df['AMT_INCOME_TOTAL'] / df['CNT_FAM_MEMBERS']
# df['ANNUITY_INCOME_PERC'] = df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']
# df['PAYMENT_RATE'] = df['AMT_ANNUITY'] / df['AMT_CREDIT']


# constantes
CREDIT_GRANT = "Credit grant" # colonne créée dans le DF pour l'accord de crédit en fonction de 'TARGET'

top_variables = [
    'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY','AMT_GOODS_PRICE',
    #
    'DAYS_BIRTH', 'CODE_GENDER', 'DAYS_EMPLOYED',
    #        
    'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'DAYS_LAST_PHONE_CHANGE',
    #
    'REGION_POPULATION_RELATIVE',
    #
    'CNT_FAM_MEMBERS',
    # 'NAME_EDUCATION_TYPE', -> catégorielle
    'OWN_CAR_AGE',
    #
    'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3'
    ]

# Variables qu'on peut éditer pour faire de nouvelles prédictions
editable_var = [
    'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY','AMT_GOODS_PRICE',
    'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'DAYS_LAST_PHONE_CHANGE',
    'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3'
    ]

# Variables qu'on peut afficher en graphe
graphable_var = [
    'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY','AMT_GOODS_PRICE',
    'DAYS_BIRTH', 'DAYS_EMPLOYED',
    'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'DAYS_LAST_PHONE_CHANGE',
    'REGION_POPULATION_RELATIVE',
    # 'CNT_FAM_MEMBERS',
    'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3'
    ]

MONEY, DAYS, UNIT = 'MONEY', 'DAYS', 'UNIT'
type_var = {}
type_var[MONEY] = ['AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY','AMT_GOODS_PRICE']
type_var[DAYS] = ['DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'DAYS_LAST_PHONE_CHANGE', 'OWN_CAR_AGE']
type_var[UNIT] = ['REGION_POPULATION_RELATIVE', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3']

range_options = {}
range_options[MONEY] = ['min', '-10000', '-5000', '-2000', '+2000', '+5000', '+10000', 'max']
range_options[DAYS] = ['min', '-10', '-5', '-2', '+2', '+5', '+10', 'max']
range_options[UNIT] = ['min', '-10', '-5', '-2', '+2', '+5', '+10', 'max']

cust_var = {}
#Personal
cust_var['PERSONAL'] = {
    'CODE_GENDER' : 'Gender', # 'M', 'F', 'XNA'
    'CNT_CHILDREN' : 'Number of children',
    'NAME_FAMILY_STATUS' : 'Family status', # 'Single / not married', 'Married', 'Civil marriage', 'Widow', 'Separated', 'Unknown'
    'NAME_EDUCATION_TYPE' : 'Highest education achieved', #'Secondary / secondary special', 'Higher education', 'Incomplete higher', 'Lower secondary', 'Academic degree'
    'CNT_FAM_MEMBERS' : 'Number of family members',    
    'DAYS_BIRTH' : "Client's age"
    }    

#Income & occupation
cust_var['INCOME_OCCUPATION'] = {    
    'NAME_INCOME_TYPE' : 'Income type', # 'Working', 'State servant', 'Commercial associate', 'Pensioner', 'Unemployed', 'Student', 'Businessman', 'Maternity leave'
    'OCCUPATION_TYPE' : 'Kind of occupation', # 'Laborers', 'Core staff', 'Accountants', 'Managers', nan,'Drivers', 'Sales staff', 'Cleaning staff', 'Cooking staff' etc.
    'AMT_INCOME_TOTAL' : 'Income of the client',
    'DAYS_EMPLOYED' : 'Current employment'
    }

# Housing & owning / # logements et biens matériels
cust_var['HOUSING_OWNING'] = {
    'FLAG_OWN_REALTY' : 'Client owns a house/flat', #'Y', 'N'
    'NAME_HOUSING_TYPE' : 'Housing situation', # 'House / apartment', 'Rented apartment', 'With parents', 'Municipal apartment', 'Office apartment', 'Co-op apartment'    
    'FLAG_OWN_CAR' : 'Owns a car', # 'Y', 'N'
    'OWN_CAR_AGE' : 'Age of car',
    'REGION_POPULATION_RELATIVE' : 'Population of region (normalized)'
    }

#Loan
cust_var['LOAN'] = {
    'NAME_CONTRACT_TYPE' : 'Loan type', # 'Cash loans', 'Revolving loans'
    'AMT_CREDIT' : 'Credit amount of the loan',
    'AMT_ANNUITY' : 'Loan annuity',
    'AMT_GOODS_PRICE' : 'Price of the goods'
    }

# informations internes relatives au client
cust_var['INTERNAL'] = {
    'DAYS_REGISTRATION' : 'Registration change (before app.)',
    'DAYS_ID_PUBLISH' : 'Identity document change (before app.)',
    'DAYS_LAST_PHONE_CHANGE' : 'Last phone change (before app.)',    
    'EXT_SOURCE_1' : 'External source 1',
    'EXT_SOURCE_2' : 'External source 2',
    'EXT_SOURCE_3' : 'External source 3'
    }

#####

# var_group = {
#     'Personal' : 'PERSONAL',
#     'Income & occupation' : 'INCOME_OCCUPATION',
#     'Housing & owning' : 'HOUSING_OWNING',
#     'Loan' : 'LOAN',
#     'Internal info' : 'INTERNAL'
#     }

var_group = {
    'PERSONAL' : 'Personal',
    'INCOME_OCCUPATION' : 'Income & occupation',
    'HOUSING_OWNING' : 'Housing & owning',
    'LOAN' : 'Loan',
    'INTERNAL' : 'Internal info'
    }
