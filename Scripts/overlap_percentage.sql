create table test_output as
	SELECT county.*, cd.p_id as parent_id,
       	(ST_Area(ST_Intersection(county.geometry, cd.geometry)) /
        	ST_Area(county.geometry)) * 100 as overlap_pct
	FROM test_county county
	INNER JOIN test_congress cd
	ON ST_Intersects(county.geometry, cd.geometry)
  	AND (ST_Area(ST_Intersection(county.geometry, cd.geometry))/
       	ST_Area(county.geometry)) > 0.01;