#!/usr/bin/env python3
# -*- coding:utf8 -*-

import sqlite3

book_dict = {1: "大学心理学", 2: "高等教育法规", 3: "高等教育学", 4: "教师伦理学"}


def print_single_question():
    conn = sqlite3.connect("prejob_training.db")
    cur = conn.cursor()
    cur.execute("select * from single_choice WHERE cid in (2,3,4)")
    questions = cur.fetchall()
    current_book = 2
    print("%s" % book_dict[current_book])
    for question in questions:
        if question[5] == current_book:
            pass
        else:
            current_book = question[5]
            print("%s" % book_dict[current_book])

        print("%d %d %d. %s %s" % (question[0], question[3], question[6], question[1].strip(),question[4],))
        cur.execute("select * from choices where question_id=? and type=1 ORDER BY id", (question[0],))
        answers = cur.fetchall()
        for answer in answers:
            print("%s" % (answer[2].strip(),))
        print()
    conn.close()


def print_multi_question():
    conn = sqlite3.connect("prejob_training.db")
    cur = conn.cursor()
    cur.execute("select * from multi_choice WHERE cid in (2,3,4)")
    questions = cur.fetchall()
    current_book = 2
    print("%s" % book_dict[current_book])
    for question in questions:
        if question[5] == current_book:
            pass
        else:
            current_book = question[5]
            print("%s" % book_dict[current_book])

        print("%d %d %d. %s %s" % (question[0], question[3], question[6], question[1].strip(),question[4],))
        cur.execute("select * from choices where question_id=? and type=2 ORDER BY id", (question[0],))
        answers = cur.fetchall()
        for answer in answers:
            print("%s" % (answer[2].strip(),))
        print()
    conn.close()


def print_true_false():
    conn = sqlite3.connect("prejob_training.db")
    cur = conn.cursor()
    cur.execute("select * from true_false WHERE cid in (2,3,4)")
    questions = cur.fetchall()
    current_book = 2
    print("%s" % book_dict[current_book])
    for question in questions:
        if question[5] == current_book:
            pass
        else:
            current_book = question[5]
            print("%s" % book_dict[current_book])

        print("%d %d %d. %s %s" % (question[0], question[3], question[6], question[1].strip(), question[4],))

        print()
    conn.close()


if __name__ == "__main__":
    print_single_question()
    print_multi_question()
    print_true_false()