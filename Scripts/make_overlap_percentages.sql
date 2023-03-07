create table test_output as
	SELECT county.*, cd.p_id as parent_id,
       	(ST_Area(ST_Transform(ST_Intersection(county.geometry, cd.geometry), 102003)) /
        	ST_Area(ST_Transform(county.geometry, 102003))) * 100 as overlap_pct
	FROM test_county county
	INNER JOIN test_congress cd
	ON ST_Intersects(ST_Transform(county.geometry, 102003), cd.geometry)
  	AND (ST_Area(ST_Transform(ST_Intersection(county.geometry, cd.geometry), 102003)) /
       	ST_Area(ST_Transform(county.geometry, 102003))) > 0.01;SELECT county.*, cd.p_id as parent_id
  FROM test_county county
  INNER JOIN test_congress cd
  ON ST_Intersects(ST_Transform(county.geometry, 102003), cd.geometry)
    AND (ST_Area(ST_Transform(ST_Intersection(county.geometry, cd.geometry), 102003)) /
        ST_Area(ST_Transform(county.geometry, 102003))) > 0.01;