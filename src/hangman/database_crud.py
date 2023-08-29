from hangman import db
from hangman.models import Statistics
from flask_login import current_user
from datetime import datetime


def write_defeat_statistics_to_db() -> None:
    db.create_all()                   
    defeat = Statistics(wins=False, defeats=True, data = datetime.now(), user_id=current_user.id)
    db.session.add(defeat)
    db.session.commit()


def write_win_statistics_to_db() -> None:
    db.create_all()          
    win = Statistics(wins=True, defeats=False, data = datetime.now(), user_id=current_user.id)
    db.session.add(win)
    db.session.commit()


def get_all_statistics() -> list:
    db.create_all()
    try:
        all_statistic = Statistics.query.filter_by(user_id=current_user.id).all()
    except:
        all_statistic = []
    return all_statistic


def get_win_statistic() -> int:
    count = 0
    all_statistic = get_all_statistics()
    for win_statistic in all_statistic:
        if win_statistic.wins == 1:
            count += 1
    return count   


def get_defeat_statistic() -> int:
    count = 0
    all_statistic = get_all_statistics()
    for defeat_statistic in all_statistic:
        if defeat_statistic.defeats == 1:
            count += 1
    return count 

    