alter table member_info
add column nominate_dim1 double precision,
add column nominate_dim2 double precision,
add column nominate_number_of_votes double precision,
add column nominate_number_of_errors double precision,
add column nokken_poole_dim1 double precision,
add column nokken_poole_dim2 double precision,
add column congress bigint;

update member_info
set 
	nominate_dim1= member_ideology.nominate_dim1,
	nominate_dim2= member_ideology.nominate_dim2,
	nominate_number_of_votes= member_ideology.nominate_number_of_votes,
	nominate_number_of_errors= member_ideology.nominate_number_of_errors,
	nokken_poole_dim1= member_ideology.nokken_poole_dim1,
	nokken_poole_dim2= member_ideology.nokken_poole_dim2,
	congress= member_ideology.congress
from member_ideology
where member_info.icpsr_id = member_ideology.icpsr::text;
