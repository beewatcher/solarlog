#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:10:53 2019

@author: mattl
"""

########################################################################################
########################################################################################
def LogFileReduzieren(filename_original, filename_csv):

    import csv
    
    # Liste für Semikolon getrennte Werte definieren
    # Spaeter werden Zeit, TS1, TS2, TS3, UI1, RO1, RO1Safety, VolFlow
    # in diese Liste geschrieben
    LOGtime = []
        
    # Dateiname definieren & Datei zum Lesen oeffnen
    filename = filename_original+".DAT"
    csv_input = open(filename, mode='r', encoding='iso-8859-1')
    
    # Durch Datei gehen und mit modul CSV Daten trennen, erste vier Zeilen werden übersprungen
    with csv_input:
        reader = csv.reader(csv_input, delimiter='\t')
        next(reader)
        next(reader)
        next(reader)
        next(reader)
        header_row = next(reader) # Hier werden Spaltenkoepfe ausgelesen
           
        """
        # Spaltenköpfe indizieren und ausgeben
        for index, column_header in enumerate(header_row):
            print(index, column_header)
        """    
        #ErsteZeile in Liste Speichern 
        LogLine = header_row[0]+";"+header_row[1]+";"+header_row[2]+";"+header_row[3]+";"+header_row[7]+";"+header_row[8]+";"+header_row[12]+";"+header_row[16]
        LOGtime.append(LogLine)
        
        LastSavedMinute = ""

        #Relevante Werte aus jeder Zeile in Liste speichern, wobei immer nur die erste 
        #gefundene Zeile einer hh:mm Kombination verarbeitet wird
        #Das reduziert bei weiterer Bearbeitung die Menge der Datenpunkte.
        for row in reader:
            TimeInRow = row[0]
            if LastSavedMinute != TimeInRow[:5]:
                LogLine = TimeInRow[:5]+";"+row[1]+";"+row[2]+";"+row[3]+";"+row[7]+";"+row[8]+";"+row[12]+";"+row[16]
                LOGtime.append(LogLine)
                LastSavedMinute = TimeInRow[:5]
            
    #Datei schließen
    csv_input.close()

    # Dateiname definieren & Datei zum Schreiben oeffnen
    filename = filename_csv+".csv"
    csv_output = open(filename, mode='w', encoding='iso-8859-1')    
    
    #Liste in Datei schreiben
    with csv_output:    
        for element in LOGtime:
            csv_output.write("%s\n" % element)

    #Datei schließen
    csv_output.close()
########################################################################################
########################################################################################
def CSVFileZeichnen(datestring, filename_csv, filename_chart, filename_thumbnails):

    import csv
    import datetime
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
# Listen für Semikolon getrennte Werte definieren
# Spaeter werden Zeit, TS1, TS2, TS3, UI1, RO1, RO1Safety, VolFlow
# in diese Listen geschrieben
    Zeit = []
    TS1 = []
    TS2 = []
    TS3 = []
    UI1 = []
    RO1 = []
    RO1Safety = []
    VolFlow = []
        
# Dateiname definieren & Datei zum Lesen oeffnen
    filename = filename_csv+".csv"
    csv_input = open(filename, mode='r', encoding='iso-8859-1')
    
# Durch Datei gehen und mit modul CSV Daten trennen, erste Zeile wird uebersprungen
    with csv_input:
        reader = csv.reader(csv_input, delimiter=';')
        header_row = next(reader) # Hier werden Spaltenkoepfe ausgelesen & ignoriert
           
        #Relevante Werte aus jeder Zeile in Liste speichern
        for row in reader:
            Zeit.append(row[0])
            TS1.append(float(row[1]))
            TS2.append(float(row[2]))
            TS3.append(float(row[3]))
            #UI1.append(float(row[4]))
            RO1.append(float(row[5]))
            RO1Safety.append(float(row[6]))
            VolFlow.append(float(row[7])/100)
            
#Datei schließen
    csv_input.close()
    
#Umwandlung der Zeichenketten-Zeiten in Matplotlib Datumsformat
    timestamps=[]
    for element in Zeit:
        timestamp="20"+datestring+" "+(element)
        timestamps.append(datetime.datetime.strptime(timestamp, "%Y%m%d %H:%M"))
    
#Definition der X-Achsengrenzen
    zeitachse_links=datetime.datetime.strptime("20"+datestring+" 00:00", "%Y%m%d %H:%M")
    zeitachse_rechts=datetime.datetime.strptime("20"+datestring+" 23:59", "%Y%m%d %H:%M")
    
#Definition der uebergeordneten Grafik mit zwei Subplots
    fig, ax_lst = plt.subplots(2, 1, dpi=300, gridspec_kw = {'height_ratios':[2.5,1]}, figsize=(10.0,8.0))  # a figure with a 2x1 grid of Axes
    fig.suptitle("                               "+datetime.datetime.strftime(zeitachse_links, "%a,  %d. %b %Y"), fontsize=20, fontweight="bold")  # Add a title so we know which it is
    
#Subplot für Temperaturen
    #Plots und Parameter für Primaerachse
    ax_lst[0].plot(timestamps, TS1, "b-", label='Kollektor [°C]')
    ax_lst[0].plot(timestamps, TS3, "r-", label='Speicher Oben [°C]')
    ax_lst[0].plot(timestamps, TS2, "g-", label='Speicher Unten [°C]')
    ax_lst[0].set_ylim(0, 140)
    ax_lst[0].set_xlim(zeitachse_links, zeitachse_rechts)
    ax_lst[0].set_ylabel('Temperatur', fontsize=12)
    ax_lst[0].legend(fancybox=True, framealpha=1)
    
    #Parameter für Sekundaerachse  
    ax2 = ax_lst[0].twinx()
    ax2.set_ylim(0, 140)
    ax2.set_ylabel('Temperatur', fontsize=12)

    #X-Achse parameterisieren    
    ax_lst[0].xaxis.set_major_formatter(mdates.DateFormatter('%H'))
    ax_lst[0].xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax_lst[0].grid(True)
    
#Subplot für Pumpenparameter
    #Plots und Parameter für Primaerachse
    ax_lst[1].plot(timestamps, RO1, "b-", label='Pumpe [%]')
    ax_lst[1].set_ylim(0, 100)
    ax_lst[1].set_xlim(zeitachse_links, zeitachse_rechts)
    ax_lst[1].set_ylabel('Pumpendrehzahl', fontsize=12)
    ax_lst[1].legend(loc=2, fancybox=True, framealpha=1)
    
    #Plots und Parameter für Sekundaerachse    
    ax3 = ax_lst[1].twinx()
    ax3.plot(timestamps, VolFlow, "g-",label='Durchfluss [l/m]')
    ax3.plot(timestamps, RO1Safety, "r-", label='Fehlerwert')
    ax3.set_ylim(0, 10)
    ax3.set_ylabel('Durchfluss', fontsize=12)
    ax3.legend(loc=1, fancybox=True, framealpha=1)
    
    #X-Achse parameterisieren    
    ax_lst[1].xaxis.set_major_formatter(mdates.DateFormatter('%H'))
    ax_lst[1].xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax_lst[1].grid(True)
    
#Text mit MAX-MIN Wertem    
    # Werte oben sammeln und String zusammenbauen
    fig.text(0.15, 0.94, "Kollektorfühler: MAX="+str(max(TS1))+" °C MIN="+str(min(TS1))+" °C", fontsize=10, verticalalignment='top')
    fig.text(0.15, 0.91, "Speicher-oben: MAX="+str(max(TS3))+" °C MIN="+str(min(TS3))+" °C", fontsize=10, verticalalignment='top')
    fig.text(0.5, 0.91, "Speicher-unten: MAX="+str(max(TS2))+" °C MIN="+str(min(TS2))+" °C", fontsize=10, verticalalignment='top')    
    fig.text(0.15, 0.34, "Pumpe: MAX="+str(max(RO1))+" %", fontsize=10, verticalalignment='top')    
    fig.text(0.5, 0.34, "Durchfluss: MAX="+str(max(VolFlow))+" l/min", fontsize=10, verticalalignment='top')    
    
#Grafik anzeigen
    #plt.show()  
    
#Grafik speichern
    fig.savefig(filename_chart+'.png')
    fig.savefig(filename_thumbnails+'.png', dpi=30)
    
#Arbeitsspeicher aufraeumen
    plt.cla()
    plt.close()


########################################################################################
########################################################################################
# main program starts here

import os
import sys

#Pfadangaben
path_original="LOGFILES_original/"
path_csv="LOGFILES_csv/"
path_chart="LOGFILES_charts/"
path_thumbnails="LOGFILES_charts/thumbnails/"

#Startmeldung
print(sys.argv[0]+" wurde aufgerufen")

#falls kein Parameter übergeben wurde, ist die Anzahl der Elemwnte in der Liste 1
if len(sys.argv) == 1: 
    print("Keinen Parameter übergeben !")
    print("Gültige Parameter:")
    print("     >folder< >> komplettes Verzeichnis wird erneutverarbeitet")
    print("     >jjmmtt< >> einzelne *.DAT Datei mit diesem Namen wird verarbeitet")

#falls Parameter >folder< übergeben wurde    
elif sys.argv[1] == "folder": 
    print('Folder Processing Mode')
    if input("Bereits erstellter Output wird überschrieben! Fortfahren(j/n)? ") == "j":
        #durchnudeln des kompletten Verzeichnis path_original
        verzeichnisinhalt = os.listdir(path_original)
        i=0
        n=0
        #DAT Dateien im Verzeichnis zählen
        for element in sorted(verzeichnisinhalt):
            if element[7:] == "DAT":
                n=n+1    
        #Für DAT Dateien, Prozeduraufrufe starten           
        for element in sorted(verzeichnisinhalt):
            if element[7:] == "DAT":
                datestring = element[:6]
                i=i+1
                print("Die Datei "+path_original+datestring+".DAT wird verarbeitet! ("+str(i)+" von "+str(n)+")")
                #Prozeduraufrufe
                LogFileReduzieren(path_original+datestring, path_csv+datestring)
                CSVFileZeichnen(datestring, path_csv+datestring, path_chart+datestring, path_thumbnails+datestring)
            
#falls irgend ein Parameter übergeben wurde
else: 
    print('Single Processing Mode')
    datestring = sys.argv[1]
    print("Parameterübergabe: "+datestring)
    #Wenn Datei vorhanden, Prozeduraufrufe starten
    if os.path.isfile(path_original+datestring+".DAT"): 
        #if input("Bereits erstellter Output wird überschrieben! Fortfahren(j/n)? ") == "j":
            print("Die Datei "+path_original+datestring+".DAT wird verarbeitet! (1 von 1)")
            #Prozeduraufrufe
            LogFileReduzieren(path_original+datestring, path_csv+datestring)
            CSVFileZeichnen(datestring, path_csv+datestring, path_chart+datestring, path_thumbnails+datestring)    
    #Wenn Datei nicht vorhanden (das fängt auch unnütze Eingaben ab), Fehlermeldung ausgeben
    else: 
        print("Die Datei "+path_original+datestring+".DAT existiert nicht!")


########################################################################################
########################################################################################
# geparkter code

"""    
keiner    
"""
