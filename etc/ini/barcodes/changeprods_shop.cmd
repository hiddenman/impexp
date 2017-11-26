IF EXIST r_Prods.zip DEL /Q /F r_Prods.zip

COPY /Y \\192.168.1.100\SHOPS\ALL\ChangeBarCode\r_Prods.Zip 

IF NOT EXIST PKZIPW.EXE COPY /Y \\192.168.1.100\SHOPS\ALL\ChangeBarCode\PKZIPW.EXE 

IF EXIST r_Prods.bcp DEL /Q /F r_Prods.bcp

PKZIPW.EXE -extract r_Prods.zip

Echo Create table on remoute server
isql -S %1 -U %2 -P %3  -i \\192.168.1.100\SHOPS\ALL\ChangeBarCode\CreateAid_bar.sql

Echo Send data to remoute server
BCP OTData..aid_bar IN r_Prods.BCP -S %1 -w -C1251 -E -a65535 -U %2 -P  %3

Echo Change data on remoute server
isql -S %1 -U %2 -P %3  -i \\192.168.1.100\SHOPS\ALL\ChangeBarCode\r_Prods.sql

IF EXIST r_Prods.zip DEL /Q /F r_Prods.zip

IF NOT EXIST PKZIPW.EXE COPY /Y \\192.168.1.100\SHOPS\ALL\ChangeBarCode\PKZIPW.EXE 

IF EXIST r_Prods.bcp DEL /Q /F r_Prods.bcp

echo Финиш работы синхронизации для %1 . >> bar.log
date /t >> bar.log
time /t >> bar.log
echo ------------------------------------>> bar.log

