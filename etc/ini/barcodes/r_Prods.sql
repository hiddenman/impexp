-- BEGIN TRANSACTION TR1
USE OTData

SET NOCOUNT ON


SELECT 'Change BarCode to temp'
----�����-��� ����,� ������ � �� ��� ����---------


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
	-- ������������� ����� ��������� ����� ���

	UPDATE 	r_ProdMQ SET BarCode = 'T' + CONVERT(varchar, ProdID) + Um
	WHERE 	ProdId = @ProdId
	AND			UM = @UM


	FETCH NEXT FROM CUR1 INTO @ProdId, @UM
END

CLOSE CUR1
DEALLOCATE CUR1
-----------------------------------------------------------------
----����� � ��.��� ����, � �����-��� �� ���������---------
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
	-- ������������� ����� ��������� ����� ���

	UPDATE 	r_ProdMQ SET BarCode = 'T' + CONVERT(varchar, ProdID) + Um
	WHERE 	ProdId = @ProdId
	AND			UM = @UM


	FETCH NEXT FROM CUR1 INTO @ProdId, @UM
END

CLOSE CUR1
DEALLOCATE CUR1
-----------------------------------------------------------
SELECT 'Restore real BarCode'
----��������� �������� �����-�����---------

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
	-- ������������� ����� ��������� ����� ���
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



/*************** ���� ����� ����������� *******************/
SELECT 'Change NameProd to temp'
----����� � ��.��� ����, � ��� �� ��������� ---------
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
	-- ������������� ����� ���������� ���

	UPDATE 	r_Prods SET ProdName = CONVERT(varchar, ProdID) + '#T#'
	WHERE 	ProdId = @ProdId

	FETCH NEXT FROM CUR1 INTO @ProdId
END

CLOSE CUR1
DEALLOCATE CUR1
-----------------------------------------------------------
----����� id �� ���������, � ��� ��������� ---------
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
	-- ������������� ����� ���������� ���

	UPDATE 	r_Prods SET ProdName = CONVERT(varchar, ProdID) + '#T#'
	WHERE 	ProdId = @ProdId

	FETCH NEXT FROM CUR1 INTO @ProdId
END

CLOSE CUR1
DEALLOCATE CUR1
-----------------------------------------------------------
SELECT 'Restore real NameProd'
----��������� �������� ������������ ---------

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
	-- ������������� ����� ��������� ����� ���
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


