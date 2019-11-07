select s.id, s.name, t.name, s.date, s.type, s.laps, s.stages, s.race_processed
from schedule s
inner join track t
    on s.track_id = t.id
order by s.date