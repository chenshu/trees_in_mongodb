#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from datetime import datetime
from pymongo import Connection
from time import sleep

def main():
    connection = Connection('192.168.194.171', 27017)
    db = connection.comments

    #init(db)
    timeline(db, 1, 2)
    print '===='
    timeline(db, 1, 2, 0, True)
    print '===='
    timeline(db, 1, 2, 1)
    print '===='
    timeline(db, 1, 2, 1, True)
    print '===='
    timeline(db, 1, 2, 0, False, since_id = 1)
    print '===='
    timeline(db, 1, 2, 0, True, since_id = 1)
    print '===='
    timeline(db, 1, 2, 0, False, None, max_id = 2)
    print '===='
    timeline(db, 1, 2, 0, True, None, max_id = 2)
    print '===='

def timeline(db, source_id, num = 10, start = 0, reverse = False, since_id = None, max_id = None):
    collection = db.full_tree_in_single_document

    skip = start
    if since_id is not None:
        skip = since_id + 1
    elif max_id is not None:
        skip = 0 if (max_id - num < 0) else max_id - num
    else:
        if reverse is True:
            skip = (0 - (skip + num))
    ret = collection.find({'_id' : source_id}, {'comments' : {'$slice' : [skip, num]}})

    for item in ret:
        total = item['total']
        for index, comment in enumerate(item['comments']):
            if since_id is not None:
                comment['index'] = since_id + 1 + index
            elif max_id is not None:
                comment['index'] = abs(max_id - num + index)
            else:
                if reverse is True:
                    comment['index'] = total - num + index - start
                else:
                    comment['index'] = start + index
        if reverse is True:
            item['comments'].reverse()
        print item

def init(db):
    collection = db.full_tree_in_single_document

    author = ['chen', 'shu', 'fred', 'mike', 'linda', 'fancl', 'jack', 'tom', 'ben']
    vote = ['good', 'very good', 'bad', 'very bad', 'yes', 'no']
    from random import choice
    doc_id = 1

    doc = {'_id' : doc_id, 'comments' : [], 'total' : 0}
    collection.insert(doc)

    create_time = update_time = datetime.now()
    comment1 = {'id' : 1, 'by' : choice(author), 'content' : choice(vote), 'replies' : [], 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [], 'parent' : -1}
    collection.update({'_id' : doc_id}, {'$push' : {'comments' : comment1}, '$inc' : {'total' : 1}})
    sleep(1)

    create_time = update_time = datetime.now()
    comment2 = {'id' : 2, 'by' : choice(author), 'content' : choice(vote), 'replies' : [], 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [], 'parent' : -1}
    collection.update({'_id' : doc_id}, {'$push' : {'comments' : comment2}, '$inc' : {'total' : 1}})
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
    collection.update({'_id' : doc_id}, {'$push' : {'comments' : comment5}, '$inc' : {'total' : 1}})
    sleep(1)

    create_time = update_time = datetime.now()
    comment6 = {'id' : 6, 'by' : choice(author), 'content' : choice(vote), 'replies' : [], 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [2], 'parent' : 2}
    collection.update({'_id' : doc_id}, {'$push' : {'comments.2.replies' : comment6}})
    sleep(1)

    create_time = update_time = datetime.now()
    comment7 = {'id' : 7, 'by' : choice(author), 'content' : choice(vote), 'replies' : [], 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [], 'parent' : -1}
    collection.update({'_id' : doc_id}, {'$push' : {'comments' : comment7}, '$inc' : {'total' : 1}})

if __name__ == '__main__':
    main()
