select s.name, d.name, rr.position, rr.range_hits
from race_results rr
inner join schedule s
    on rr.race_id = s.id
inner join driver d
    on rr.driver_id = d.id
order by s.name, rr.position