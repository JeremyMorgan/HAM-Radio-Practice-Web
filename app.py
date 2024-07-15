from json import dump
import sqlite3
from flask import Flask, make_response, redirect, render_template, request, session, url_for
from app.models.database_connection import DatabaseConnection
from app.models.questions import Questions
from app.models.session import Session

app = Flask(__name__)

print(app)

@app.route('/delete-cookie', methods=['GET'])
@app.before_request
def before_request():
    """
    This function is executed before each request to the '/delete-cookie' endpoint.
    It deletes the cookie and returns a response with the updated index.html template.

    Parameters:
    None.

    Returns:
        flask.Response: The response object with the updated index.html template and deleted cookie.
    """
    if request.endpoint == 'delete-cookie':
        response = make_response(render_template('index.html', data=None, session_id=None))
        response.delete_cookie()
        return response
    
    
@app.route('/quiz/<question_id>/<question_number>', methods=['GET', 'POST'])
def quiz(question_id, question_number):
    """
    This function is responsible for handling the quiz route. It retrieves the current question based on the provided question_id,
    and renders the 'quiz.html' template with the current question and question_number.
    If the request method is 'POST', it stores the selected answer in the database and updates the session with the answered question.
    If the number of answered questions is less than 35, it retrieves the next question and redirects to the same route with the updated question_id and question_number.
    If the number of answered questions is equal to or more than 35, it redirects to the 'results' route.

    :param question_id: The unique identifier of the current question.
    :param question_number: The current question number in the quiz.
    :returns: A Flask response object with the updated 'quiz.html' template and the appropriate redirects.
    """
    our_session = request.cookies.get('session_id') 
    thisquestion = None
    # Set the path to the database    
    db_path = 'data/questions.db'
    # Call the function and store the returned data in a variable
    with DatabaseConnection(db_path) as cursor:         
        if isinstance(cursor, sqlite3.Cursor):
        # The 'cursor' object is a valid database cursor
            questions = Questions(cursor)  # Assuming 'cursor' is your database cursor
            print("question_id: " + question_id)
            thisquestion = questions.get_question(question_id)
        else:
            # The 'cursor' object is not a valid database cursor
            print("Error: 'cursor' object is not a valid database cursor")    
        
    #next_question = questions.get_next_question(our_session)     
        if request.method == 'POST':
            selected_answer = request.form['answer']
            questions.store_answer(question_id, selected_answer,  our_session)            
            questions_answered = questions.get_answered_questions(our_session)
            
            if questions_answered < 35:
                next_question = questions.get_next_question(our_session)
                print("next: " + next_question)
                question_number = int(question_number) + 1
                return redirect(url_for('quiz', question_id=next_question, question_number = str(question_number)))
            else:
                return redirect(url_for('results'))
            
        return render_template('quiz.html', question=thisquestion,question_number=question_number)


@app.route('/', methods=['GET'])
def index():
    """
    This function is responsible for handling the root route of the application.
    It sets up the necessary database connections and session management,
    and then determines whether the user has answered enough questions to see their results.

    Parameters:
    None

    Returns:
    flask.Response: A response object that either renders the 'start.html' template with the next question and session ID,
    or redirects to the 'results' route if the user has answered enough questions.
    """    
    # Set the path to the database    
    db_path = 'data/questions.db'

    # Call the function and store the returned data in a variable
    with DatabaseConnection(db_path) as cursor:        
        session = Session(cursor)
        questions = Questions(cursor)
        our_session_id = request.cookies.get('session_id')         

        if our_session_id is None:
            session.session_id = session.create_session()
        else:
            session.session_id = our_session_id
       
        questions_answered = questions.get_answered_questions(session.session_id)
                
        if questions_answered < 35:
            next_question = questions.get_next_question(session.session_id)
            response = make_response(render_template('start.html', next_question=next_question, session_id=session.session_id))
            #we set the cookie for session ID every time
            response.set_cookie('session_id', str(session.session_id))
            return response
        else: 
            return redirect(url_for('results'))

@app.route('/results', methods=['GET'])
def results():
    """
    This function is responsible for displaying the results of the quiz to the user. It retrieves the user's session ID from the cookies,
    tallies the number of correct and incorrect answers, and then renders the 'results.html' template with the appropriate data.

    Parameters:
        None

    Returns:
        flask.Response: A response object that renders the 'results.html' template with the user's results and deletes the 'session_id' cookie.
    """
    db_path = 'data/questions.db'
    
    with DatabaseConnection(db_path) as cursor:         
        if isinstance(cursor, sqlite3.Cursor):
            questions = Questions(cursor) 
            our_session = request.cookies.get('session_id') 
            results = questions.tally_results(our_session)
            print(our_session)
            print(results)
            correct = results["questions_correct"]
            incorrect = results["questions_incorrect"]
            total_answered = correct + incorrect            
    
    # Create a response object
    response = make_response(render_template('results.html', correct=correct, incorrect=incorrect, total_answered=total_answered))

    # Delete the 'session_id' cookie
    response.delete_cookie('session_id')
    
    return response

if __name__ == "__main__":
    app.run(debug=True)
