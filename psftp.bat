@ECHO OFF
:: This batch file transfers the webserver files to the raspi
TITLE PSFTP Transfer Webserver
ECHO Please wait... Transfering files.
psftp.exe raspi-bett -bc -be -b "E:/Raspberry/21 Projekte/light/psftpTransfer"
PAUSE