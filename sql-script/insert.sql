insert into "Faculty"(
    select 'f01', 'EECS', 'SC01'
    union
    select 'f02', 'Law', 'L08'
    union
    select 'f03', 'Society', 'S05'
);

insert into "Users"(
    select '180005', 'abc123', 'adm', TRUE, '660782', 'A02-B117', 'f01', 'EECS', 'Alice'
    union 
    select '090005', 'abc123', 'adm', TRUE, '628734', 'A07-C01', 'f01', 'EECS', 'Tom'
    union
    select '170001', 'abc123', 'adm', FALSE, '610307', 'A03-C03', 'f02', 'Law', 'Bob'
    union
    select '130000', 'abc123', 'adm', TRUE, '630203', 'A14-C01', 'f03', 'Society', 'Carol'
    union
    select '080156', '123abc', 'tea', TRUE, '623498', 'A93-D02', 'f01', 'EECS', 'Dave'
    union
    select '030123', '123abc', 'tea', TRUE, '624923', 'A34-E24', 'f01', 'EECS', 'Eve'
    union
    select '130108', '123abc', 'tea', FALSE, '639273', 'C09-B93', 'f02', 'Law', 'France'
    union
    select '190123', '123abc', 'tea', FALSE, '637927', 'D28-C02', 'f02', 'Law', 'Grace'
    union
    select '170134', '123abc', 'tea', TRUE, '642589', 'A09-B12', 'f03', 'Society', 'Hans'
    union
    select '190277', '123', 'stu', TRUE, '627799', '#S01', 'f01', 'EECS', 'Isan'
    union
    select '190231', '123', 'stu', TRUE, '672312', '#S01', 'f01', 'EECS', 'Jason'
    union
    select '190217', '123', 'stu', TRUE, '639919', '#S01', 'f01', 'EECS', 'Kate'
    union
    select '200208', '123', 'stu', FALSE, '678239', '#S01', 'f01', 'EECS', 'Laura'
    union
    select '200214', '123', 'stu', TRUE, '639321', '#S01', 'f01', 'EECS', 'Mandala'
    union
    select '200215', '123', 'stu', FALSE, '630219', '#S01', 'f01', 'EECS', 'Nathan'
    union
    select '180215', '123', 'stu', TRUE, '603919', '#S02', 'f02', 'Law', 'Ola'
    union
    select '180217', '123', 'stu', FALSE, '603519', '#S02', 'f02', 'Law', 'Paul'
    union
    select '180219', '123', 'stu', TRUE, '639039', '#S02', 'f02', 'Law', 'Queue'
    union
    select '200266', '123', 'stu', FALSE, '628919', '#S03', 'f03', 'Society', 'Ria'
    union
    select '210223', '123', 'stu', TRUE, '639569', '#S03', 'f03', 'Society', 'Sara' 
);

insert into "Administrator"(
    select '180005', 3, FALSE
    union
    select '090005', 12, TRUE
    union
    select '170001', 4, FALSE
    union
    select '130000', 8, TRUE
);

insert into "Student"(
    select '190277', 2019, FALSE
    union
    select '190231', 2019, FALSE
    union
    select '190217', 2019, FALSE
    union
    select '200208', 2020, TRUE
    union
    select '200214', 2020, FALSE
    union
    select '200215', 2020, FALSE
    union
    select '180215', 2018, FALSE
    union
    select '180217', 2018, FALSE
    union
    select '180219', 2018, TRUE
    union
    select '200266', 2020, FALSE
    union
    select '210223', 2021, FALSE
);

insert into "Teacher"(
    select '080156', 'Prof', 13
    union
    select '030123', 'Associate Prof', 18
    union
    select '130108', 'Assistant Prof', 8
    union
    select '190123', 'Assistant Prof', 2
    union
    select '170134', 'Associate Prof', 4
);

insert into "Course"(
    select 'c01', '080156', 'ICS', 'Mandatory', 5
    union
    select 'c01', '030123', 'ICS', 'Mandatory', 5
    union
    select 'c02', '030123', 'CVDL', 'Selective', 3
    union
    select 'c03', '190123', 'Criminal Law', 'Mandatory', 4
    union
    select 'c04', '170134', 'Chinese Society', 'Mandatory', 4
    union 
    select 'c05', '130108', 'Civil Law', 'Selective', 3
    union
    select 'c06', '170134', 'American Society', 'Selective', 2
);

insert into "SC"(
    select '190277', 'c01', '080156', 86, TRUE, FALSE, 20190901
    union
    select '190231', 'c01', '080156', 90, TRUE, FALSE, 20190901
    union
    select '190217', 'c01', '080156', NULL, TRUE, TRUE, 20190901
    union
    select '200208', 'c01', '030123', 88, TRUE, FALSE, 20210901
    union
    select '200214', 'c01', '030123', 89, TRUE, TRUE, 202109101
    union
    select '180215', 'c02', '030123', 82, FALSE, FALSE, 20210308
    union
    select '180219', 'c02', '030123', 87, FALSE, FALSE, 20210308
    union
    select '180215', 'c03', '190123', 95, TRUE, FALSE, 20200901
    union
    select '180217', 'c03', '190123', 80, TRUE, FALSE, 20200901
    union
    select '180219', 'c03', '190123', 84, TRUE, FALSE, 20200901
    union
    select '200266', 'c04', '170134', 87, TRUE, FALSE, 20210221
    union
    select '210223', 'c04', '170134', 94, TRUE, FALSE, 20210221
    union
    select '190217', 'c04', '170134', 85, FALSE, FALSE, 20210221
    union
    select '200215', 'c05', '130108', NULL, TRUE, TRUE, 20210308
    union
    select '190217', 'c05', '130108', 91, TRUE, FALSE, 20210308
);