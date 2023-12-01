from flask import Flask, render_template, url_for, request, redirect
import os
import json

import create_app, database
from models import *


app = create_app.create_app()


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route('/select-category', methods=['POST', 'GET'])
def select_category():
    if request.method == 'POST':
        url = request.form['category-url']
        for cat_url in db.session.query(Category.url).distinct():
            if url == cat_url[0]:
                return "Сылка уже есть в списке"
        os.system(f'python3 main.py {url}')
        return redirect('/')

    else:
        categorys = database.get_all(Category)
        return render_template("select-category.html", categorys=categorys)


def category_id(id, char, idx_char):
    category = database.get_instance(Category, id)

    data = database.get_data(category)

    keys = list()
    for key in idx_char:
        keys.append(char[int(key)])

    data_list = list()

    for item in data:
        item_dict = json.loads(item[0])
        data_item = list()
        for key in keys:
            if key in item_dict.keys():
                data_item.append(item_dict[key])
            else:
                data_item.append("-")
        data_list.append(data_item)

    return render_template("category.html", category=category, table_head=keys, data_list=data_list)


@app.route('/select-displayed-characteristics/<int:id>', methods=['POST', 'GET'])
def select_displayed_characteristics(id):
    if request.method == 'POST':
        # print(request.form.getlist('check'))
        category = database.get_instance(Category, id)
        char = category.characteristics.split(', ')
        return category_id(id, char, request.form.getlist('check'))
        
    else:
        category = database.get_instance(Category, id)
        char = category.characteristics.split(', ')
        return render_template('select-displayed-characteristics.html', category=category, char=char)


@app.route('/faqs')
def faqs():
    return render_template('faqs.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
