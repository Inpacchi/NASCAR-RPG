select t1.name as "Equipment Lender", t2.name as "Equipment Lendee", tr.equipment_bonus
from team_rentals tr
    inner join team t1
        on tr.from_id = t1.id
    inner join team t2
        on tr.to_id = t2.id
order by t1.name