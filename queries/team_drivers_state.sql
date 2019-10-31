select t.id as "Team ID", t.name as "Team Name", d.name as "Driver Name",
       td.series as "Series"
from team_drivers td
    inner join driver d
        on td.driver_id = d.id
    inner join team t
        on td.team_id = t.id
order by t.id