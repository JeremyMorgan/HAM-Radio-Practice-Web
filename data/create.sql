CREATE TABLE "sessions" (
	"session_id"	INTEGER,
	"questions_correct"	INTEGER,
	"questions_incorrect"	INTEGER,
	PRIMARY KEY("session_id" AUTOINCREMENT)
)

CREATE TABLE "question_sets" (
	"question_set_id"	INTEGER,
	"session_id"	INTEGER,
	"question_id"	INTEGER,
	PRIMARY KEY("question_set_id" AUTOINCREMENT)
)

CREATE TABLE "questions" (
	"id"	TEXT UNIQUE,
	"correct"	INTEGER,
	"question"	TEXT,
	"a"	TEXT,
	"b"	TEXT,
	"c"	TEXT,
	"d"	TEXT,
	PRIMARY KEY("id")
)
