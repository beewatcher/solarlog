#!/bin/bash

function check_file {
    [ -f "$1" ]
    return $?
}

gestern=$(date -d 'yesterday' "+%y%m%d")
#gestern="190318"
echo -e "\033[1;32m Parameter: \033[0m"$gestern

echo -e "\033[1;36m Verbindung wird hergestellt\033[0m"
python3 RelaisControl.py connect
sleep 5s # Waits 5 seconds.

echo -e "\033[1;35m Datenträger /dev/sda1 bei /media/pi/solarregler wird eingehangen\033[0m"
sudo mount /dev/sda1 /media/pi/solarregler
sleep 5s # Waits 5 seconds.

echo -e "\033[1;33m Datei von gestern wird kopiert\033[0m"
if check_file /media/pi/solarregler/LOGFILES/$gestern.DAT; then
    echo "Datei "$gestern".DAT ist vorhanden. Download wird gestartet."
	cp -v /media/pi/solarregler/LOGFILES/$gestern.DAT /home/pi/Documents/Logfile-Processing/LOGFILES_original
	cp -v /media/pi/solarregler/LOGFILES/$gestern.LOG /home/pi/Documents/Logfile-Processing/LOGFILES_original
	sleep 10s # Waits 10 seconds.
    echo "Download abgeschlossen."
else
    echo "Datei "$gestern".DAT fehlt. Abbruch und geordneter Rückzug."
fi

echo -e "\033[1;35m Datenträger /dev/sda1 wird ausgehangen\033[0m"
sudo umount /media/pi/solarregler 
sleep 5s # Waits 5 seconds.

echo -e "\033[1;36m Verbindung wird getrennt\033[0m"
python3 RelaisControl.py disconnect

if check_file /home/pi/Documents/Logfile-Processing/LOGFILES_original/$gestern.DAT; then
	echo -e "\033[1;33m Logfile ist vorhanden und wird verarbeitet\033[0m"
	python3 LogFile.py $gestern
    echo "Verarbeitung abgeschlossen."
fi

echo -e "\033[1;32m Script beendet\033[0m"
