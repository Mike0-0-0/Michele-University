# -*- coding: utf-8 -*-
"""
Created on Sun May 24 15:12:02 2026

@author: miche
"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

#VARIABILE DI CONTROLLO
#stagione='inverno'
#stagione='primavera'
stagione='estate'
#stagione='autunno'

if stagione=='inverno':
    ora_inizio , ora_fine =12,15
    soglia_ore=3 
    ore_totali=4
    mesi=[11,12,1,2] #Nov, dic, gen , feb
elif stagione=='estate':
    ora_inizio , ora_fine=11, 17 
    soglia_ore=5 
    ore_totali=7
    mesi=[7,8]
elif stagione=='autunno':
    ora_inizio, ora_fine=12, 16
    soglia_ore= 4 
    ore_totali=5
    mesi=[9,10]
else:
    ora_inizio, ora_fine=12, 16
    soglia_ore= 4 
    ore_totali=5
    mesi=[3,4]


# IMPORTO I DATI 
df=pd.read_csv(r'C:\Users\miche\Desktop\progetto LABORATORIO\stationsData5min\ML-30.csv')
df1=pd.read_csv(r'C:\Users\miche\Desktop\progetto LABORATORIO\CLEARSKY_CET_5min.csv')

# CONVERTO IN DATATIME
df['Time_CET'] = pd.to_datetime(df['Time_CET'], format="%d/%m/%Y %H:%M")
df1['Time_CET']=pd.to_datetime(df1['Time_CET'], format="%d/%m/%Y %H:%M") # converto subito anche il dataframe ClearSky

#DEFINISCO LA PORZIONE SU BASE STAGIONALE DEL DATAFRAME
condizione_stagionale=( (df['Time_CET'].dt.hour >= ora_inizio) &
                      (df['Time_CET'].dt.hour<=ora_fine) &
                      (df['Time_CET'].dt.month.isin(mesi))
                      )
df_stagionale=df[condizione_stagionale].copy() 
df_stagionale['date']=df_stagionale['Time_CET'].dt.date
df_stagionale['hour']=df_stagionale['Time_CET'].dt.hour
num_giorni_stagionali=df_stagionale['date'].nunique() #conta i giorni distinti stagione per stagione



#IMPONGO LE CONDIZIONI SULLA VELOCITà DEL VENTO
vel = df_stagionale.groupby(['date', 'hour'])['WSpeed'].mean().unstack() #con .unstack() trasformo una series multi-indice in un DataFrame
condizione_wspeed=(vel>1) & (vel<6) #sostanzialmente un nuovo DataFrame in cui le informazioni sulla velocità sono ridotte a True/False, in base ad una condizione arbitraria
count_speed=condizione_wspeed.sum(axis=1) #con axis=1 sommo per righe, con axis=0 sommo per colonne


#IMPONGO CONDIZIONI SULLA DIREZIONE DEL VENTO
#questo blocco di codice serve a fare la media degli angoli
rad=np.deg2rad(df_stagionale['WDir'])
u=np.cos(rad)
v=np.sin(rad)
df_stagionale['u']=u
df_stagionale['v']=v
def funct(df):
    u_mean = df.groupby(['date','hour'])['u'].mean()
    v_mean = df.groupby(['date','hour'])['v'].mean()

    mean_dir = np.rad2deg(np.arctan2(v_mean, u_mean))
    mean_dir = (mean_dir + 360) % 360

    return mean_dir
#fine 

direction_matrix=funct(df_stagionale).unstack() #DataFrame delle medie corrette in degree
condizione_wdir =(direction_matrix>220) & (direction_matrix<270) #condizione sulla direzione
dir_score=condizione_wdir.sum(axis=1) #sommo i valori : se rispettano condizione (True) +1, altrimenti (False) +0


#IMPONGO LE CONDIZIONI SULLA RADIAZIONE
#teniamo conto del fatto che non tutte le stazioni hanno misure di radiazione
piranometro= df_stagionale['Rad'].notna().sum() >0
if piranometro:
    df_merge=pd.merge( df_stagionale, #in questo nuovo DataFrame c'è anche la radiazione solare di clearsky, perchè pd.merge unisce due DataFrame in base a una o più colonne in comune
                      df1,
                      on='Time_CET',
                      how='inner')
    df_merge['ratio']=df_merge['Rad']/df_merge['clearskyRad'] #aggiungo una colonna al dataframe df_merge, ovvero il rapporto I=rad_sper/rad_teo
    df_merge=df_merge.dropna(subset=['Rad','clearskyRad']) #elimino solo le righe dove mancano Rad oppure clearskyRad
    mean_rad=df_merge.groupby(['date','hour'])['ratio'].mean().unstack() 
    rad_cond=(mean_rad>=0.75)
    rad_count=rad_cond.sum(axis=1)
else:
    rad_count=None



#IMPONGO LA NO-RAIN CONDITION

rain_=df_stagionale.groupby(['date','hour'])['Rain'].mean().unstack()
condizione_rain=(rain_==0) 
rain_count=condizione_rain.sum(axis=1)

#DATAFRAME FINALE

    
dati_breeze={
    'Wspeed': count_speed,
    'Wdirection': dir_score,
    'rain': rain_count,
    }
if piranometro:
    dati_breeze['Rad']=rad_count

df_breeze=pd.DataFrame(dati_breeze).dropna()

if piranometro:
    df_breeze['breeze']=((df_breeze['Wspeed']>= soglia_ore) & #aggiungo questa nuova colonna di True/False in base al rispetto di TUTTI i proxy
                         (df_breeze['Wdirection']>= soglia_ore) &
                         (df_breeze['rain']>=ore_totali) & #non deve piovere mai, quindi per la pioggia la condizione è diversa
                         (df_breeze['Rad']>=soglia_ore)
                         )
else: 
    df_breeze['breeze']=((df_breeze['Wspeed']>= soglia_ore) & #aggiungo questa nuova colonna di True/False in base al rispetto di TUTTI i proxy
                         (df_breeze['Wdirection']>= soglia_ore) &
                         (df_breeze['rain']>=ore_totali)
                         )

breeze_days=df_breeze['breeze']

#QUANTI E QUALI SONO I GIORNI DI BREZZA?
conto=breeze_days.sum()
giorni_br=breeze_days[breeze_days]
perc=conto/num_giorni_stagionali

print(f"--- REPORT {stagione.upper()} (Stazione analizzata: LA-01) ---")
print(f"Sensore Radiazione Solare: {'ATTIVO' if piranometro else 'NON DISPONIBILE (Proxy Escluso)'}")
print(f'I giorni di brezza sono: {conto} su {num_giorni_stagionali} giorni stagionali totali.')
print(f"La percentuale di giorni di brezza su base stagionale nell'arco (2020-2025) è: {perc:.1%}")
print(f'La percentuale di giorni di brezza arrotondata è: {perc:.0%}')
print("\nElenco delle date in cui si è verificata la brezza:")
print(giorni_br.index)

#--------------------------------------------------------------
#--------------------------------------------------------------

#CREIAMO IL DIZIONARIO CON NOMI, PERCORSI E DISTANZE DAL MARE

path_stazioni=r'C:\Users\miche\Desktop\progetto LABORATORIO\stationsData5min'

path_distanze=r'C:\Users\miche\Desktop\progetto LABORATORIO\distanze_km.txt'

stazioni={}
with open(path_distanze,'r') as file: 
    for linea in file:
        frammenti=linea.split(',') #diciamo a Python di separare il nome dalla distanza se c'è la virgola in mezzo
        
        nome=frammenti[0].strip()  #strip serve solo a rimuovere eventuali spazi
        distanza=float(frammenti[1].strip())
        
        stazioni[nome]= {
            'path':fr'{path_stazioni}\{nome}.csv',
            'distanza': distanza
            }
     
#creo una lista pulita di date in cui c'è stata la brezza
date_brezza=giorni_br.index  # I GIORNI DI BREZZA SONO SEMPRE RELATIVI ALLA VARIABILE DI CONTROLLO, QUINDI L'ANALISI è STAGIONALE !

#lista in cui salvo i DataFrame delle medie orarie di ogni stazione
lista_medie_stazioni=[]

for nome_stazione,info in stazioni.items(): # ciclo for per ogni stazione
    df_staz=pd.read_csv(info['path']) #leggo il data_path della prima stazione
    df_staz['Time_CET']=pd.to_datetime(df_staz['Time_CET'], format="%d/%m/%Y %H:%M") #converto la colonna in datetime data
    df_staz['date']=df_staz['Time_CET'].dt.date 
    df_staz['hour']=df_staz['Time_CET'].dt.hour
    
    # ora filtriamo il dataframe tenendo TUTTE e 24 le ore ma SOLO dei giorni di brezza
    df_filtrato=df_staz[df_staz['date'].isin(date_brezza)].copy() #un dataframe identico a quello originale ma che contiene solo i giorni di brezza
    
    if not df_filtrato.empty:
        #calcoliamo le 24 medie orarie su tutti i giorni di brezza
        medie_24h=df_filtrato.groupby('hour')['T'].mean().reset_index() # indicizziamo di nuovo
        #creo le nuove colonne 'stazione' e 'distanza'
        medie_24h['stazione']=nome_stazione
        medie_24h['distanza_mare']=info['distanza']
        #salviamo nella lista precedentemente creata i valori di medie_24h
        lista_medie_stazioni.append(medie_24h)
df_macro=pd.concat(lista_medie_stazioni, ignore_index=True) # mettiamo insieme in un unico grande DataFrame i valori della lista costruita (nella lista ogni valore è separato dal successivo)

# CALCOLIAMO I GRADIENTI
from scipy.stats import linregress
gradienti_totali=[] #creo una lista da riempire coi valori dei gradienti orari 
for h in range (24): #per tutte e 24 le ore
    dati_ora=df_macro[df_macro['hour']==h].dropna(subset=['distanza_mare','T'])   # creiamo un nuovo dataset che ha tutti i dati di temperatura all'ora h e distanza delle stazioni 
    if len(dati_ora)>2 : #controllo di avere abbastanza stazioni
        slope, intercept, r_value, p_value, std_err= linregress(dati_ora['distanza_mare'], dati_ora['T'])
        
        r_quadro = r_value**2 # il coefficiente di determinazione indica in che percentuale la temperatura è influenzata dalla distanza dal mare (mi aspetto che sia considerevolmente vicino ad uno solo nelle ore di brezza)
        gradienti_totali.append({
            'hour':h,
            'gradiente':slope,
            'r_sq':r_quadro})
        #stampiamo a schermo ??
        
df_risultati_gradienti=pd.DataFrame(gradienti_totali) 
# Ho fatto una cosa simile a prime: ho preso i valori nella lista gradienti_totali e li ho inseriti nel grande DataFrame appena creato


#GRAFICO DI T(KM) PER UN'ORA TARGET (le temperature ad una data distanza sono quelle mediate lungo tutti i giorni di brezza della stagione di controllo)
ora_target=14 #ora target come parametro di controllo
df_ora=df_macro[df_macro['hour']==ora_target].dropna(subset=['distanza_mare','T'])

if len(df_ora)>1:  #mi assicuro che ci siano sufficienti dati per una retta

    slope, intercept, r_value, p_value, std_err= linregress(df_ora['distanza_mare'],df_ora['T'])
    r_quadro=r_value**2 
    
    plt.figure(figsize=(9,6))
    plt.scatter(df_ora['distanza_mare'],df_ora['T'], label='stazioni meteo')
    for i, riga in df_ora.iterrows():
        plt.annotate(riga['stazione'], (riga['distanza_mare'], riga['T']), 
                     textcoords="offset points", xytext=(5,5), ha='left', fontsize=9, fontweight='bold')
    #disegniamo ora la retta di regressione
    x_linea=np.linspace(df_ora['distanza_mare'].min() - 2, df_ora['distanza_mare'].max() + 2, 100)
    y_linea=slope*x_linea + intercept 
    plt.plot(x_linea, y_linea, color='r', 
         label=f'Retta di tendenza (Gradiente: {slope:.3f} °C/km) | {stagione.upper()} - Ore {ora_target}:00')
    plt.xlabel('Distanza dal mare (km)')
    
    plt.ylabel('Temperatura Media(°C)')
    plt.legend(loc='upper left') #dove posizionare la legenda
    plt.show()
else:
    print('dati insufficienti per questo grafico')
print(r_quadro)

#GRAFICO DI CONFRONTO 24 ORE TRA DUE STAZIONI TARGET

# GRAFICO DI CONFRONTO 24 ORE TRA DUE STAZIONI TARGET (TEMPERATURA E VENTO)

stazione_vicina = 'ML-01'  
stazione_lontana = 'ML-13'

df_vicina = df_macro[df_macro['stazione'] == stazione_vicina] # prendo il df_macro della stazione vicina scelta
df_lontana = df_macro[df_macro['stazione'] == stazione_lontana] # prendo il df_macro della stazione lontana scelta

dist_vicina = df_vicina['distanza_mare'].iloc[0] if not df_vicina.empty else 0 # se il df_vicina non è vuoto, salva la distanza; altrimenti 0
dist_lontana = df_lontana['distanza_mare'].iloc[0] if not df_lontana.empty else 0 # se il df_lontana non è vuoto, salva la distanza; altrimenti 0

if not df_vicina.empty and not df_lontana.empty:
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # --- ASSE Y PRIMARIO (TEMPERATURA) - LINEE CONTINUE ---
    # Plot Temperatura Stazione Vicina
    line1, = ax1.plot(df_vicina['hour'], df_vicina['T'], color='deepskyblue', marker='o', 
                      linewidth=2, label=f'Temp {stazione_vicina} ({dist_vicina} km)')
    
    # Plot Temperatura Stazione Lontana
    line2, = ax1.plot(df_lontana['hour'], df_lontana['T'], color='darkorange', marker='s', 
                      linewidth=2.5, label=f'Temp {stazione_lontana} ({dist_lontana} km)')

    ax1.set_xlabel("Ora del giorno", fontsize=11)
    ax1.set_ylabel("Temperatura Media (°C)", fontsize=11, color='black')
    ax1.set_xticks(range(0, 24))
    ax1.grid(True, linestyle=':', alpha=0.5)

    # --- ASSE Y SECONDARIO (VELOCITÀ DEL VENTO) - LINEE TRATTEGGIATE ---
    ax2 = ax1.twinx()  # Crea l'asse gemello a destra

    # Plot Vento Stazione Vicina (utilizzando Wspeed)
    line3, = ax2.plot(df_vicina['hour'], df_vicina['WSpeed'], color='deepskyblue', linestyle='--', 
                      linewidth=1.8, alpha=0.8, label=f'Vento {stazione_vicina}')
    
    # Plot Vento Stazione Lontana (utilizzando Wspeed)
    line4, = ax2.plot(df_lontana['hour'], df_lontana['WSpeed'], color='darkorange', linestyle='--', 
                      linewidth=1.8, alpha=0.8, label=f'Vento {stazione_lontana}')

    ax2.set_ylabel("Velocità Media Vento (m/s)", fontsize=11, color='black')

    # --- UNIONE DELLE LEGENDE ---
    lines = [line1, line2, line3, line4]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=9, framealpha=0.9)

    plt.title(f"Confronto Termico-Dinamico Giornaliero ({stagione.upper()})\nMedie orarie sui giorni di brezza", fontsize=12)
    plt.tight_layout()
    plt.show()

else:
    print("Errore: uno dei DataFrame è vuoto.")







