from seaborn.matrix import _HeatMapper
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import io
import base64
import streamlit.components.v1 as components


st.set_page_config(page_title="Dashboard", page_icon="https://www.camping-croisee-chemins.fr/wp-content/uploads/2021/02/Recyclage.png",layout="wide")

st.title("Datasets dashboards by PONNOU Wilfried")
dataset1='C:/Users/PONNOU Wilfried/OneDrive - Efrei/M1/data viz/Labs/uber-raw-data-apr14.csv'
dataset2='C:/Users/PONNOU Wilfried/OneDrive - Efrei/M1/data viz/Labs/ny-trips-data.csv'

##################COMPOSANT BIDIRECTIONNEL RADIOBUTTON#######################################################################################
_radio_button = components.declare_component(
    "radio_button", url="http://localhost:3001",
)



def custom_radio_button(label, options, default, key=None):
    return _radio_button(label=label, options=options, default=default, key=key)

with st.sidebar:
    datasetchoice = custom_radio_button(
    "Which dataset?",
    options=["dataset Uber","dataset NY"],
    default="dataset NY"
    )
    st.write("This dataset has been choosed: %s" % datasetchoice)
################################################################################################################################################
#############################Le COMPOSANT STATIC SE TROUVE A LA LIGNE 327##################################################""

##############decorateur##################################
def timer(func):
    def wrapper(*args,**kwargs):
        
        with open("logs1.txt","a") as f:
            before=time.time()
            func(*args,**kwargs)
            f.write("Function "+ func.__name__ +" took: "+str(time.time()-before)+"seconds in lab3 \n")
    return wrapper
############################################################""

#########################################fonctions#####################################################################
##########################uncomment @timer if you want the logs of the functions###########################################################
def get_dom(dt): 
    return dt.day 

def get_weekday(dt): 
    return dt.weekday() 

def get_hour(dt): 
    return dt.hour
def tf(dfcolumn,getwhat):
    data=dfcolumn.map(getwhat)
    return data
def readcsv(dataset):
    return pd.read_csv(dataset)

def datetimetf(dfcolumn):
    datetimecolumn=pd.to_datetime(dfcolumn)
    return datetimecolumn
#@timer
#@st.cache(suppress_st_warning=True)
def occurences(df,groupbyfactor):
    data=df.groupby(groupbyfactor).size().unstack()
    return data
#@timer
@st.cache(suppress_st_warning=True)
def mapper(dflat,dflon):
    gpspoints={'latitude':dflat,'longitude':dflon}
    map_data = pd.DataFrame(data=gpspoints)
    st.map(map_data)
#@timer
@st.cache(suppress_st_warning=True)
def histplotter(column,bine,rwidth,rang,title,xlabel,ylabel):
    fig,ax= plt.subplots()
    n,bine,patches=ax.hist(column,bins=bine, rwidth=rwidth,range=rang)
    for i in range(len(patches)):
        patches[i].set_facecolor(plt.cm.viridis(n[i]/max(n)))
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)
#@timer
#@st.cache(suppress_st_warning=True)
def occurencecounter(param,groupbyfactor, text):
    st.write(occurences(df,groupbyfactor)[int(param)], text)
#@timer
#@st.cache(suppress_st_warning=True)
def sorter(df,param):
    return df.sort_values(param)
#@timer
#@st.cache(suppress_st_warning=True)
def mapparam(sliderparam,dflon,dflat,coordparam,start,stop,begin):
    param_to_filter = st.slider(sliderparam, start, stop, begin)
    d={'lon':dflon[coordparam.dt.hour == param_to_filter],'lat':dflat[coordparam.dt.hour == param_to_filter]}
    filtered_data = pd.DataFrame(data=d)
    st.subheader(f'Map of all orders at {param_to_filter}')
    st.map(filtered_data)
#@timer
@st.cache(suppress_st_warning=True)
def heatmapplotter(df,params,title):
    df_grouped_by_params=occurences(df,params)
    fig,ax=plt.subplots()
    ax=sns.heatmap(df_grouped_by_params)
    ax.set_title(title)
    st.pyplot(fig)
#@timer
@st.cache(suppress_st_warning=True)
def linear(kms,xparam,yparam):
    m, b = np.polyfit(xparam, yparam, 1)
    return m*kms+b
#@timer
@st.cache(suppress_st_warning=True)
def twoplots(xparam,yparam,xlabel,ylabel,title) : 
    x=xparam
    y=yparam
    m, b = np.polyfit(x, y, 1)
    fig, ax = plt.subplots()
    ax.plot(x,y, "r*")
    ax.plot(x, m*x + b)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    st.pyplot(fig)
    plt.plot(x,y, "r*")
    return m,b
#@timer
@st.cache(suppress_st_warning=True)
def barchartplotter(dfcolumn,bine,rang):
    hist_values = np.histogram(dfcolumn.dt.hour, bins=bine, range=rang)[0]
    st.bar_chart(hist_values)

#@timer
@st.cache(suppress_st_warning=True)
def plotter(x,y,xlabel,ylabel,title):
    fig, ax = plt.subplots()
    ax.plot(x,y,"ro")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    st.pyplot(fig)
#@timer
#@st.cache(suppress_st_warning=True)
def headprinter(df):
    st.write(df.head())
########################################################################################################################""""






#######################################app streamlit~########################################################################""
if datasetchoice=='dataset Uber':
    st.header("This dataset represent Uber orders during The month of April 2014")
    #preprocessing###############################################
    df=readcsv(dataset1)
    df['Date/Time']=datetimetf(df['Date/Time'])
    df['dom']=tf(df['Date/Time'],get_dom)
    df['weekday']=tf(df['Date/Time'],get_weekday)
    df['Hour'] = tf(df['Date/Time'],get_hour)
    ##########################################################""
    if st.checkbox('Voir les données'):
        st.text('Voici le dataset en question:')
        st.write(headprinter(df))
    
    
    if st.checkbox('Voir la carte des commandes Uber'):
        gpspoints={'latitude':df['Lat'],'longitude':df['Lon']}
        map_data = pd.DataFrame(data=gpspoints)
        st.map(map_data)
    
    option = st.selectbox('Which figure do you want to see? There will be interactive tools in some of them !',
    ["Frequency by DoM","Order by hours","Orders by weekday"])
    st.write('You selected: ', option,",scroll down to see the entire possibilities!")

    if option=='Frequency by DoM':
        
        if st.checkbox("Voir l'histogramme"):
            histplotter(df['dom'],30,0.8,(0.5,30.5),"Frequency by DoM","Date of the month","Frequency")

        if st.checkbox("Choisir le jour du mois"):
            dom=st.selectbox('Which day of month?',['1','2','3','4','5','6','7','8','9','10','11','12'
            ,'13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30'])
            occurencecounter(dom,'dom','orders this day')
        
        
    
    elif option=='Order by hours':
        if st.checkbox("Voir l'histogramme"):
            df_hour_sorted=sorter(df,'Hour')
            histplotter(df['Hour'],24,0.8,(0.5,23),"Orders by hours","Hours","Orders")
  
        elif st.checkbox("Voir l'emplacement des commandes uber par heure"):
            mapparam('hour',df['Lon'],df['Lat'],df['Date/Time'],0,23,17)

        
    elif option=='Orders by weekday':
        if st.checkbox("Voir l'histogramme"):
            
            df_hour_sorted=sorter(df,'Hour')
            df_weekday_sorted=sorter(df,'weekday')
            histplotter(df_weekday_sorted['weekday'],7,0.8,(-.5,6.5),'Orders by weekday','Days of the week','Orders')

        
        elif st.checkbox('Voir la carte des commandes par jour de la semaine'):
            mapparam('Day',df['Lon'],df['Lat'],df['Date/Time'],1,7,1)

        
        elif st.checkbox("Voir la heatmap"):
            heatmapplotter(df,['weekday','Hour'],'Heatmap of Orders during hours of each weekday')



if datasetchoice == 'dataset NY':
    
    #Preprocessing OF DATASET2
    #df= pd.read_csv(dataset2)
    df=readcsv(dataset2)
    df['tpep_pickup_datetime']=datetimetf(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime']=datetimetf(df['tpep_dropoff_datetime'])
    df['trip_duration']=(df['tpep_dropoff_datetime']-df['tpep_pickup_datetime']).dt.round('10min')
    df['trip_duration'] = df['trip_duration'].astype(str).map(lambda x: x[10:])
    df['pickup_Hour'] = tf(df['tpep_pickup_datetime'],get_hour)
    df['dropoff_Hour'] = tf(df['tpep_dropoff_datetime'],get_hour)
    df['roundedtripdistance']=df['trip_distance'].round()
    df['Hour'] = tf(df['tpep_pickup_datetime'],get_hour)
   

    ##########################################################
    st.header("This dataset represent New York city's trips data during one day")
    if st.checkbox('Voir les données'):
        st.text('Voici le dataset en question:')
        st.write(headprinter(df))

    
    if st.checkbox("Voir les cartes"):
    
        startendchoice=st.selectbox('Quelle carte voulez-vous voir?',['Voir les points de prise en charge','Voir les points de dépot'])
        
        if startendchoice=='Voir les points de dépot':
            mapper(df['dropoff_latitude'],df['dropoff_longitude'])


        elif startendchoice=='Voir les points de prise en charge':
            mapper(df['pickup_latitude'],df['pickup_longitude'])

    
    option = st.selectbox('Which figure do you want to see? There will be interactive tools in some of them !',
    ["fare amount according to trip distance","tip amount according to trip distance","Trips duration"
    ,"Trips dropoff according to hour","Trips per vendor"
    ,"Trips pickup according to hour","duration according to trip distance","trips distance according to pickup hour"
    ,"Passengers per trips"])
    st.write('You selected: ', option, ",scroll down to see the entire possibilities")

    if option=="fare amount according to trip distance":
        twoplots(df['trip_distance'],df['fare_amount'],'Trip distance','Fare amount',"Fare amount according to trip distance")


        if st.checkbox("Do you want to know your trip's fare based on this dataset?"):
            kms=st.slider(label="Select your trip's distance",min_value=1, max_value=200)
            st.write('For '+ str(kms) +' kms your fare will be of '+ str(linear(kms,df['trip_distance'],df['fare_amount']))+' $ !This is just an estimation!')


    elif option=="tip amount according to trip distance":
        twoplots(df['trip_distance'],df['tip_amount'],'Trip distance','tip amount',"Tip amount according to trip distance")


        if st.checkbox("Do you want to know how much you should tip for your trip based on this dataset?"):
            kms=st.slider(label="Select your trip's distance", max_value=40)
            st.write('For '+ str(kms) +' kms you should tip '+ str(linear(kms,df['trip_distance'],df['tip_amount']))+' $ !This is just an estimation!')
    
    elif option=="Trips duration":
        histplotter(df['trip_duration'],None,0.8,None,"Trip duration and its frequency","Trip duration",'Total trips')

    elif option=="Trips dropoff according to hour":
        
        if st.checkbox('Voir le bar chart'):
            barchartplotter(df['tpep_dropoff_datetime'],24,(0,24))

        elif st.checkbox('Voir les données par heure sur une carte'):
            mapparam('hour',df['dropoff_longitude'],df['dropoff_latitude'],df['tpep_dropoff_datetime'],0,23,17)


        
    elif option=="Trips pickup according to hour":
        if st.checkbox('Voir le bar chart'):
            barchartplotter(df['tpep_pickup_datetime'],24,(0,24))

        elif st.checkbox('Voir les données par heure sur une carte'):
            mapparam('hour',df['pickup_longitude'],df['pickup_latitude'],df['tpep_pickup_datetime'],0, 23, 17)


    elif option=="Passengers per trips":
        histplotter(df['passenger_count'],None,0.8,None,"Passenger per trip","Number of passenger",'Total trips')

    elif option=="Trips per vendor":
        if st.checkbox("Do you want to see a Histogram"):
            histplotter(df['VendorID'],None,0.8,None,"Trips per Vendor","Vendor","Trips")
 
        elif st.checkbox("Do you want to select a vendor"):
            
            vendorchoice=st.selectbox('Which vendor?',['1','2'])
            occurencecounter(vendorchoice,'VendorID',' trips')

    
    elif option=="duration according to trip distance":
        
        if st.checkbox("Do you want to see a plot"):
            twoplots(df['trip_distance'],(df['trip_duration'].str.slice(stop=2)).astype(int),"Trips distance","duration","Duration according to trip distance")

        elif st.checkbox("Do you want to see a heatmap"):
            heatmapplotter(df,['roundedtripdistance','trip_duration'],"Trip duration according to distance")

        if st.checkbox("Do you want to know how much time your trip will take, based on this dataset?"):
            kms=st.slider(label="Select your trip's distance",min_value=1, max_value=150)
            st.write('For '+ str(kms) +' kms the trip should be about '+ str(linear(kms,df['trip_distance'],(df['trip_duration'].str.slice(stop=2)).astype(int)))+' min')

    elif option=="trips distance according to pickup hour":
#######################"COMPOSANT STATIC"#################################################################################################################
        components.html("""<html lang="fr">

                            <head>
                                <title>Chep</title>
                                <meta charset="utf-8">
                            </head>
                            
                            <body>
                            
                                
                                <img src="https://zupimages.net/up/21/38/dkzg.png">
                                <img src="https://zupimages.net/up/21/38/m08g.png">
                            

                            
                            
                            </body>
                            
                        </html>""",height=500,scrolling=True)
