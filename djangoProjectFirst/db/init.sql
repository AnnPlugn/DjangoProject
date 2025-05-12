CREATE DATABASE pharmdb;

-- Connect to the pharmdb database
\c pharmdb

-- Log database connection
DO $$ BEGIN
    RAISE NOTICE 'Connected to pharmdb';
END; $$;