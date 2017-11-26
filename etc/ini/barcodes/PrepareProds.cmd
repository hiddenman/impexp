isql -S STAR  -U sa -P Arhistratig  -Q "DELETE OTData..aid_bar"
isql -S STAR  -U sa -P Arhistratig  -Q "INSERT INTO OTData..aid_bar SELECT  a.ProdID, a.UM, a.BarCode, b.ProdName FROM OTData..r_ProdMQ a INNER JOIN  OTData..r_Prods b ON a.ProdID = b.ProdID"
BCP OTData..aid_bar OUT r_Prods.BCP -S STAR -w -C1251 -E -a65535 -U sa -P Arhistratig
CALL PKZIPW.EXE -add r_Prods.zip r_Prods.BCP
COPY /Y r_Prods.zip \\SUN\SHOPS\ALL\ChangeBarCode
