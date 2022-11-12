from flask import render_template, request, flash, redirect, url_for, session
import datetime
from loguru import logger

from app import app, db
from app.forms import ContactForm
from app.models import Contact


@app.route('/')
@app.route('/home')
def homepage():
    return render_template('homepage.html', title='Home')


@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        logger.debug(f"""The form is sent in {datetime.datetime.now()}
                    Name = {form.name.data}
                    Email = {form.email.data}
                    Phone = {form.phone.data}
                    Subject = {dict(form.subject.choices).get(form.subject.data)}
                    Message = {form.message.data}""")
        db.session.add(Contact(name=form.name.data, email=form.email.data, phone=form.phone.data,
                               subject=dict(form.subject.choices).get(form.subject.data), message=form.message.data))
        db.session.commit()
        session['name'] = form.name.data
        session['email'] = form.email.data
        flash(f"Дані успішно відправлено: {form.name.data}, {form.email.data}", category='success')
        return redirect(url_for("contact"))

    elif request.method == 'POST':
        flash("Не пройшла валідація з Post", category='warning')

    form.name.data = session.get("name")
    form.email.data = session.get("email")
    return render_template('contact.html', form=form)


@app.route('/reset', methods=["GET", "POST"])
def reset():
    if session.get('email') is not None and session.get('name') is not None:
        session.pop("email")
        session.pop("name")
    return redirect(url_for("contact"))


@app.route('/display_contacts', methods=["GET", "POST"])
def display_contacts():
    return render_template('contact_table.html', contacts=Contact.query.all())


@app.route('/delete_contact/<contact_id>', methods=["GET", "POST"])
def delete_contact(contact_id):
    db.session.delete(db.session.query(Contact).get(contact_id))
    db.session.commit()
    return redirect(url_for("display_contacts"))
