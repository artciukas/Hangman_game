
from flask_admin.contrib.sqla import ModelView

from flask_login import current_user, login_manager, login_required
from hangman import admin, db
from hangman.models import Vartotojas


class ManoModelView(ModelView):
    def is_accessible(self):
        print(current_user)
        return current_user.is_authenticated and current_user.el_pastas == "as@tomas.lt"

admin.add_view(ManoModelView(Vartotojas, db.session))



