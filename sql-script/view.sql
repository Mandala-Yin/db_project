CREATE OR REPLACE VIEW admin_information
 AS
 SELECT "Users".id,
    "Users".name,
    "Users".sex,
    "Users".telephone,
    "Users".address,
    "Users".fid,
    "Users".fname,
    "Administrator".working_year,
    "Administrator".is_cadre
   FROM "Users",
    "Administrator"
  WHERE "Users".id::text = "Administrator".id::text;

CREATE OR REPLACE VIEW student_information
 AS
 SELECT "Users".id,
    "Users".name,
    "Users".sex,
    "Users".telephone,
    "Users".address,
    "Users".fid,
    "Users".fname,
    "Student".grade,
    "Student".is_foreign_stu
   FROM "Users",
    "Student"
  WHERE "Users".id::text = "Student".id::text;

CREATE OR REPLACE VIEW teacher_information
 AS
 SELECT "Users".id,
    "Users".name,
    "Users".sex,
    "Users".telephone,
    "Users".address,
    "Users".fid,
    "Users".fname,
    "Teacher".title,
    "Teacher".working_year
   FROM "Users",
    "Teacher"
  WHERE "Users".id::text = "Teacher".id::text;
