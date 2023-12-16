from sqlalchemy.sql import text
import json
import sqlite3
from datetime import datetime
import time
import logging

from models import db, Category
from config import database_name

logging.basicConfig(level=logging.DEBUG)

def get_all(model):
    data = model.query.all()
    return data


def get_instance(model, id):
    return model.query.get_or_404(id)


def get_data(category):
    name = category.name_of_category.replace(' ', '_')
    cursor = db.session.execute(text(f'SELECT json_data FROM {name}'))
    data = cursor.fetchall()
    return data


def add_instance(name, item):
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        json_data = json.dumps(item)
        insert = f'INSERT INTO {name} (json_data) VALUES (?)'
        cursor.execute(insert, (json_data, ))


def delete_instance(model, id):
    model.query.filter_by(id=id).delete()
    commit_changes()


def create_table(table_name):
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        query = f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, json_data TEXT NOT NULL)'
        cursor.execute(query)


def delete_table(name_table):
    # table = db.metadata.tables[name_table]
    # if table is not None:
    #     db.metadata.drop_all(db.engine, [table], checkfirst=True)
    #     commit_changes()
    try:
        db.session.execute(text(f"SELECT id FROM {name_table} WHERE id = 1"))
        db.session.execute(text(f'DROP TABLE {name_table}'))
        commit_changes()
    except Exception as ex:
        logging.error(ex)
        pass


def add_category(category):
    # if category['url'] in db.session.query(Category.url).distinct():
    #     print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #     Category.query.filter_by(url=category['url']).update({'data_last_pars' : str(datetime.utcfromtimestamp(int(time.time())))})
    # else:
    #     instance = Category(category)
    #     db.session.add(instance)
    #     commit_changes()

    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Category (
        id INTEGER PRIMARY KEY,
        name_of_category TEXT NOT NULL,
        url TEXT NOT NULL,
        data_last_pars TEXT NOT NULL,
        characteristics TEXT NOT NULL
        )
        ''')
        cursor.execute("SELECT name_of_category FROM Category WHERE name_of_category = ?", (category["name"], ))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO Category (name_of_category, url, data_last_pars, characteristics) VALUES (?, ?, ?, ?)',\
                        (category["name"],category['url'], str(datetime.utcfromtimestamp(int(time.time()))), category["characteristics"]))
        else:
            cursor.execute('UPDATE Category SET data_last_pars = ? WHERE name_of_category = ?',\
                        (str(datetime.utcfromtimestamp(int(time.time()))), category["name"]))


def commit_changes():
    db.session.commit()
