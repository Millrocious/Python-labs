from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from loguru import logger

from . import todo_bp
from .forms import TaskForm, CategoryForm, CommentForm
from .models import Task, Category, Comment
from .. import db


@todo_bp.route('/task/create', methods=["GET", "POST"])
@login_required
def task_create():
    form = TaskForm()
    if form.validate_on_submit():
        logger.debug(f"""title={form.title.data},
                                message={form.description.data},
                                deadline={form.deadline.data},
                                priority={form.priority.data},
                                progress={form.progress.data},
                                owner={current_user}""")

        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data
        priority = form.priority.data
        progress = form.progress.data
        category = form.category.data
        task_info = Task(title=title,
                         description=description,
                         deadline=deadline,
                         priority=priority,
                         progress=progress,
                         category_id=category,
                         owner_id=current_user.id)
        task_info.users.append(current_user)
        db.session.add(task_info)
        db.session.commit()

        flash(f"Task successfully created: {form.title.data}", category='success')
        return redirect(url_for("todo_bp.task_create"))
    elif request.method == 'POST':
        flash("Не пройшла валідація з Post", category='warning')
        return redirect(url_for("todo_bp.task_create"))

    return render_template('task_form.html', title="Create task", form=form)


@todo_bp.route('/category/create', methods=['GET', 'POST'])
@login_required
def category_create():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        cat_info = Category(name=name)
        db.session.add(cat_info)
        db.session.commit()

        flash(f"Category successfully added", category='success')
        return redirect(url_for("todo_bp.category_create"))

    elif request.method == 'POST':
        flash("Не пройшла валідація з Post", category='warning')
        return redirect(url_for("todo_bp.category_create"))

    return render_template('category_form.html', form=form)


@todo_bp.route('/task/<int:task_id>', methods=['GET'])
@login_required
def detail_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task_detail = {
        'Title': task.title,
        'Description': task.description,
        'Created': task.created,
        'Modified': task.modified,
        'Deadline': task.deadline.date(),
        'Priority': task.priority,
        'Progress': task.progress
    }
    form = TaskForm()
    form_comment = CommentForm()
    comments = Comment.query.filter_by(task_id=task_id).all()
    data = {
        'form_comment': form_comment,
        'comments': comments
    }
    return render_template('task.html', task_detail=task_detail,
                           task_id=task.id,
                           form=form,
                           assigned=task.users,
                           data=data)


@todo_bp.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def task_update(task_id):
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data
        priority = form.priority.data
        progress = form.progress.data

        task = Task.query.filter_by(id=task_id).first()
        task.title = title
        task.description = description
        task.deadline = deadline
        task.priority = priority
        task.progress = progress
        db.session.add(task)
        db.session.commit()

        flash(f"Task successfully updated", category='success')
        return redirect(url_for("todo_bp.detail_task", task_id=task_id))

    elif request.method == 'POST':
        print(form.errors, form.description.data)
        flash("Не пройшла валідація з Post", category='warning')
        return redirect(url_for("todo_bp.detail_task", task_id=task_id))

    return render_template('task_update.html', title="Update task", form=form, task_id=task_id)


@todo_bp.route('/task/<int:task_id>/delete', methods=['GET', 'POST'])
@login_required
def task_delete(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    flash("Successfully deleted!", category='success')
    return redirect(url_for("todo_bp.task_create"))


@todo_bp.route('/task/list', methods=['GET', 'POST'])
@login_required
def list_task():
    task_list = current_user.tasks
    task_list = task_list.order_by(Task.priority.desc())
    task_list = task_list.order_by(Task.deadline.asc())
    print("fd")
    # task_list = Task.query.filter(Task.users.any(id=current_user.id)).all()
    # print(type(task_list[0].owner_id))
    return render_template('tasks.html', title="Update task", task_list=task_list)
