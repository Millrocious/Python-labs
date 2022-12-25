from flask_admin.contrib.sqla import ModelView

from app import bcrypt


class UserModelView(ModelView):
    form_columns = ('username',
                    'email',
                    'image_file',
                    'about_me',
                    'last_seen',
                    'admin',
                    'password_hashed')

    def on_model_change(self, form, model, is_created):
        # If creating a new user, hash password
        model.password_hashed = bcrypt.generate_password_hash(form.password_hashed.data)
