SELECT county.*, cd.primary_key
FROM test_county county, test_cd cd
WHERE ST_Intersects(ST_Transform(county.geometry, 102003), cd.geometry)
  AND (ST_Area(ST_Transform(ST_Intersection(county.geometry, cd.geometry), 102003)) /
       ST_Area(ST_Transform(county.geometry, 102003))) > 0.01;