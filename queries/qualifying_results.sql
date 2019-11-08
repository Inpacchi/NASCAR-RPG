select s.name, d.name, qr.position, qr.range_hits
from qualifying_results qr
inner join schedule s
    on qr.race_id = s.id
inner join driver d
    on qr.driver_id = d.id
order by s.name, qr.position