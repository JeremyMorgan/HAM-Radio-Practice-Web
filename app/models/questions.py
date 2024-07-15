import random


class Questions:
    """
    This class is responsible for interacting with the database to fetch and store questions and answers.

    Args:
        cursor (sqlite3.Cursor): A database cursor to execute SQL queries.

    Attributes:
        cursor (sqlite3.Cursor): A database cursor to execute SQL queries.

    Methods:
        get_all_questions(self) -> list:
            Fetches all the questions from the database.

        get_question(self, question_id) -> dict:
            Fetches a specific question from the database based on the provided question_id.

        get_question_set(self, session_id=None) -> list:
            Fetches a set of 35 unique questions for a session. If session_id is provided, it fetches the questions for that specific session.

        get_answered_questions(self, session_id) -> int:
            Fetches the number of questions answered in a session.

        get_next_question(self, session_id) -> str:
            Fetches the next question to be answered in a session.

        store_answer(self, question_id, selected_answer, session_id) -> str:
            Stores the answer to a question and updates the session's score accordingly.

        mark_answer_wrong(self, session_id) -> None:
            Marks an answer as incorrect for a session.

        tally_results(self, session_id) -> dict:
            Fetches the total number of correct and incorrect answers in a session.
    """
    def __init__(self, cursor):
        self.cursor = cursor

    def get_all_questions(self):
        self.cursor.execute("SELECT id FROM questions")
        return self.cursor.fetchall()
    
    def get_question(self, question_id):
        
        self.cursor.execute('''SELECT id, correct, question, a, b, c, d from questions where id = ?''', (question_id,)) 
        result = self.cursor.fetchone()

        if result is None:
            return None

        question_dict = {
            'id': result[0],
            'correct': result[1],
            'question': result[2],
            'a': result[3],
            'b': result[4],
            'c': result[5],
            'd': result[6]
        }

        return question_dict
    
    def get_question_set(self, session_id=None):
        if (session_id is None):
            all_questions = self.get_all_questions()
            if len(all_questions) < 35:
                return "There are not enough questions to generate a set."
            question_set = set()
            while len(question_set) < 35:
                question_id = random.choice(list(all_questions))
                question_set.add(question_id)
            return list(question_set)
        else:
            # Get a list of questionIDs 
            self.cursor.execute("""WITH question_set_info AS (
                    SELECT DISTINCT question_id
                    FROM question_sets
                    WHERE session_id = ?
                    )
                    SELECT
                    questions.id,
                    questions.correct,
                    questions.question,
                    questions.a,
                    questions.b,
                    questions.c,
                    questions.d
                    FROM questions
                    JOIN question_set_info
                    ON questions.id = question_set_info.question_id;"""
                ,(session_id,))
            result = self.cursor.fetchall()
            if result is None:
                return None
            else:
                return list(result)
    
    def get_answered_questions(self, session_id):
        self.cursor.execute("SELECT questions_correct, questions_incorrect FROM sessions WHERE session_id = ?", (session_id,))
        result = self.cursor.fetchone()
        questions_correct, questions_incorrect = result if result else (0, 0)

        # Calculate the total number of questions answered
        questions_answered = questions_correct + questions_incorrect
        return int(questions_answered)
    
    def get_next_question(self, session_id):
        # Execute the first query and fetch all results
        self.cursor.execute("SELECT question_id FROM question_sets WHERE session_id = ?", (session_id,))
        question_ids = [row[0] for row in self.cursor.fetchall()]
        
        print(question_ids[0])
        
        questions_answered = self.get_answered_questions(session_id)

        # if questions answered is less than 35, return the question    
        if questions_answered < 35:
            #print(str(question_id_dict[0]))
            next_question = str(question_ids[questions_answered])
            return next_question
        
        return next_question   
   
    def store_answer(self, question_id, selected_answer, session_id):
        
        self.cursor.execute('SELECT correct from questions where id = ?', (question_id,))
        
        result = self.cursor.fetchone()
        correct_answer = int(result[0])
        
        print ("Correct answer is " + str(result[0]) + " and you selected " + str(selected_answer))
        
        if (correct_answer == int(selected_answer)):
            print("correct")
            self.cursor.execute('UPDATE sessions SET questions_correct = questions_correct + 1 WHERE session_id = ?;', (session_id,))
        else:
            print("naw")
            self.cursor.execute('UPDATE sessions SET questions_incorrect = questions_incorrect + 1 WHERE session_id = ?;', (session_id,))
        return "test"
    
    def mark_answer_wrong(self, session_id):
        self.cursor.execute('UPDATE sessions SET questions_incorrect = questions_incorrect + 1 WHERE session_id = ?;', (session_id,))
                    
    def tally_results(self, session_id):
        self.cursor.execute("SELECT questions_correct, questions_incorrect FROM sessions WHERE session_id = ?", (session_id,))
        result = self.cursor.fetchone()
        questions_correct, questions_incorrect = result if result else (0, 0)
        return {"questions_correct": questions_correct, "questions_incorrect": questions_incorrect}
    