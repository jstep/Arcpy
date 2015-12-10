CREATE VIEW ed_bs10_view
AS SELECT *
FROM indea:mdwilkie.indea_edvas_active ed
WHERE ed.emp_id = "10";


# Grant privileges
GRANT SELECT 
ON ed_bs10_view 
TO USER dispatch_mgr WITH GRANT OPTION;


-- http://resources.arcgis.com/en/help/main/10.2/index.html#//002m000000rs000000



-- Table
indea:mdwilkie.indea_edvas_active
-- BS Field
ebc_bdy_set_id
-- View name
edvas_active_bs10_v_



-- Arcpy
INPUT_DATABASE = "C:\Users\jastepha\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to indeaprod2.sde"
VIEW_DEFINITION = "SELECT * FROM indea:mdwilkie.indea_edvas_active WHERE ebc_bdy_set_id='10'"
VIEW_NAME = "edvas_active_bs10_v_"
arcpy.CreateDatabaseView_management(INPUT_DATABASE, VIEW_NAME, VIEW_DEFINITION)