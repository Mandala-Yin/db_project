-- 学生，教师，教务都可以修改自己的信息，能修改的信息暂定仅为telephone和address
CREATE OR REPLACE PROCEDURE modify_users(
    IN tel character varying,
    IN addr character varying,
    IN id_ character varying)
LANGUAGE 'sql'

BEGIN ATOMIC
 UPDATE "Users" SET telephone = modify_users.tel, address = modify_users.addr
   WHERE (("Users".id)::text = (modify_users.id_)::text);
END;