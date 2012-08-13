#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from datetime import datetime
from pymongo import Connection
from time import sleep

def main():
    connection = Connection('192.168.194.171', 27017)
    db = connection.comments

    init(db)

def init(db):
    collection = db.full_tree_in_single_document

    author = ['chen', 'shu', 'fred', 'mike', 'linda', 'fancl', 'jack', 'tom', 'ben']
    vote = ['good', 'very good', 'bad', 'very bad', 'yes', 'no']
    from random import choice
    doc_id = 1

    doc = {'_id' : doc_id, 'comments' : []}
    collection.insert(doc)

    create_time = update_time = datetime.now()
    comment1 = {'id' : 1, 'by' : choice(author), 'content' : choice(vote), 'replies' : [], 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [], 'parent' : -1}
    collection.update({'_id' : doc_id}, {'$push' : {'comments' : comment1}})
    sleep(1)

    create_time = update_time = datetime.now()
    comment2 = {'id' : 2, 'by' : choice(author), 'content' : choice(vote), 'replies' : [], 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [], 'parent' : -1}
    collection.update({'_id' : doc_id}, {'$push' : {'comments' : comment2}})
    sleep(1)

    create_time = update_time = datetime.now()
    comment3 = {'id' : 3, 'by' : choice(author), 'content' : choice(vote), 'replies' : [], 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [1], 'parent' : 1}
    collection.update({'_id' : doc_id}, {'$push' : {'comments.1.replies' : comment3}})
    sleep(1)

    create_time = update_time = datetime.now()
    comment4 = {'id' : 4, 'by' : choice(author), 'content' : choice(vote), 'replies' : [], 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [1, 0], 'parent' : 0}
    collection.update({'_id' : doc_id}, {'$push' : {'comments.1.replies.0.replies' : comment4}})
    sleep(1)

    create_time = update_time = datetime.now()
    comment5 = {'id' : 5, 'by' : choice(author), 'content' : choice(vote), 'replies' : [], 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [], 'parent' : -1}
    collection.update({'_id' : doc_id}, {'$push' : {'comments' : comment5}})
    sleep(1)

    create_time = update_time = datetime.now()
    comment6 = {'id' : 6, 'by' : choice(author), 'content' : choice(vote), 'replies' : [], 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [2], 'parent' : 2}
    collection.update({'_id' : doc_id}, {'$push' : {'comments.2.replies' : comment6}})

if __name__ == '__main__':
    main()
