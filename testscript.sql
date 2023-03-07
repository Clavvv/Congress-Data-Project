select test_output.overlap_pct, "NAME", "CD116FP" from test_congress
INNER JOIN test_output ON test_output.parent_id=test_congress.p_id
AND test_output."STATEFP" ='06'
ORDER BY "CD116FP";