# Information Management System


数据库初始化：

```
psql

create database Information_Management_System;
\c information_management_system;

\i sql-script/create.sql
\i sql-script/index.sql
\i sql-script/insert.sql
\i sql-script/stored_procedure.sql
\i sql-script/trigger.sql
\i sql-script/view.sql
```


执行方法：

```
export FLASK_APP=app
flask run
```