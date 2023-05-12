import os
home_directory = os.path.expanduser( '~' )


Newdir = "phonepescrapper"
phngitcloned = os.path.join(home_directory, Newdir)
if not os.path.exists(phngitcloned):
    os.mkdir(os.path.join(home_directory, Newdir))

clone_command = "git clone https://github.com/PhonePe/pulse.git"
clone_with_path = clone_command  +" "+ phngitcloned
os.system(clone_with_path)

Newdir1= "data"

phngitcloneddata = os.path.join(phngitcloned, Newdir1)


import json
import pandas as pd
#path=r"C:\Users\kisho\Downloads\pulse-master\pulse-master2\pulse-master\data\aggregated\transaction\country\india\state\\"
p1 = r"C:\Users\kisho\Downloads\pulse-master\pulse-master2\pulse-master\data\\"


def Agg_trans(path):
    clm = {'State': [], 'Year': [], 'Quater': []}
    c = 0
    for i in Agg_state_list:
        p_i = path + i + "\\"
        Agg_yr = os.listdir(p_i)
        for j in Agg_yr:
            p_j = p_i + j + "\\"
            Agg_yr_list = os.listdir(p_j)
            for k in Agg_yr_list:
                p_k = p_j + k
                if p_k.endswith('.json'):
                    Data = open(p_k, 'r')
                    D = json.load(Data)
                for z in D['data']['transactionData']:
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
                    df = pd.json_normalize(D['data']['transactionData'], record_path=['paymentInstruments'], meta=['name'])
                if c == 0:
                    df1 = df
                    c = 1
                else:
                    # df1 = df1.append(df)
                    df1 = pd.concat([df1, df], ignore_index=True)


    Agg = pd.DataFrame(clm)
    df1_agg = df1.join(Agg, how='outer')
    # df1_agg = pd.concat([df1,Agg],axis = 1)
    return df1_agg


def Agg_top_trans(path):
    clm={'State':[], 'Year':[],'Quater':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[], 'Entity_name':[]}
    c = 0
    for i in Agg_state_list:
        p_i=path+i+"\\"
        Agg_yr=os.listdir(p_i)
        for j in Agg_yr:
            p_j=p_i+j+"\\"
            Agg_yr_list=os.listdir(p_j)
            for k in Agg_yr_list:
                p_k=p_j+k
                if p_k.endswith('.json'):
                    Data=open(p_k,'r')
                    D=json.load(Data)
                for z in D['data']['districts']:
                    Name=z['entityName']
                    Type=z['metric']['type']
                    count=z['metric']['count']
                    amount=z['metric']['amount']
                    clm['Entity_name'].append(Name)
                    clm['Transacion_type'].append(Type)
                    clm['Transacion_count'].append(count)
                    clm['Transacion_amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
    df5_agg=pd.DataFrame(clm)
    return df5_agg


def Agg_map_trans(path):
    clm = {'State': [], 'Year': [], 'Quater': []}
    c = 0
    for i in Agg_state_list:
        p_i = path + i + "\\"
        Agg_yr = os.listdir(p_i)
        for j in Agg_yr:
            p_j = p_i + j + "\\"
            Agg_yr_list = os.listdir(p_j)
            for k in Agg_yr_list:
                p_k = p_j + k
                if p_k.endswith('.json'):
                    Data = open(p_k, 'r')
                    D = json.load(Data)
                    df_metric = pd.json_normalize(D['data'],record_path =['hoverDataList','metric'])
                    df_name = pd.json_normalize(D['data'],record_path =['hoverDataList'])
                    df_name = df_name.drop(['metric'], axis = 1)
                    df = pd.concat([df_metric, df_name], axis=1)
                    #df = pd.json_normalize(D['data'], "counties", ["state", "shortname", ["info", "governor"]]
                for z in df.index:
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
                if c == 0:
                    df1 = df
                    c = 1
                else:
                    # df1 = df1.append(df)
                    df1 = pd.concat([df1, df], ignore_index=True)


    Agg = pd.DataFrame(clm)
    df3_agg = df1.join(Agg, how='outer')
    # df1_agg = pd.concat([df1,Agg],axis = 1)
    return df3_agg



def ph_user(path):
    clm = {'State': [], 'Year': [], 'Quater': []}
    c = 0
    for i in Agg_state_list:
        p_i = path + i + "\\"
        Agg_yr = os.listdir(p_i)
        for j in Agg_yr:
            p_j = p_i + j + "\\"
            Agg_yr_list = os.listdir(p_j)
            for k in Agg_yr_list:
                p_k = p_j + k
                if p_k.endswith('.json'):
                    Data = open(p_k, 'r')
                    D = json.load(Data)
                df = pd.json_normalize(D['data'], record_path=['usersByDevice'])
                for z in df.index:
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
                if c == 0:
                    df1 = df
                    c = 1
                else:
                    # df1 = df1.append(df)
                    df1 = pd.concat([df1, df], ignore_index=True)

    Agg = pd.DataFrame(clm)
    df2_agg = df1.join(Agg, how='outer')
    # df2_agg = pd.concat([df1,Agg],axis = 1)
    return df2_agg

def ph_map_user(path):
    clm={'State':[], 'Year':[],'Quater':[],'registeredUsers':[], 'district':[], 'appOpens':[]}
    for i in Agg_state_list:
        p_i=path+i+"\\"
        Agg_yr=os.listdir(p_i)
        for j in Agg_yr:
            p_j=p_i+j+"\\"
            Agg_yr_list=os.listdir(p_j)
            for k in Agg_yr_list:
                p_k=p_j+k
                d1=[]
                if p_k.endswith('.json'):
                    Data=open(p_k,'r')
                    D=json.load(Data)
                    d1=[t for t in D['data']['hoverData']]
                for u in d1:
                    Name=D['data']['hoverData'][u]['registeredUsers']
                    Name1=D['data']['hoverData'][u]['appOpens']
                    clm['registeredUsers'].append(Name)
                    clm['appOpens'].append(Name1)
                    clm['district'].append(str(u.replace('hoverData.', '')))
                    #clm['Transacion_type'].append(Type)
                    #clm['Transacion_count'].append(count)
                    #clm['Transacion_amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
    #Succesfully created a dataframe
    Agg_Trans=pd.DataFrame(clm)
    return Agg_Trans



def ph_top_user(path):
    clm = {'State': [], 'Year': [], 'Quater': []}
    c = 0
    for i in Agg_state_list:
        p_i = path + i + "\\"
        Agg_yr = os.listdir(p_i)
        for j in Agg_yr:
            p_j = p_i + j + "\\"
            Agg_yr_list = os.listdir(p_j)
            for k in Agg_yr_list:
                p_k = p_j + k
                if p_k.endswith('.json'):
                    Data = open(p_k, 'r')
                    D = json.load(Data)
                df = pd.json_normalize(D['data'], record_path=['districts'])
                for z in df.index:
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
                if c == 0:
                    df1 = df
                    c = 1
                else:
                    # df1 = df1.append(df)
                    df1 = pd.concat([df1, df], ignore_index=True)

    Agg = pd.DataFrame(clm)
    df6_agg = df1.join(Agg, how='outer')
    # df2_agg = pd.concat([df1,Agg],axis = 1)
    return df6_agg


DB_list = os.listdir(phngitcloneddata)
for d in DB_list:
    p_agg = phngitcloneddata + "\\" + d + "\\"
    table_list = os.listdir(p_agg)
    for e in table_list:
        p_table = p_agg + e + "\\"
        if d == "map":
            path = p_table + "hover\country\india\state\\"
            Agg_state_list=os.listdir(path)
            if e == "transaction":
                df_map_tran=Agg_map_trans(path)
            else:
                df_map_user=ph_map_user(path)
        elif d == "top":
            path = p_table + "country\india\state\\"
            Agg_state_list=os.listdir(path)
            if e == "transaction":
                df_top_trans=Agg_top_trans(path)
            else:
                df_top_user=ph_top_user(path)
        else:
            path = p_table + "country\india\state\\"
            Agg_state_list=os.listdir(path)
            if e == "transaction":
                df_Agg_tran=Agg_trans(path)
            else:
                df_Agg_user=ph_user(path)
Agg_state_list=os.listdir(path)

df_map_tran.rename(columns = {'name':'district'}, inplace = True)
df_top_trans.rename(columns = {'Entity_name':'district'}, inplace = True)
df_top_user.rename(columns = {'name':'district'}, inplace = True)
df_map_tran['district']=df_map_tran['district'].str.replace('district', '')
df_map_user['district']=df_map_tran['district'].str.replace('district', '')

#########BElow part is to upload the data into sql data base.###########

from sqlalchemy import create_engine
engine1 = create_engine("mysql+pymysql://{user}:{pw}@localhost"
                       .format(user="root",
                               pw="root123"))

existing_databases = engine1.execute("SHOW DATABASES;")
# Results are a list of single item tuples, so unpack each tuple
existing_databases = [d[0] for d in existing_databases]
database = "phonepe1"

if database not in existing_databases:
    engine1.execute("CREATE DATABASE {0}".format(database))
    print("Created database {0}".format(database))
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="root123",
                              db = database))
df_Agg_tran.to_sql('aggregated_transaction', con = engine, if_exists = 'replace')
df_Agg_user.to_sql('aggregated_user', con = engine, if_exists = 'replace')
df_map_tran.to_sql('map_transaction', con = engine, if_exists = 'replace')
df_map_user.to_sql('map_user', con = engine, if_exists = 'replace')
df_top_trans.to_sql('top_transaction', con = engine, if_exists = 'replace')
df_top_user.to_sql('top_user', con = engine, if_exists = 'replace')