C:
CD C:\ChangeBarCode

echo ���� ஡�� ᨭ�஭���樨 �ࠢ�筨��� >> bar.log
date /t >> bar.log
time /t >> bar.log
echo --------------------------------------- >> bar.log
call COPY /Y \\192.168.1.100\SHOPS\ALL\ChangeBarCode\ChangeProds.cmd C:\ChangeBarCode
CALL C:\ChangeBarCode\ChangeProds.cmd EVA7A sa Arhistratig
IF EXIST C:\ChangeBarCode\ChangeProds.cmd DEL /Q /F C:\ChangeBarCode\ChangeProds.cmd
 
