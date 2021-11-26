    DROP TABLE IF EXISTS food_access_main;
	DROP TABLE IF EXISTS state_county;
	DROP TABLE IF EXISTS food_access_stg;
	DROP TABLE IF EXISTS food_access_ethnicity;
	-- staging table (It is required to run this create statement and upload the file on POSTGRES SQL then run teh remainning script.
	CREATE TABLE food_access_stg ( censustract int
	                             , county VARCHAR(60) 
                                 , state VARCHAR(60)
                                 , urban int
                                 , tractlowi int
                                 , ohu2010 int
								 , pop2010 int
                                 , medianfamilyincome int
								 , povertyrate numeric
                                 , PctWhite numeric
								 , PctBlack numeric
								 , PctAsian numeric
								 , PctHispanic numeric
								 , PctOtherMinority numeric
								 , la1and10 int
								 );
     --  state county look up table
	CREATE TABLE state_county    (statecountyid int
	                            , statecounty VARCHAR(60) NOT NULL
							    , state VARCHAR(60) NOT NULL
							    , county VARCHAR(60) NOT NULL
							    , PRIMARY KEY (statecountyid)
								  );
	INSERT INTO state_county (statecountyid , statecounty ,state ,county)
	SELECT DISTINCT ROW_NUMBER()OVER(ORDER BY StateCounty ASC) AS StateCountyId
         , StateCounty                                         AS StateCounty
	     , state                                               AS State 
	     , county                                              AS county
    FROM
	(
	SELECT DISTINCT state
	   	 , county
	     , concat(replace(state,' ',''),replace(county,' ','')) AS StateCounty
	FROM   food_access_stg	
	) A;
	
    ---update main table with data from staging with statecountyid as foreign key from state_county table	
	
	CREATE TABLE food_access_main ( statecountyid int
	                              , urban int
								  , pop2010 int
								  , ohu2010 int
								  , povertyrate numeric
								  , medianfamilyincome int
								  , tractlowi int
								  , la1and10 int
								  , CONSTRAINT fk_StateCounty1
                                    FOREIGN KEY(statecountyid) 
	                                REFERENCES state_county(statecountyid)
						           );
	INSERT INTO food_access_main (statecountyid, urban, pop2010, ohu2010, povertyrate, medianfamilyincome, tractlowi,la1and10)
	SELECT  sc.statecountyid
	      , Der.urban
	  	  , Der.pop2010
	      , Der.ohu2010
	      , Der.povertyrate
	      , Der.medianfamilyincome
	      , Der.tractlowi
	      , Der.la1and10
  	FROM    (
	SELECT  concat(replace(state,' ',''),replace(county,' ','')) AS StateCounty
   		   , urban
	  	   , pop2010
	       , ohu2010
	       , povertyrate
	       , medianfamilyincome
	       , tractlowi
	       , la1and10
	FROM    food_access_stg
	)Der
	LEFT JOIN state_county sc
           ON Der.StateCounty = sc.StateCounty;
	
	----
	CREATE TABLE food_access_ethnicity ( statecountyid int
	                                   , PctWhite numeric
									   , PctBlack numeric
									   , PctAsian numeric
									   , PctHispanic numeric
									   , PctOtherMinority numeric
								       , CONSTRAINT fk_StateCounty2
                                         FOREIGN KEY(statecountyid) 
	                                     REFERENCES state_county(statecountyid)
						                );
	INSERT INTO food_access_main (statecountyid, PctWhite, PctBlack, PctAsian, PctHispanic, PctOtherMinority)
	SELECT  sc.statecountyid
	      , PctWhite 
	  	  , PctBlack 
	      , PctAsian 
	      , PctHispanic 
	      , PctOtherMinority 
	FROM    (
	SELECT  concat(replace(state,' ',''),replace(county,' ','')) AS StateCounty
   		   , PctWhite 
	  	   , PctBlack 
	       , PctAsian 
	       , PctHispanic 
	       , PctOtherMinority
	FROM    food_access_stg
	)Der
	LEFT JOIN state_county sc
           ON Der.StateCounty = sc.StateCounty;