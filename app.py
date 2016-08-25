# -*- coding: utf-8 -*-

from flask import Flask, session, request
import json, uuid, base64
from pyfcm import FCMNotification

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

push_service = FCMNotification(api_key="AIzaSyBEVkJRz7HazHJq_u8NmQP5ZLJikf1lEbM")


class User(object):
    pass


users = {
}

crawlers = {
    "sdhfi3": {
        "crawler_id": "sdhfi3",
        "title": "한양대학교 컴퓨터전공 공지사항",
        "description": "한양대 컴공 공지 알림",
        "thumbnail_url": "http://cs.hanyang.ac.kr/images/common/logo.gif",
    },
    "asfd13": {
        "crawler_id": "asfd13",
        "title": "네이버 실시간 검색어 순위",
        "description": "네이버 실시간 검색어 순위가 바뀌었을 때 알림",
        "thumbnail_url": "http://img.naver.net/static/www/u/2013/0731/nmms_224940510.gif",
    },
    "wf42i": {
        "crawler_id": "wf42i",
        "title": "디시인사이드 힛갤러리 알림",
        "description": "디시인사이드 힛갤러리에 새글이 등록되면 알림",
        "thumbnail_url": "http://wstatic.dcinside.com/main/main2011/dcmain/logo_swf/top_logo_160718.png",
    },
    "xvio31": {
        "crawler_id": "xvio31",
        "title": "Steam 세일 알림",
        "description": "새로 등록되는 세일 아이템을 알림",
        "thumbnail_url": "http://steamcommunity-a.akamaihd.net/public/shared/images/header/globalheader_logo.png",
    },
    "j1ktk2": {
        "crawler_id": "j1ktk2",
        "title": "LOL 패치노트",
        "description": "새로 등록된 패치노트 확인",
        "thumbnail_url": "https://upload.wikimedia.org/wikipedia/en/thumb/7/77/League_of_Legends_logo.png/500px-League_of_Legends_logo.png",
    }
}


@app.route("/")
def index():
    return "HungryOsori TestServer"


def make_error_response(error_code, message):
    result = {}
    result['error'] = error_code
    result['message'] = message

    return json.dumps(result)


def make_success_result(**args):
    result = {}
    result['error'] = 0
    result['message'] = 'Success'

    for key, value in args.items():
        result[key] = value

    return json.dumps(result)


def refresh_user_key():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return r_uuid.replace('=', '')


def verify_user():
    user_id = None
    user_key = None

    try:
        user_id = request.form['user_id']
        user_key = request.form['user_key']
    except Exception as e:
        return False, -1, -1, "no have form data 'user_id' or 'user_key"

    try:
        if session['user_id'] != user_id or session['user_key'] != user_key:
            return False, -1, -1, "invalid session"
    except Exception as e:
        return False, -1, -1, "no have key in session"

    return True, user_id, user_key


@app.route('/req_login', methods=["POST"])
def req_login():
    try:
        user_id = request.form['user_id']
    except Exception as e:
        return make_error_response(-1, "no have form data 'user_id'")

    try:
        user_key = request.form['user_key']
    except:
        user_key = refresh_user_key()

    try:
        push_token = request.form['token']
    except Exception as e:
        push_token = None

    if 'user_id' in session:
        if session['user_id'] != user_id:
            session['user_id'] = user_id
            session['user_key'] = user_key
        elif session['user_key'] != user_key:
            session.pop('user_id', None)
            session.pop('user_key', None)

            return make_error_response(-1, "invalid session, retry to login")
    else:
        session['user_id'] = user_id
        session['user_key'] = user_key

    if user_id not in users:
        users[user_id] = User()
        users[user_id].id = user_id
        users[user_id].subscriptions = []
        users[user_id].token = push_token

    return make_success_result(user_key=user_key)


@app.route("/req_subscription_list", methods=["GET", "POST"])
def req_subscription_list():
    if request.method == "GET":
        return make_error_response(-1, "need to change request method(get -> post)")

    user_verified_info = verify_user()
    if not user_verified_info[0]:
        return make_error_response(-1, "invalid user id-key")

    user_id = user_verified_info[1]

    try:
        if users.has_key(user_id) is True:
            subscription_list = users[user_id].subscriptions
    except:
        return make_error_response(-1, "collection error")

    return make_success_result(subscriptions=subscription_list)


@app.route("/req_entire_list", methods=["POST"])
def req_entire_list():
    user_info = verify_user()
    if not user_info[0]:
        return make_error_response(-1, "invalid user id-key")

    return make_success_result(crawlers=[item for item in crawlers.itervalues()])


@app.route("/req_subscribe_crawler", methods=["POST"])
def req_subscribe_crawler():
    user_info = verify_user()
    if not user_info[0]:
        return make_error_response(-1, "invalid user id-key")

    user_id = user_info[1]

    try:
        crawler_id = request.form['crawler_id']
    except Exception as e:
        return make_error_response(-1, "no have crawler_id")

    try:
        if crawler_id in users[user_id].subscriptions:
            return make_error_response(-1, "already registered")
    except:
        return make_error_response(-1, "collection error")

    users[user_id].subscriptions.append(crawler_id)

    return make_success_result()


@app.route("/req_unsubscribe_crawler", methods=["POST"])
def req_unsubscribe_crawler():
    user_info = verify_user()
    if not user_info[0]:
        return make_error_response(-1, "invalid user id-key")

    user_id = user_info[1]

    try:
        crawler_id = request.form['crawler_id']
    except Exception as e:
        return make_error_response(-1, "no have crawler_id")

    try:
        if crawler_id not in users[user_id].subscriptions:
            return make_error_response(-1, "not registered")
    except:
        return make_error_response(-1, "collection error")

    users[user_id].subscriptions.remove(crawler_id)

    return make_success_result()


@app.route("/register_push_token", methods=["POST"])
def req_register_push_token():
    user_info = verify_user()
    if not user_info[0]:
        return make_error_response(-1, "invalid user id-key")

    try:
        token = request.form['token']
    except Exception as e:
        return make_error_response(-1, "no have apple push token")

    user_id = user_info[1]
    users[user_id].token = token

    return make_success_result()


@app.route('/req_push', methods=["POST"])
def req_push():
    try:
        title = request.form['title']
        message = request.form['message']
    except Exception as e:
        return make_error_response(-1, "invalid data")

    tokens = []
    for user in users:
        if hasattr(user, 'token') is True:
            tokens.append(user.token)

    try:
        result = push_service.notify_multiple_devices(registration_ids=tokens, message_title=title, message_body=message)
    except Exception as e:
        print e

    print result

    return str(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
