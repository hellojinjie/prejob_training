#!/usr/bin/env python3
# -*- coding:utf8 -*- 

import requests
import sqlite3
import hashlib
import time
from bs4 import BeautifulSoup
from string import Template

c = [1, 2, 3, 4]
p = range(1, 21)

urlTemplate = Template("http://zjzx.zjnu.edu.cn/test/Default.aspx?cid=${cid}&pid=${pid}")

'''
drop table choices;
drop table multi_choice;
drop table single_choice;
drop table true_false;

CREATE TABLE choices(id integer primary key autoincrement, question_id integer, title string);

CREATE TABLE multi_choice(id integer primary key autoincrement, title string, digest string, appear_count int, answer string, cid integer, pid integer);

CREATE TABLE single_choice(id integer primary key autoincrement, title string, digest string, appear_count int, answer string, cid integer, pid integer);

CREATE TABLE true_false(id integer primary key autoincrement, title string, digest string, appear_count int, answer string, cid integer, pid integer);
'''


def get_page_text(cid0, pid0):
    url = urlTemplate.substitute(cid=cid0, pid=pid0)
    session = requests.session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
    response = session.get(url)

    page = BeautifulSoup(response.text)
    view_state = page.find("input", id="__VIEWSTATE")
    event_validation = page.find("input", id="__EVENTVALIDATION")
    data = {
        "drop1": cid0,
        "drop2": pid0,
        "Button1": "提交并查看单选题答案",
        "__VIEWSTATE": view_state['value'],
        "__EVENTVALIDATION": event_validation['value']
    }
    response = session.post(url, data)

    page = BeautifulSoup(response.text)
    view_state = page.find("input", id="__VIEWSTATE")
    event_validation = page.find("input", id="__EVENTVALIDATION")
    data = {
        "drop1": cid0,
        "drop2": pid0,
        "Button2": "提交并查看多选题答案",
        "__VIEWSTATE": view_state['value'],
        "__EVENTVALIDATION": event_validation['value']
    }
    response = session.post(url, data)

    page = BeautifulSoup(response.text)
    view_state = page.find("input", id="__VIEWSTATE")
    event_validation = page.find("input", id="__EVENTVALIDATION")

    data = {
        "drop1": cid0,
        "drop2": pid0,
        "Button3": "提交并查看判断题答案",
        "__VIEWSTATE": view_state['value'],
        "__EVENTVALIDATION": event_validation['value']
    }
    response = session.post(url, data)
    return response.text


def parse_question(text, cid0, pid0):
    conn = sqlite3.connect("prejob_training.db")
    cur = conn.cursor()
    try:
        page = BeautifulSoup(text)
        for num in range(2, 42):
            num_zfill = str(num).zfill(2)
            question = page.find("span", {'id': Template('GridView1_ctl${num}_Label1').substitute(num=num_zfill)}).string
            answer = page.find("span", {'id': Template('GridView1_ctl${num}_Label6').substitute(num=num_zfill)}).string
            selection_a = page.find("span", {'id': Template('GridView1_ctl${num}_Label2').substitute(num=num_zfill)}).string
            selection_b = page.find("span", {'id': Template('GridView1_ctl${num}_Label3').substitute(num=num_zfill)}).string
            selection_c = page.find("span", {'id': Template('GridView1_ctl${num}_Label4').substitute(num=num_zfill)}).string
            selection_d = page.find("span", {'id': Template('GridView1_ctl${num}_Label5').substitute(num=num_zfill)}).string
            digest = hashlib.md5(str(question + selection_a + selection_b + selection_c + selection_d).encode("utf-8")).hexdigest()
            cur.execute("select appear_count from single_choice where digest=?", (digest, ))
            appear_count = 1
            row = cur.fetchone()
            if row is not None:
                cur.execute("update single_choice set appear_count=appear_count+1 where digest=?", (digest, ))
            else:
                cur.execute("insert into single_choice (title, digest, appear_count, answer, cid, pid) values (?,?,?,?,?,?)",
                        (question, digest, appear_count, answer, cid0, pid0))
                question_id = cur.lastrowid
                cur.execute("insert into choices (question_id, title) values (?, ?)", (question_id, selection_a))
                cur.execute("insert into choices (question_id, title) values (?, ?)", (question_id, selection_b))
                cur.execute("insert into choices (question_id, title) values (?, ?)", (question_id, selection_c))
                cur.execute("insert into choices (question_id, title) values (?, ?)", (question_id, selection_d))

        for num in range(2, 22):
            num_zfill = str(num).zfill(2)
            question = page.find("span", {'id': Template('GridView2_ctl${num}_Label15').substitute(num=num_zfill)}).string
            answer = page.find("span", {'id': Template('GridView2_ctl${num}_Label16').substitute(num=num_zfill)}).string
            selection_a = page.find("span", {'id': Template('GridView2_ctl${num}_Label17').substitute(num=num_zfill)}).string
            selection_b = page.find("span", {'id': Template('GridView2_ctl${num}_Label18').substitute(num=num_zfill)}).string
            selection_c = page.find("span", {'id': Template('GridView2_ctl${num}_Label19').substitute(num=num_zfill)}).string
            selection_d = page.find("span", {'id': Template('GridView2_ctl${num}_Label20').substitute(num=num_zfill)}).string
            selection_e = page.find("span", {'id': Template('GridView2_ctl${num}_Label21').substitute(num=num_zfill)}).string
            selection_f = page.find("span", {'id': Template('GridView2_ctl${num}_Label22').substitute(num=num_zfill)}).string
            digest = hashlib.md5(
                str(question + selection_a + selection_b + selection_c + selection_d).encode("utf-8")).hexdigest()
            cur.execute("select appear_count from multi_choice where digest=?", (digest,))
            appear_count = 1
            row = cur.fetchone()
            if row is not None:
                cur.execute("update multi_choice set appear_count=appear_count+1 where digest=?", (digest,))
            else:
                cur.execute("insert into multi_choice (title, digest, appear_count, answer, cid, pid) values (?,?,?,?,?,?)",
                            (question, digest, appear_count, answer, cid0, pid0))
                question_id = cur.lastrowid
                cur.execute("insert into choices (question_id, title) values (?, ?)", (question_id, selection_a))
                cur.execute("insert into choices (question_id, title) values (?, ?)", (question_id, selection_b))
                cur.execute("insert into choices (question_id, title) values (?, ?)", (question_id, selection_c))
                cur.execute("insert into choices (question_id, title) values (?, ?)", (question_id, selection_d))
                if selection_e:
                    cur.execute("insert into choices (question_id, title) values (?, ?)", (question_id, selection_e))
                if selection_f:
                    cur.execute("insert into choices (question_id, title) values (?, ?)", (question_id, selection_f))

        for num in range(2, 22):
            num_zfill = str(num).zfill(2)
            question = page.find("span", {'id': Template('GridView3_ctl${num}_Label40').substitute(num=num_zfill)}).string
            answer = page.find("span", {'id': Template('GridView3_ctl${num}_Label41').substitute(num=num_zfill)}).string
            digest = hashlib.md5(str(question).encode("utf-8")).hexdigest()
            cur.execute("select appear_count from true_false where digest=?", (digest,))
            appear_count = 1
            row = cur.fetchone()
            if row is not None:
                cur.execute("update true_false set appear_count=appear_count+1 where digest=?", (digest,))
            else:
                cur.execute("insert into true_false (title, digest, appear_count, answer, cid, pid) values (?,?,?,?,?,?)",
                            (question, digest, appear_count, answer, cid0, pid0))
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e
    conn.commit()
    conn.close()


def do_work(cid0, pid0):
    url = urlTemplate.substitute(cid=cid0, pid=pid0)
    try:
        page_text = get_page_text(cid0, pid0)
        parse_question(page_text, cid0, pid0)
        print("success:%s" %(url,))
    except Exception as error:
        print("failed:%s" %(url,))

for cid in c:
    for pid in p:
        do_work(cid, pid)
        time.sleep(2)
