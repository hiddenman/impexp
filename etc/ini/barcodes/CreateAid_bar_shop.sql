USE OTData
if exists (select * from dbo.sysobjects where id = object_id(N'[dbo].[aid_bar]') and OBJECTPROPERTY(id, N'IsUserTable') = 1)
drop table aid_bar
GO

CREATE TABLE aid_bar (
	ProdId int NOT NULL ,
	UM varchar (50) NOT NULL ,
	BarCode varchar(42) NOT NULL ,
	ProdName varchar (200) NULL 
) ON [PRIMARY]
GO

