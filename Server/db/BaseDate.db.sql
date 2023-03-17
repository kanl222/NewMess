BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR,
	"email"	VARCHAR,
	"hashed_password"	VARCHAR,
	"creation_time"	DATETIME,
	"icon"	BLOB,
	PRIMARY KEY("id"),
	UNIQUE("email"),
	UNIQUE("username"),
	UNIQUE("id")
);
CREATE TABLE IF NOT EXISTS "chats" (
	"id"	INTEGER,
	"tittle"	VARCHAR,
	"chat_participant"	VARCHAR,
	"icon"	BLOB,
	PRIMARY KEY("id"),
	UNIQUE("id"),
	UNIQUE("tittle")
);
CREATE TABLE IF NOT EXISTS "messages" (
	"id"	INTEGER,
	"id_user"	INTEGER,
	"id_chat"	INTEGER,
	"message"	VARCHAR,
	"send_time_message"	DATETIME,
	PRIMARY KEY("id"),
	FOREIGN KEY("id_chat") REFERENCES "chats"("id"),
	FOREIGN KEY("id_user") REFERENCES "users"("id"),
	UNIQUE("id")
);
CREATE TABLE IF NOT EXISTS "chat_participants" (
	"id"	INTEGER,
	"id_chat"	INTEGER,
	"id_user"	INTEGER,
	"icon"	BLOB,
	PRIMARY KEY("id"),
	FOREIGN KEY("id_chat") REFERENCES "chats"("id"),
	FOREIGN KEY("id_user") REFERENCES "users"("id"),
	UNIQUE("id")
);
PRAGMA synchronous=OFF;
COMMIT;
