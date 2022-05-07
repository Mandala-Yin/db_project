CREATE FUNCTION user_insert_check() RETURNS trigger AS $user_insert_check$
    BEGIN
        IF NEW.fname != (SELECT fname FROM "Faculty" WHERE "Faculty".fid=NEW.fid) THEN
            RAISE EXCEPTION 'user faculty id and name do not match';
        END IF;
        RETURN NEW;
    END;
$user_insert_check$ LANGUAGE plpgsql;

CREATE TRIGGER user_insert_check BEFORE INSERT OR UPDATE ON "Users"
    FOR EACH ROW EXECUTE FUNCTION user_insert_check();
