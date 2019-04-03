#!/bin/bash

function check_file {
    [ -f "$1" ]
    return $?
}

#######################################################################
gestern=$(date -d 'yesterday' "+%y%m%d")
#gestern="190318"
echo -e "\033[1;32m Parameter: \033[0m"$gestern

#Test ob Datei zum Upload vorhanden
#Getestet wird nur auf eine, die anderen (tmb, csv, log, dat) sind dann auch da.
if check_file /home/pi/Documents/Logfile-Processing/LOGFILES_charts/$gestern.png; then
    echo "Datei "$gestern".png ist vorhanden. Upload & Sicherung wird gestartet."
else
    echo "Datei "$gestern".png fehlt. Abbruch."
    exit 0
fi

#Upload auf FTP Server zur Veröffentlichung der Daten
echo -e "\033[1;32m Grafik wird auf FTP Server veröffentlicht\033[0m"
ftp -in www.mafoe.de << EOF
user xxxxx xxxxx
binary
hash
cd /html/SUBDOMAINS/solarlog/images/
lcd /home/pi/Documents/Logfile-Processing/LOGFILES_charts
put $gestern.png
cd /html/SUBDOMAINS/solarlog/images/thumbnails
lcd /home/pi/Documents/Logfile-Processing/LOGFILES_charts/thumbnails
put $gestern.png

quit
EOF
sleep 5s # Waits 5 seconds.

#Upload auf NAS (auch via FTP) zur Sicherung der Daten
echo -e "\033[1;32m Grafik und Logfile wird auf Diskstation kopiert\033[0m"
ftp -in 192.168.133.5 << EOF
user xxxxx xxxxx
binary
hash
cd /ftpshare/LOGFILES_charts
lcd /home/pi/Documents/Logfile-Processing/LOGFILES_charts
put $gestern.png
cd /ftpshare/LOGFILES_charts/thumbnails
lcd /home/pi/Documents/Logfile-Processing/LOGFILES_charts/thumbnails
put $gestern.png
cd /ftpshare/LOGFILES_csv
lcd /home/pi/Documents/Logfile-Processing/LOGFILES_csv
put $gestern.csv
cd /ftpshare/LOGFILES_original
lcd /home/pi/Documents/Logfile-Processing/LOGFILES_original
put $gestern.LOG
put $gestern.DAT

quit
EOF

echo -e "Script beendet"
