# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 17:21:59 2020

@author: alain
"""

# from pathlib import Path
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import pickle
import kernel_1 as kn1
import dashboard1_var as dsh
# TOTO
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap


st.set_page_config(page_title='PRÊT à DÉPENSER', layout='wide')

# layout pour seaborn
sns.set_style("darkgrid")
shap.initjs()

@st.cache(suppress_st_warning=True)
def init_script(first):
    """
    Initialise les variables et instances d'objets utilisés dans tout le script
    first = True permet d'initialiser une seule fois les variables, puis utiliser le cache ensuite
    """
    num_rows = 2000
    # récupère le DF processed (utilisé pour le predict_proba)    
    # processed_df = kn1.get_df(debug=True, reload=True, process=True, num_rows=1000)
    # processed_df = kn1.get_df(debug = True, reload = True, process = True, num_rows=num_rows)
    
    
    processed_df = pd.read_csv('processed_df.csv', nrows= num_rows)
    processed_df = processed_df[processed_df['TARGET'].notnull()]    
    
    # récupère le DF brut (utilisé pour l'affichage')
    display_df = pd.read_csv('display_df.csv', nrows= num_rows)            
        
    # dictionnaire des MIN et MAX pour chaque variable éditable
    # recharge les dictionnaires
    min_var, max_var = {}, {}
    with open("min_max_feats", "rb") as input_file:
        min_var = pickle.load(input_file)
        max_var = pickle.load(input_file)
        feats = pickle.load(input_file)
    
    # charge le modèle entraîné
    with open("lightGBM_trained_model", "rb") as input_file:
        lightGBM_clf = pickle.load(input_file)    

    with open("shap_objects", "rb") as input_file:
        shap_explainer = pickle.load(input_file)
        shap_values = pickle.load(input_file)
     
        
    # shap_explainer = shap.TreeExplainer(lightGBM_clf)
    # shap_values = shap_explainer.shap_values(processed_df[feats])
        
    print('first init')
    
    return processed_df, display_df, feats, lightGBM_clf, min_var, max_var, shap_explainer, shap_values
 

#(allow_output_mutation=True)

@st.cache(allow_output_mutation=True)
def get_customer_from_df(sk_id_curr):
    """
    Récupère les infos client du DF

    """
    print('get_customer_from_df...\n')
    try:
        sk_id_curr = int(sk_id_curr)
    except ValueError:
        print('sk_id_curr non convertible en int. Arrêt du script')
        st.stop()   
    
    # extrait le DF processed (1 ligne) correspondant au client
    processed_customer_df = processed_df[ processed_df.SK_ID_CURR == sk_id_curr].copy()
    # extrait le DF brut (1 ligne) correspondant au client
    raw_customer_df = display_df[ display_df.SK_ID_CURR == sk_id_curr].copy()

    return processed_customer_df, raw_customer_df


def display_graph(var_name, var_label, cust_value, df, graph_type):
    """
    Affiche un graphe, soit histogramme de distribution, soit boxplot
    
    """
    # filtrage outliers
    outlier_thresh = 20 # seuil à X %
    q_down, q_up = np.nanpercentile(df[var_name].values, outlier_thresh), np.nanpercentile(df[var_name].values, 100-outlier_thresh)
    iqr = q_up - q_down
    cut_off = iqr * 1.5
    lower, upper = q_down - cut_off, q_up + cut_off        
    # df_filtered = [x for x in df[var_name].values if x >= lower and x <= upper]
    df_filtered = df[ (df[var_name] >= lower) &  (df[var_name] <= upper) ]
    
    # affichage graphe
    fig_1, g = plt.subplots(1,1, figsize=(4,2)) # figsize : largeur x hauteur
    # HISTOGRAMME
    if graph_type == 'HISTO':
        g = sns.distplot(df_filtered[var_name].values, kde=False, color='k') # distplot DEPRECATED -> utiliser displot
        # g = sns.displot(data=df, x=var_name, hue=dsh.CREDIT_GRANT, multiple="stack", palette="deep")
        g.set(xlabel = var_label, ylabel = "Number of clients")
    # BOXPLOT
    elif graph_type == 'BOXPLOT':        
        g = sns.boxplot(data=df_filtered, x=var_name, y=dsh.CREDIT_GRANT)       

    # Affiche les droites verticales pour : client, médiane        
    # mean=df[col].mean()
    #ax[i].axvline(mean, color='r', linestyle='--')    
    
    # median = np.nanmedian(df_filtered)
    # g.axvline(median, color='g', linestyle='-')
    g.axvline(cust_value, color='r', linestyle='-')
    g.legend({'Client':cust_value}) # 'Median':median,         
    
    st.pyplot(fig_1)                
    return

def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)


def display_customer_header(raw_customer_df, sk_id_curr):
    # affiche ID Client
    # client_idx = raw_customer_df.index[0]
    client_idx = processed_df[ processed_df.SK_ID_CURR == sk_id_curr].index

    print('client_idx', client_idx)
    # client_id_str = "Client ID : {}".format(str(raw_customer_df['SK_ID_CURR'].iloc[0]))
    st.write(str(sk_id_curr))

    # affiche l'interprétation SHAP    
    fig_1, ax_1 = plt.subplots(1,1, figsize=(10,5))    
    st_shap( shap.force_plot( shap_explainer.expected_value[1], shap_values[1][client_idx,:], processed_df[feats].loc[client_idx,:],
                    link='logit', figsize=(12,3) ) ) #shap_values[1]                      
    return
    
def display_var_section(raw_customer_df, var_group_name):
    """
    Affiche les infos client dans la colonne de gauche
    Retourne les variables saisie par l'utilisateur
    """
    # récupère le dict
    my_dict = dsh.cust_var[ var_group_name ]        
    # variables saisie par l'utilisateur dans les input
    user_var = {}    
    
    # affiche le nom de la section choisie
    st.header( dsh.var_group[var_group_name].upper() )
    
    
    # affiche chaque variable de la section choisie
    for var_name, var_label in my_dict.items():
        cust_value = raw_customer_df[var_name].values[0]
        # formatage de la valeur en fonction du type 
        # if type(cust_value) == np.float64:
        #     cust_value_fmt = "%.2f" % cust_value
        # elif type(cust_value) == np.int64:
        # cust_value_fmt = "%.0f" % cust_value
        # else:
        #     cust_value_fmt = str(cust_value)
        
        # formatage de la valeur en fonction du type DAYS, MONEY, UNIT            
        if var_name in dsh.type_var[dsh.DAYS]:
            cust_value_fmt = "{:.2f} years".format( float(cust_value) ) #*(-1)/365
            var_type = dsh.DAYS
        elif var_name in dsh.type_var[dsh.MONEY]:
            cust_value_fmt = "{:.0f} $".format( float(cust_value) )
            var_type = dsh.MONEY
        elif var_name in dsh.type_var[dsh.UNIT]:
            cust_value_fmt = "{:.2f}".format( float(cust_value) )
            var_type = dsh.UNIT
        else:
            cust_value_fmt = str(cust_value)                
        
        # chaîne à afficher : label de la variable et valeur de la variable
        str_2_write = var_label+' : '+cust_value_fmt
        
        # si la variable n'est ni éditable ni graphable, l'affiche en dur
        if ( (var_name not in dsh.editable_var) & (var_name not in dsh.graphable_var) ):
            st.write(str_2_write)
            # passe à la variable suivante
            continue
            
        # sinon l'affiche dans un expander_label
        expander_label = str_2_write
        
        with st.beta_expander(expander_label, expanded=False):
            # si la variable est éditable, affiche un text_input
            if var_name in dsh.editable_var:
                min_val = float(0)
                max_val = float(max_var[var_name])
                input_label = "Enter new value for prediction [ min : {:.2f} - max : {:.2f} ]".format(min_val, max_val) #min_var[var_name], max_var[var_name]
                user_var[var_name] = st.number_input(label=input_label, value=float(cust_value), 
                                                     format='%.2f', min_value = min_val, # min_var[var_name]
                                                     max_value = max_val, key=var_name) # max_var[var_name]
            
            # si la variable est graphable, affiche les checkboxes de graphe                
            if var_name in dsh.graphable_var:
                # select slider                    
                #range_options = ['min', '-10', '-5', '-2', '2', '5', '10', 'max']
                # start_range, end_range = st.select_slider('Select a range of comparison',
                #                                       options=dsh.range_options[var_type],
                #                                       value=('min', 'max'), key=var_name)  
                # CHECKBOX affichage histogram
                if st.checkbox(label='histogram', value=False, key='histo'+var_name):
                    # with right_column:                        
                    display_graph(var_name, var_label, cust_value, display_df, 'HISTO')    
                # CHECKBOX affichage boxplot
                if st.checkbox(label='boxplot', value=False, key='boxplot'+var_name):
                    # with right_column:  
                    display_graph(var_name, var_label, cust_value, display_df, 'BOXPLOT')                                                               
    #
    return user_var


def display_predict_proba(processed_customer_df): #, user_var):    
       
    # prédiction par le modèle    
    pred = model_clf.predict_proba(processed_customer_df[feats])[0][1] #, num_iteration=model_clf.best_iteration_
    print('processed_customer_df[var_name] : ',processed_customer_df[dsh.editable_var])
    print('Predict : ', pred)
    
    # affichage
    pred_str = "Default risk : \n{:.2f}%".format(pred*100)
    grant_str = 'Credit prediction :\n'
    
    if pred < model_threshold:
        pred_str += " < {:.0f}% (thresh.)".format(model_threshold*100)
        grant_str += 'favorable'
    else:
        pred_str += " > {:.0f}% (thresh.)".format(model_threshold*100)
        grant_str += 'not favorable'
        
    st.sidebar.write(pred_str)
    st.sidebar.write(grant_str)    
    return


# @st.cache(allow_output_mutation=True)
# def get_prev_sk_id(sk_curr):
           
#     return sk_curr



# initialise les objets du script au premier démarrage, utilise le cache ensuite
processed_df, display_df, feats, model_clf, min_var, max_var, shap_explainer, shap_values = init_script(first=True)

# seuil du modèle pour 'TARGET'
model_threshold = 0.1

# BARRE LATERALE
st.sidebar.image(image='dashboard-img.png')


    
# select box "identifiant client"
sk_id_curr = st.sidebar.selectbox(label='Client ID', options=display_df['SK_ID_CURR'], index=0, key='client_id')


if sk_id_curr is not None: # != prev_sk_id: 
    print('sk_id_curr : ', sk_id_curr)
    processed_customer_df, raw_customer_df = get_customer_from_df(sk_id_curr)
    # prev_sk_id = sk_id_curr
    # display_customer_header(raw_customer_df)
    # display_var_section(raw_customer_df, var_group_name='PERSONAL') #user_var = 

# bouton 'RELOAD' / TOTEST
# if st.sidebar.button(label='display', key='reload'):
#     processed_customer_df, raw_customer_df = get_customer_from_df(sk_id_curr)

display_customer_header(raw_customer_df, sk_id_curr)
display_var_section(raw_customer_df, var_group_name='PERSONAL')


# PREDICTION de PROBA CLIENT
if st.sidebar.button('Predict') or (processed_customer_df is not None): #
    display_predict_proba(processed_customer_df) #, user_var)

# affiche importance features 
fig_1, ax_1 = plt.subplots(1,1, figsize=(5,20))
shap.summary_plot(shap_values, processed_df[feats])
st.sidebar.pyplot(fig_1)
    
    
# CHECKBOXES : choix de la section à afficher ()
for var_group_name, var_group_label in dsh.var_group.items():
    if var_group_name != 'PERSONAL':
        if st.sidebar.checkbox(label=var_group_label, value=False, key=var_group_name):
            user_var = display_var_section(raw_customer_df, var_group_name)
            print('user_var : ', user_var)
            
            # met à jour 'processed_customer_df' avec les nouvelles variables
            print('\nmet à jour processed_customer_df avec les nouvelles variables')
            print('user_var.keys() : ', user_var.keys())
            for var_name in user_var.keys(): #dsh.editable_var:
                # try:
                processed_customer_df[var_name] = user_var[var_name]
                print(var_name, ' : ', user_var[var_name])    



