# solarlog
tl;dr: Raspberry used to connect to thermosolar control station to pull, process and publish logfiles.

The basic motivation for this project was to develop a workaround for manual downloading log files from our solar control station. Earlier it was always necessary to download the files standing beside the wall mounted control station & handling USB cables and laptop somehow without any table or workspace. This manual downloading was followed by showing the log files as nice graphs in a self developed VB application, taking screen dumps to show the graph to our craftsman.
All this took time and didn't lead to continuity.

So, I developed the idea to connect a small computer (Raspberry, Arduino, whatever) to the solar control station and download the files every night.

It didn't take long to understand that this wouldn't work, as the solar control station always stops operation when a USB cable & computer is connected. So the challenge was, to kind of simulate plugging in and out the USB cable in the middle of the night.  Whilst friend of mine proposed to build a little mechanism, that is physically doing this job, I decided to try interrupting the USB cable with a GPIO relay board. 

A nice mock up of Raspberry and relay board proved feasibility of the approach. Shell script was written quickly to pull the log file of $yesterday after closing the connection and mounting the SD-card in the solar control station.

To get rid of the manual work of showing and screendumping the logs in the VB application, I made use of Python & Matplotlib to create a nice and shiny picture of the $yesterdays parameter. Finally everything is publish in my web space and copied to the NAS to get some kind of backup.

Feel free to improve the idea or make use of it.

Regards,
Matthias
