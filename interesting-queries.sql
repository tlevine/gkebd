-- Hur många
create view hur_många_skript as
select kommun, count(*) as 'skript'
from skript
group by kommun;

create view hur_många_kakor as
select kommun, count(*) as 'kakor'
from kaka
group by kommun;

select
  hur_många_skript.kommun,
  hur_många_skript.skript,
  hur_många_kakor.kakor
from hur_många_skript
join hur_många_kakor
on hur_många_skript.kommun = hur_många_kakor.kommun
order by skript, kakor;

-- Datum
select kommun, max(expires)
from kaka
group by kommun
order by max(expires);

-- Varifrån kommer kakor?
select ltrim(replace(domain, 'www.', ''), '.') AS 'domain', count(*)
from kaka group by 1 order by 2;
