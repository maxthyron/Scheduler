select *
from schedule_scheduletime
where id not in (select time_id
                 from schedule_schedulesubject
                          join schedule_auditorium sa on schedule_schedulesubject.auditorium_id = sa.id
                 where day = 0
                   and auditorium_id = '218л');

select *
from schedule_scheduletime
         join schedule_schedulesubject ss on schedule_scheduletime.id = ss.time_id
where ss.day = 0
  and auditorium_id = '218л';

delete from schedule_schedulesubject;
delete from schedule_scheduletime;
delete from schedule_auditorium;