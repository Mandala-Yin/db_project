CREATE TABLE IF NOT EXISTS "User"
(
    id character varying(10) NOT NULL,
    password character varying(15) NOT NULL,
    role character(3) NOT NULL,
    sex boolean NOT NULL,
    telephone character varying(15) NOT NULL,
    address character varying(20) NOT NULL,
    fid character varying(10) NOT NULL,
    fname character varying(20) NOT NULL,
    name character varying(10) NOT NULL,
    CONSTRAINT users_pk PRIMARY KEY (id),
    CONSTRAINT users_fk FOREIGN KEY (fid)
        REFERENCES "Faculty" (fid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

CREATE TABLE IF NOT EXISTS "Faculty"
(
    fid character varying(10)  NOT NULL,
    fname character varying(20)  NOT NULL,
    location character varying(10) ,
    CONSTRAINT faculty_pk PRIMARY KEY (fid)
);

CREATE TABLE IF NOT EXISTS "Teacher"
(
    id character varying(10) NOT NULL,
    title character varying(20) NOT NULL,
    working_year integer,
    CONSTRAINT teacher_pkey PRIMARY KEY (id),
    CONSTRAINT teacher_fk FOREIGN KEY (id)
        REFERENCES "Users" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

CREATE TABLE IF NOT EXISTS "Student"
(
    id character varying(10) NOT NULL,
    grade integer NOT NULL,
    is_foreign_stu boolean NOT NULL DEFAULT false,
    CONSTRAINT student_pk PRIMARY KEY (id),
    CONSTRAINT student_fk FOREIGN KEY (id)
        REFERENCES "Users" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

CREATE TABLE IF NOT EXISTS "Administrator"
(
    id character varying(10)  NOT NULL,
    working_year integer NOT NULL,
    is_cadre boolean NOT NULL DEFAULT false,
    CONSTRAINT adm_pk PRIMARY KEY (id),
    CONSTRAINT adm_fk FOREIGN KEY (id)
        REFERENCES "Users" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

CREATE TABLE IF NOT EXISTS "Course"
(
    cid character varying(10) NOT NULL,
    tid character varying(10) NOT NULL,
    uni_id character varying(10) NOT NULL,
    cname character varying(20) NOT NULL,
    category character varying(20) NOT NULL,
    credit integer NOT NULL,
    CONSTRAINT "Course_pkey" PRIMARY KEY (cid, tid),
    CONSTRAINT unique_course UNIQUE (uni_id),
    CONSTRAINT course_fk FOREIGN KEY (tid)
        REFERENCES "Teacher" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "SC"
(
    sid character varying(10) NOT NULL,
    cid character varying(10) NOT NULL,
    tid character varying(10) NOT NULL,
    score integer,
    is_major boolean NOT NULL,
    is_w boolean NOT NULL,
    semester integer NOT NULL,
    CONSTRAINT student_course_pk PRIMARY KEY (sid, cid),
    CONSTRAINT sc_fk_1 FOREIGN KEY (sid)
        REFERENCES "Student" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT sc_fk_2 FOREIGN KEY (cid, tid)
        REFERENCES "Course" (cid, tid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);