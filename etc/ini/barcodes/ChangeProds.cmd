
Echo Create table on remoute server
isql -S %1 -U %2 -P %3  -i CreateAid_bar.sql

Echo Send data to remoute server
BCP OTData..aid_bar IN r_Prods.BCP -S %1 -w -C1251 -E -a65535 -U %2 -P  %3

Echo Change data on remoute server
isql -S %1 -U %2 -P %3  -i r_Prods.sql

echo Финиш работы синхронизации для %1 . >> bar.log
date /t >> bar.log
time /t >> bar.log
echo ------------------------------------>> bar.log

Exit