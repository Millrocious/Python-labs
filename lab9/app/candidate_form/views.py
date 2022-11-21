from flask import render_template, session, flash, redirect, url_for, request, current_app
from .. import db
from .forms import Myform
from .models import FormModel
from . import candidate_bp


@candidate_bp.route('/test')
def test():
    return 'OK'

# @candidate_bp.route('/form', methods=['GET', 'POST'])
# def form():
#     form = Myform()
    
#     if form.validate_on_submit():
#         session['username'] = form.name.data
#         session['email'] = form.email.data
        
#         form_ = FormModel(name=form.name.data, email=form.email.data,
#                   phone=form.phone.data, subject=form.subject.data,
#                   message=form.message.data)
        
        
#         email_exists = FormModel.query.filter_by(email=form.email.data).first()
#         phone_exists = FormModel.query.filter_by(phone=form.phone.data).first()
        
#         if not email_exists and not phone_exists: 
#             try:
#                 db.session.add(form_)
#             except:
#                 db.session.rollback()
#             else:
#                 db.session.commit()
            
#                 flash("Data sent successfully: " + session['username']+ ' ' + session['email'], category = 'success')
#                 current_app.logger.info("Data sent successfully: " + session['username']+ ' ' + session['email'])
#         else:
#             flash("User already exists", category="warning")
              
#         return redirect(url_for("candidate.form"))
    
#     elif request.method == 'POST':
#         flash("Not correct data", category = 'warning')
#         current_app.logger.warning("Not correct data")
        
        
    
#     # if session.get('email'):
#     form.name.data = session.get('username')
#     form.email.data = session.get('email')

#     return render_template('form.html', form=form)
 
 
# @candidate_bp.route('/db_form_table')
# def db_form_table():
#     forms = FormModel.query.all()
#     return  render_template('db_form_table.html', forms=forms)
   
