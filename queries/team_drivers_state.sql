select t.name, d.name, td.series from team_drivers td
inner join driver d on td.driver_id = d.id inner join team t on td.team_id = t.id