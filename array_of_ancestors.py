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
    timeline(db, 1, 2, 0, False, since_id = 2)
    print '===='
    timeline(db, 1, 2, 0, True, since_id = 2)
    print '===='
    timeline(db, 1, 2, 0, False, None, max_id = 5)
    print '===='
    timeline(db, 1, 2, 0, True, None, max_id = 5)
    print '===='

def timeline(db, source_id, num = 10, start = 0, reverse = False, since_id = None, max_id = None):
    source = db.array_of_ancestors

    sort_type = 1
    if reverse is True:
        sort_type = -1

    # 直接评论文档的
    ret = []
    if since_id is not None:
        ret = source.find({'sid' : source_id, 'parent' : 0, '_id' : {'$gt' : since_id}}).sort('create_time', sort_type).limit(num)
    elif max_id is not None:
        ret = source.find({'sid' : source_id, 'parent' : 0, '_id' : {'$lt' : max_id}}).sort('create_time', sort_type).limit(num)
    else:
        ret = source.find({'sid' : source_id, 'parent' : 0}).sort('create_time', sort_type).limit(num).skip(start)

    # 直接评论文档的评论个数
    cnt = source.find({'sid' : source_id, 'parent' : 0}).count()
    tree = {'total' : cnt, 'replies' : OrderedDict()}

    # 子评论
    data = {}
    for node in ret:
        tree['replies'][node['_id']] = node
        children = source.find({'sid' : source_id, 'ancestors' : node['_id']})
        for child in children:
            data[child['_id']] = child
    for cid in data:
        ancestors = list(data[cid]['ancestors'])
        ancestors.append(cid)
        node = {'ancestors' : ancestors}
        insertNode(tree, node, data)
    print tree

def insertNode(root, node, data):
    ancestors = node['ancestors']
    for parent in ancestors:
        if 'replies' not in root or parent not in root['replies']:
            root['replies'] = OrderedDict()
            root['replies'][parent] = data[parent]
        else:
            root = root['replies'][parent]

def init(db):
    source = db.array_of_ancestors

    author = ['chen', 'shu', 'fred', 'mike', 'linda', 'fancl', 'jack', 'tom', 'ben']
    vote = ['good', 'very good', 'bad', 'very bad', 'yes', 'no']
    from random import choice
    doc_id = 1

    create_time = update_time = datetime.now()
    comment1 = {'_id' : 1, 'sid' : doc_id, 'by' : choice(author), 'content' : choice(vote), 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [], 'parent' : 0}
    source.insert(comment1)
    sleep(1)

    create_time = update_time = datetime.now()
    comment2 = {'_id' : 2, 'sid' : doc_id, 'by' : choice(author), 'content' : choice(vote), 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [], 'parent' : 0}
    source.insert(comment2)
    sleep(1)

    create_time = update_time = datetime.now()
    comment3 = {'_id' : 3, 'sid' : doc_id, 'by' : choice(author), 'content' : choice(vote), 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [2], 'parent' : 2}
    source.insert(comment3)
    sleep(1)

    create_time = update_time = datetime.now()
    comment4 = {'_id' : 4, 'sid' : doc_id, 'by' : choice(author), 'content' : choice(vote), 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [2, 3], 'parent' : 3}
    source.insert(comment4)
    sleep(1)

    create_time = update_time = datetime.now()
    comment5 = {'_id' : 5, 'sid' : doc_id, 'by' : choice(author), 'content' : choice(vote), 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [], 'parent' : 0}
    source.insert(comment5)
    sleep(1)

    create_time = update_time = datetime.now()
    comment6 = {'_id' : 6, 'sid' : doc_id, 'by' : choice(author), 'content' : choice(vote), 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [5], 'parent' : 5}
    source.insert(comment6)
    sleep(1)

    create_time = update_time = datetime.now()
    comment7 = {'_id' : 7, 'sid' : doc_id, 'by' : choice(author), 'content' : choice(vote), 'create_time' : create_time, 'update_time' : update_time, 'ancestors' : [], 'parent' : 0}
    source.insert(comment7)

if __name__ == '__main__':
    main()
