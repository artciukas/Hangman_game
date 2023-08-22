import os
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, logout_user, login_user, login_required
from datetime import datetime


from hangman import app, db, bcrypt
from hangman.forms import RegistracijosForma, PrisijungimoForma, PaskyrosAtnaujinimoForma, IrasasForm
from hangman.models import Vartotojas, Irasas
from hangman.photo_save import save_picture

from hangman.utilities import get_random_word,word_database,display_word,display_all_letters






@app.route("/registruotis", methods=['GET', 'POST'])
def registruotis():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistracijosForma()
    if form.validate_on_submit():
        koduotas_slaptazodis = bcrypt.generate_password_hash(form.slaptazodis.data).decode('utf-8')
        vartotojas = Vartotojas(vardas=form.vardas.data, el_pastas=form.el_pastas.data, slaptazodis=koduotas_slaptazodis)
        db.session.add(vartotojas)
        db.session.commit()
        flash('You have successfully registered! You can login.', 'success')
        return redirect(url_for('index'))
    
    return render_template('registruotis.html', title='Register', form=form)


@app.route("/prisijungti", methods=['GET', 'POST'])
def prisijungti():
    if current_user.is_authenticated:
        return redirect(url_for('start'))
    form = PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if user and bcrypt.check_password_hash(user.slaptazodis, form.slaptazodis.data):
            login_user(user, remember=form.prisiminti.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('start'))
        else:
            flash('Login failed. Check email email and password.', 'danger')
    return render_template('prisijungti.html', title='Prisijungti', form=form)


@app.route("/atsijungti")
def atsijungti():
    logout_user()
    return redirect(url_for('index'))


@app.route("/")
def index():
    if current_user.is_authenticated:
        flash('You already registered!', 'success')
        return redirect(url_for('start'))
    flash('You are not registered!', 'danger')
    return render_template("welcome.html")

@app.route("/start")
def start():
    start_game()
    return render_template("start.html")




@app.route("/paskyra", methods=['GET', 'POST'])
@login_required
def paskyra():
    form = PaskyrosAtnaujinimoForma()
    
    if form.validate_on_submit():
        if form.nuotrauka.data:
            nuotrauka = save_picture(form.nuotrauka.data)
            current_user.nuotrauka = nuotrauka
        current_user.vardas = form.vardas.data
        current_user.el_pastas = form.el_pastas.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('paskyra'))
    elif request.method == 'GET':
        form.vardas.data = current_user.vardas
        form.el_pastas.data = current_user.el_pastas
    nuotrauka = url_for('static', filename='profilio_nuotraukos/' + current_user.nuotrauka)
    return render_template('paskyra.html', title='Account', form=form, nuotrauka=nuotrauka)


# @app.route("/naujas_irasas", methods=["GET", "POST"])
# @login_required
# def new_record():
#     db.create_all()
#     forma = hangman.forms.IrasasForm()
#     if forma.validate_on_submit():
#         naujas_irasas = Irasas(pajamos=forma.pajamos.data, suma=forma.suma.data, vartotojas_id=current_user.id)
#         db.session.add(naujas_irasas)
#         db.session.commit()
#         flash(f"Įrašas sukurtas", 'success')
#         return redirect(url_for('records'))
#     return render_template("prideti_irasa.html", form=forma)

@app.route("/irasai")
@login_required
def records():
    db.create_all()
    try:
        visi_irasai = Irasas.query.filter_by(vartotojas_id=current_user.id).all()
    except:
        visi_irasai = []
    print(visi_irasai)
    return render_template("irasai.html", visi_irasai=visi_irasai, datetime=datetime)


def start_game():
    random_word = get_random_word(word_database)
    session['guessed_letters'] = []
    session['random_word'] = random_word
    session['unused_letters_list'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    session['not_correct_answers'] = []


@app.route('/game', methods=['GET', 'POST'])
@login_required
def my_function():
    
    guessed_letters = session['guessed_letters']
    random_word = session['random_word']
    unused_letters_list = session['unused_letters_list']
    not_correct_answers = session['not_correct_answers']
    hiden_word = display_word(random_word, guessed_letters)
    lives = 7 - len(not_correct_answers)
    
    img = os.path.join('static', 'img')
    print(list(session))


    # GET LOGIC
    if request.method == 'GET':
        if 'random_word' not in session:
            start_game()
            print(f'aaa{random_word}')
        

        file = os.path.join(img, f'{lives}.jpg')
        print(f"Answer: {random_word}")
        print(f"picture image: {file}")
        answer ='Please choice a letter'
        display_unused_letters_list = display_all_letters(unused_letters_list)
        return render_template('game.html', data = file, answer = answer, random_word = random_word, hiden_word = hiden_word, display_unused_letters_list = display_unused_letters_list)
    
    # POST LOGIC
    else: 
        #GET INPUT FROM FRONT END
        user_guess = request.form.get('name').upper()
        file = os.path.join(img, f'{lives}.jpg')
        print(file)


    # CHECK LIVES
        if len(not_correct_answers) < 6:
            print(f'lives left: {len(not_correct_answers)}')
            print(f'wrong answers: {not_correct_answers}')
            print(file)


    # IF USER NOT REPEAT LETTER
            if user_guess in guessed_letters:
                answer ='Letter was already used!!!'
                display_unused_letters_list = display_all_letters(unused_letters_list)
                return render_template('game.html', data = file, random_word = random_word, hiden_word = hiden_word, answer = answer , display_unused_letters_list = display_unused_letters_list)
            
            
    # ELIF APPEND APPROVE LETTER
            elif user_guess.isalpha() and len(user_guess) == 1:
                guessed_letters.append(user_guess)
                session['guessed_letters'] = guessed_letters
                
                hiden_word = display_word(random_word, guessed_letters)
                print(f'Guessed letters are: {guessed_letters}')
                print(f'Question are: {hiden_word}')
                
    # IF ALL LETTERS GESSED WIN
                if "_" not in hiden_word:
                    file = os.path.join(img, 'heaven.jpg')
                    answer = f"Congratulations! You guessed the word: {random_word}"


                    db.create_all()
                    
                    win = Irasas(laimejo=True, pralaimejo=False, vartotojas_id=current_user.id)
                    db.session.add(win)
                    db.session.commit()
                    flash(f"Statistics updated", 'success')



                    return render_template('win.html', data = file, answer = answer)
                
    # IF USER GUESS RIGHT LETTER
                elif user_guess in random_word:
                    answer = f'Correct. Letter {user_guess} is in the word'
                    unused_letters_list.remove(user_guess)
                    session['unused_letters_list'] = unused_letters_list
                    display_unused_letters_list = display_all_letters(unused_letters_list)
                    return render_template('game.html', data = file, random_word = random_word, hiden_word = hiden_word, answer = answer, display_unused_letters_list = display_unused_letters_list)
                
    # IF USER GUESS WRONG LETTER
                else: 
                    answer = f'Letter {user_guess} does not exist in the word'
                    unused_letters_list.remove(user_guess)
                    session['unused_letters_list'] = unused_letters_list
                    display_unused_letters_list = display_all_letters(unused_letters_list)
                    not_correct_answers.append(user_guess)
                    session['not_correct_answers'] = not_correct_answers
                    lives = 7 - len(not_correct_answers)
                    file = os.path.join(img, f'{lives}.jpg')
                    print(f"picture image: {file}")
                    print(f"No correct letters list: {not_correct_answers}")
                    print(lives)
                    
                    
                    return render_template('game.html', data = file, random_word = random_word, hiden_word = hiden_word, answer = answer, display_unused_letters_list = display_unused_letters_list)
    
    # IF USER INPUT NOT SINGLE LETTER
            else:
                answer ='Please enter single letter!'
                display_unused_letters_list = display_all_letters(unused_letters_list)
                return render_template('game.html', data = file, random_word = random_word, hiden_word = hiden_word, answer = answer, display_unused_letters_list = display_unused_letters_list)
        else:
            file = os.path.join(img, 'hell.jpg')
            db.create_all()
                        
            win = Irasas(laimejo=False, pralaimejo=True, vartotojas_id=current_user.id)
            db.session.add(win)
            db.session.commit()
            flash(f"Statistics updated", 'success')
            return render_template('lost.html', data = file, answer = "Game Over. Try again.")
    

@app.route('/restart')
def restart():
    start_game()
    return redirect(url_for('my_function'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
