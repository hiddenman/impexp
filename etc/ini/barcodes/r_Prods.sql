-- BEGIN TRANSACTION TR1
USE OTData

SET NOCOUNT ON


SELECT 'Change BarCode to temp'
----Штрих-код есть,а товара с ед изм нету---------


DECLARE CUR1 CURSOR
READ_ONLY
FOR 
	SELECT 	b.ProdId, b.UM 
	FROM	aid_bar a, r_ProdMQ b
	WHERE 	a.Barcode = b.Barcode 
	AND	(a.um<>b.um OR a.ProdId<>b.ProdId)


DECLARE @ProdId 		int
DECLARE @UM 				varchar(50)
DECLARE @BarCode 		varchar(42)
DECLARE @ProdName 	varchar(200)

SELECT @ProdId = 0
SELECT @UM = ''
SELECT @BarCode = ''
SELECT @ProdName = ''

OPEN CUR1

FETCH NEXT FROM CUR1 INTO @ProdId, @UM
WHILE (@@fetch_status <> -1)
BEGIN
	-- Устанавливаем новый временный штрих код

	UPDATE 	r_ProdMQ SET BarCode = 'T' + CONVERT(varchar, ProdID) + Um
	WHERE 	ProdId = @ProdId
	AND			UM = @UM


	FETCH NEXT FROM CUR1 INTO @ProdId, @UM
END

CLOSE CUR1
DEALLOCATE CUR1
-----------------------------------------------------------------
----Товар с ед.изм есть, а штрих-код не совпадает---------
DECLARE CUR1 CURSOR
READ_ONLY
FOR 
	SELECT 	b.ProdId, b.UM 
	FROM	aid_bar a, r_ProdMQ b
	WHERE a.Barcode <> b.Barcode 
	AND		a.um = b.um 
	AND 	a.ProdId = b.ProdId

SELECT @ProdId = 0
SELECT @UM = ''
SELECT @BarCode = ''
SELECT @ProdName = ''

OPEN CUR1

FETCH NEXT FROM CUR1 INTO @ProdId, @UM
WHILE (@@fetch_status <> -1)
BEGIN
	-- Устанавливаем новый временный штрих код

	UPDATE 	r_ProdMQ SET BarCode = 'T' + CONVERT(varchar, ProdID) + Um
	WHERE 	ProdId = @ProdId
	AND			UM = @UM


	FETCH NEXT FROM CUR1 INTO @ProdId, @UM
END

CLOSE CUR1
DEALLOCATE CUR1
-----------------------------------------------------------
SELECT 'Restore real BarCode'
----Установка реальных штрих-кодов---------

DECLARE CUR1 CURSOR
READ_ONLY
FOR 
SELECT a.ProdId,a.UM 
FROM	r_ProdMQ a,aid_bar b
WHERE a.ProdId=b.ProdId 
AND a.um=b.um 
AND a.BarCode = 'T' + CONVERT(varchar, a.ProdID) + a.Um

SELECT @ProdId = 0
SELECT @UM = ''
SELECT @BarCode = ''
SELECT @ProdName = ''

OPEN CUR1

FETCH NEXT FROM CUR1 INTO @ProdId, @UM
WHILE (@@fetch_status <> -1)
BEGIN
	-- Устанавливаем новый временный штрих код
	SELECT @BarCode = BarCode FROM aid_bar 
	WHERE 	ProdId = @ProdId
	AND			UM = @UM

	UPDATE 	r_ProdMQ SET BarCode = @BarCode
	WHERE 	ProdId = @ProdId
	AND			UM = @UM


	FETCH NEXT FROM CUR1 INTO @ProdId, @UM
END

CLOSE CUR1
DEALLOCATE CUR1



/*************** Если Имена различаются *******************/
SELECT 'Change NameProd to temp'
----Товар с ед.изм есть, а имя не совпадает ---------
DECLARE CUR1 CURSOR
READ_ONLY
FOR 
	SELECT DISTINCT	b.ProdId
	FROM	aid_bar a, r_Prods b
	WHERE a.ProdId = b.ProdId
  AND		a.ProdName <> b.ProdName

SELECT @ProdId = 0
SELECT @UM = ''
SELECT @BarCode = ''
SELECT @ProdName = ''

OPEN CUR1

FETCH NEXT FROM CUR1 INTO @ProdId
WHILE (@@fetch_status <> -1)
BEGIN
	-- Устанавливаем новое времеенное имя

	UPDATE 	r_Prods SET ProdName = CONVERT(varchar, ProdID) + '#T#'
	WHERE 	ProdId = @ProdId

	FETCH NEXT FROM CUR1 INTO @ProdId
END

CLOSE CUR1
DEALLOCATE CUR1
-----------------------------------------------------------
----Товар id не совпадает, а имя совпадает ---------
DECLARE CUR1 CURSOR
READ_ONLY
FOR 
	SELECT DISTINCT	b.ProdId
	FROM	aid_bar a, r_Prods b
	WHERE a.ProdId <> b.ProdId
  AND		a.ProdName = b.ProdName

SELECT @ProdId = 0
SELECT @UM = ''
SELECT @BarCode = ''
SELECT @ProdName = ''

OPEN CUR1

FETCH NEXT FROM CUR1 INTO @ProdId
WHILE (@@fetch_status <> -1)
BEGIN
	-- Устанавливаем новое времеенное имя

	UPDATE 	r_Prods SET ProdName = CONVERT(varchar, ProdID) + '#T#'
	WHERE 	ProdId = @ProdId

	FETCH NEXT FROM CUR1 INTO @ProdId
END

CLOSE CUR1
DEALLOCATE CUR1
-----------------------------------------------------------
SELECT 'Restore real NameProd'
----Установка реальных наименований ---------

DECLARE CUR1 CURSOR
READ_ONLY
FOR 
SELECT DISTINCT a.ProdId
FROM	r_Prods a,aid_bar b
WHERE a.ProdId=b.ProdId 
AND SUBSTRING(a.ProdName, LEN(a.ProdName) - 2, 3) = '#T#'

SELECT @ProdId = 0
SELECT @UM = ''
SELECT @BarCode = ''
SELECT @ProdName = ''

OPEN CUR1

FETCH NEXT FROM CUR1 INTO @ProdId
WHILE (@@fetch_status <> -1)
BEGIN
	-- Устанавливаем новый временный штрих код
	SELECT DISTINCT @ProdName = ProdName FROM aid_bar 
	WHERE 	ProdId = @ProdId

	UPDATE 	r_Prods SET ProdName = @ProdName
	WHERE 	ProdId = @ProdId

	FETCH NEXT FROM CUR1 INTO @ProdId
END

CLOSE CUR1
DEALLOCATE CUR1

-- COMMIT TRANSACTION TR1

SET NOCOUNT OFF
GO


