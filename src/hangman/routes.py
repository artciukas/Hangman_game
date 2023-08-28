import os
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, logout_user, login_user, login_required
from datetime import datetime


from hangman import app, db, bcrypt, logging
from hangman.forms import RegisterForm, LoginForm, AccountUpdateForm
from hangman.models import User, Statistics
from hangman.photo_save import save_picture
from hangman.database_crud import write_defeat_statistics_to_db, write_win_statistics_to_db, get_all_statistics, get_win_statistic, get_defeat_statistic

from hangman.utilities import get_random_word,word_database,display_word,display_all_letters


@app.route("/register", methods=['GET', 'POST'])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You can login.', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('start'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            start_game()
            return redirect(next_page) if next_page else redirect(url_for('start'))
        else:
            flash('Login failed. Check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/disconnect")
def disconnect():
    logout_user()
    return redirect(url_for('index'))


@app.route("/")
def index():
    if current_user.is_authenticated:
        flash('You already registered!', 'success')
        return render_template("start.html")
    flash('You are not registered!', 'danger')
    return render_template("welcome.html")


@app.route("/start")
def start():
    start_game()
    # if session['game_status'] == False:
    #     redirect(url_for('restart'))
    
    return redirect(url_for('restart'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.photo.data:
            photo = save_picture(form.photo.data)
            current_user.photo = photo
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    photo = url_for('static', filename='profile_pictures/' + current_user.photo)
    return render_template('account.html', title='Account', form=form, photo=photo)


@app.route("/statistic")
@login_required
def records():
    all_statistic = get_all_statistics()
    user_wins = get_win_statistic()
    user_defeat = get_defeat_statistic()
    return render_template("statistic.html", all_statistic=all_statistic, datetime=datetime, user_wins=user_wins, user_defeat=user_defeat, current_user=current_user)


def start_game():
    random_word = get_random_word(word_database)
    session['guessed_letters'] = []
    session['random_word'] = random_word
    session['unused_letters_list'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    session['not_correct_answers'] = []
    session['game_status'] = True
    logging.info('reseting game data')
    return redirect(url_for('game_route'))


@app.route('/game', methods=['GET', 'POST'])
@login_required
def game_route():
    
    guessed_letters = session['guessed_letters']
    random_word = session['random_word']
    unused_letters_list = session['unused_letters_list']
    not_correct_answers = session['not_correct_answers']
    hiden_word = display_word(random_word, guessed_letters)
    lives = 7 - len(not_correct_answers)
    img = os.path.join('static', 'img')


    # GET LOGIC
    if request.method == 'GET':
        logging.info(session['game_status'])
        if session['game_status'] == False:
            redirect(url_for('game_route'))
            start_game()
        
        game_status = True
        session['game_status'] = game_status
        redirect(url_for('restart'))
        file = os.path.join(img, f'{lives}.jpg')
        logging.info(f"Answer: {random_word}")
        answer ='Please choice a letter'
        display_unused_letters_list = display_all_letters(unused_letters_list)
        return render_template('game.html', data = file, answer = answer, random_word = random_word, hiden_word = hiden_word, display_unused_letters_list = display_unused_letters_list)
    
    # POST LOGIC
    else: 
        #GET INPUT FROM FRONT END
        user_guess = request.form.get('name').upper()
        file = os.path.join(img, f'{lives}.jpg')
        logging.info(session['game_status'])
        logging.info(f"Answer: {random_word}")


    # CHECK LIVES
        if len(not_correct_answers) < 6:
        

    # IF USER NOT REPEAT LETTER
            if user_guess in guessed_letters:
                answer ='Letter was already used!!!'
                logging.info(f"Letter {user_guess} was already used!!!")
                display_unused_letters_list = display_all_letters(unused_letters_list)
                return render_template('game.html', data = file, random_word = random_word, hiden_word = hiden_word, answer = answer , display_unused_letters_list = display_unused_letters_list)
            
            
    # ELIF APPEND APPROVE LETTER
            elif user_guess.isalpha() and len(user_guess) == 1:
                guessed_letters.append(user_guess)
                session['guessed_letters'] = guessed_letters
                hiden_word = display_word(random_word, guessed_letters)
                logging.info(f'Guessed letters are: {guessed_letters}')
                logging.info(f'Question are: {hiden_word}')
        
                
    # IF ALL LETTERS GESSED WIN
                if "_" not in hiden_word:
                    file = os.path.join(img, 'heaven.jpg')
                    logging.info(f"Congratulations! You guessed the word: {random_word}")
                    answer = f"Congratulations! You guessed the word: {random_word}"
                    write_win_statistics_to_db()
                    flash(f"Statistics updated", 'success')
                    game_status = False
                    session['game_status'] = game_status
                    redirect(url_for('game_route'))
                    start_game()
                    return render_template('win.html', data = file, answer = answer)
                

    # IF USER GUESS RIGHT LETTER
                elif user_guess in random_word:
                    answer = f'Correct. Letter {user_guess} is in the word'
                    logging.info(f'Correct. Letter {user_guess} is in the word')
                    unused_letters_list.remove(user_guess)
                    session['unused_letters_list'] = unused_letters_list
                    display_unused_letters_list = display_all_letters(unused_letters_list)
                    return render_template('game.html', data = file, random_word = random_word, hiden_word = hiden_word, answer = answer, display_unused_letters_list = display_unused_letters_list)
                

    # IF USER GUESS WRONG LETTER
                else: 
                    answer = f'Letter {user_guess} does not exist in the word'
                    logging.info(f'Letter {user_guess} does not exist in the word')
                    unused_letters_list.remove(user_guess)
                    session['unused_letters_list'] = unused_letters_list
                    display_unused_letters_list = display_all_letters(unused_letters_list)
                    not_correct_answers.append(user_guess)
                    session['not_correct_answers'] = not_correct_answers
                    lives = 7 - len(not_correct_answers)
                    file = os.path.join(img, f'{lives}.jpg')
                    logging.info(f"Incorrect letters list: {not_correct_answers}")
                    redirect(url_for('game_route'))
                    return render_template('game.html', data = file, random_word = random_word, hiden_word = hiden_word, answer = answer, display_unused_letters_list = display_unused_letters_list)
    

    # IF USER INPUT NOT SINGLE LETTER
            else:
                answer ='Please enter single letter!'
                logging.info('Please enter single letter!')
                display_unused_letters_list = display_all_letters(unused_letters_list)
                return render_template('game.html', data = file, random_word = random_word, hiden_word = hiden_word, answer = answer, display_unused_letters_list = display_unused_letters_list)
        else:
            file = os.path.join(img, '0.jpg')
            logging.info("Game Over. Try again.")
            write_defeat_statistics_to_db()
            game_status = False
            session['game_status'] = game_status
            redirect(url_for('game_route'))
            start_game()
            logging.info(session['game_status'])
            flash(f"Statistics updated", 'success')
            return render_template('defeat.html', data = file, answer = "Game Over. Try again.", random_word = random_word)
    

@app.route('/restart')
def restart():
    start_game()
    flash(f"Statistics updated", 'success')
    return redirect(url_for('game_route'))

@app.route('/give_up')
def give_up():
    start_game()
    write_defeat_statistics_to_db()
    flash(f"You gave up. Statistics updated", 'success')
    return redirect(url_for('game_route'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
