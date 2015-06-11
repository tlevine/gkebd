create view if not exists varifrån_kommer_kakorna as
select ltrim(replace(domain, 'www.', ''), '.') as 'domain', count(*)
from kaka group by 1 order by 2;

create view if not exists hur_många_skript as
select kommun, count(*) as 'skript'
from skript
group by kommun;

create view if not exists hur_många_kakor as
select kommun, count(*) as 'kakor'
from kaka
group by kommun;

create view if not exists hur_många_skript_och_kakor as
select
  hur_många_skript.kommun,
  hur_många_skript.skript,
  hur_många_kakor.kakor
from hur_många_skript
join hur_många_kakor
on hur_många_skript.kommun = hur_många_kakor.kommun
order by skript, kakor;

create view if not exists lång_kakor as
select kommun, max(expires)
from kaka
group by kommun
order by max(expires);
