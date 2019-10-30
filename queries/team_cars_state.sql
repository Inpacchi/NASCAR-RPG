select t.name, tc.series, tc.car_number, tc.status from team_cars tc
inner join team t on tc.team_id = t.id