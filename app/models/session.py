from .database_connection import DatabaseConnection
from .questions import Questions

class Session:
    def __init__(self, cursor: DatabaseConnection) -> None:
        """
        Initialize a new Session object with a given cursor.

        Args:
        cursor (DatabaseConnection): A cursor object that represents a database connection.

        Attributes:
        cursor (DatabaseConnection): The database cursor used for database operations.
        session_id (int): The unique identifier for the current session.
        questions_correct (int): The number of correct answers given by the user.
        questions_incorrect (int): The number of incorrect answers given by the user.
        """
        self.cursor = cursor
        self.session_id = 0
        self.questions_correct = 0
        self.questions_incorrect = 0

    def create_session(self):
        self.cursor.execute("SELECT MAX(session_id) FROM sessions")
        result = self.cursor.fetchone()
        if result[0] is None:
            session_id = 1
        else:
            session_id = result[0] + 1
            self.cursor.execute("INSERT INTO sessions VALUES (?, ?, ?)", (session_id, 0, 0))

        question_set_id = self.get_next_question_set_id()
        self.create_question_set(session_id, question_set_id)
        self.session_id = session_id
            
        return self.session_id

    def get_next_question_set_id(self):
        self.cursor.execute("SELECT question_set_id FROM question_sets ORDER BY question_set_id DESC LIMIT 1")
        result = self.cursor.fetchone()
        if result is None:
            return 1
        else:
            return result[0] + 1

    def create_question_set(self, session_id, question_set_id):
        questions = Questions(self.cursor)
        question_set = questions.get_question_set()
        for question in question_set:
            self.cursor.execute("INSERT INTO question_sets VALUES (null,?,?)", (session_id, question[0]))           

