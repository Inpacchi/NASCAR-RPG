select t.id as "Team ID", t.name as "Team Name", tc.series as "Series",
        tc.car_number as "Car Number", tc.status as "Status"
from team_cars tc
    inner join team t
        on tc.team_id = t.id
order by t.name