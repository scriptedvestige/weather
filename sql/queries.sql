-- Select all columns for a given date
select * from work_forecast where starttime::date = 'DATE';

-- Select all columns and sort by column
select * from home_forecast order by updated asc;

-- Select certain columns for a given date or datetime
select updated, starttime, temp, precip from home_forecast where starttime::date = '2026-01-28' order by starttime, updated asc;
select updated, starttime, temp, precip from home_forecast where starttime = '2026-01-28 15:00:00+00' order by starttime, updated asc

-- Select certain columns during daytime on a given date
select updated, temp, precip, windspeed from work_forecast where starttime::date = 'DATE' and isdaytime = TRUE order by updated asc;

-- Delete all data from table
truncate table [TABLE];

-- Delete table
drop table [TABLE];

-- Table size
select pg_size_pretty(pg_total_relation_size('TABLE'));
SELECT pg_size_pretty( hypertable_size('TABLE'));

-- Verify Timescale behavior
select MIN(starttime), MAX(starttime), COUNT(*) from home_forecast;

-- Check duplicates
select starttime, COUNT(*) from home_forecast group by starttime having count(*) > 1;

-- Create hypertable
select create_hypertable('work_forecast', 'starttime', if_not_exists => TRUE);

-- Show hypertables
select * from timescaledb_information.hypertables;

-- Get mins and maxes for column given date
select MIN(precip), MAX(precip) from home_forecast where starttime::date = '2026-01-29';
select MIN(temp), MAX(temp) from work_forecast where starttime::date = '2026-01-29' and updated::date = '2026-01-28';

-- Most recent forecast scrapes views
create or replace view current_home_forecast as select updated, starttime, temp, precip, windspeed from home_forecast where updated = (select max(updated) from home_forecast) order by starttime;
create or replace view current_work_forecast as select updated, starttime, temp, precip, windspeed from work_forecast where updated = (select max(updated) from work_forecast) order by starttime;

-- Grafana queries
SELECT starttime as time, temp, precip, windspeed FROM current_home_forecast WHERE $__timeFilter(starttime) ORDER BY starttime;
SELECT starttime as time, temp, precip, windspeed FROM current_work_forecast WHERE $__timeFilter(starttime) ORDER BY starttime;

-- Storm Views
create or replace view home_storm_view as 
select 
    starttime, 
    temp, 
    precip, 
    windspeed, 
    humidity,
    case 
        when shortfc ilike '%Snow' then 'snow' 
        when shortfc ilike '%Rain%' then 'rain' 
        else null
    end as storm_type 
from home_forecast 
where updated = (select max(updated) from home_forecast) 
    and (
        shortfc ilike '%Snow%' 
        or shortfc ilike '%Rain'
    );

create or replace view work_storm_view as 
select 
    starttime, 
    temp, 
    precip, 
    windspeed, 
    humidity,
    case 
        when shortfc ilike '%Snow' then 'snow' 
        when shortfc ilike '%Rain%' then 'rain' 
        else null
    end as storm_type 
from work_forecast 
where updated = (select max(updated) from work_forecast) 
    and (
        shortfc ilike '%Snow%' 
        or shortfc ilike '%Rain'
    );

-- Grafana Storm View display
select starttime as "time", temp, precip, windspeed, humidity from home_storm_view order by time;
select starttime as "time", temp, precip, windspeed, humidity from work_storm_view order by time;