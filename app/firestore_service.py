from pickle import TRUE
import uuid
import datetime
import firebase_admin
from json import dumps
from app.utils import json_serial
from firebase_admin import credentials, firestore


credentials = credentials.ApplicationDefault()
firebase_admin.initialize_app(credentials)

db = firestore.client()


def get_messages():
    messgaes_ref = db.collection("messages")
    docs = messgaes_ref.order_by(
        'likes', direction=firestore.Query.DESCENDING).get()
    data = []
    for doc in docs:
        sub_data = get_sub_messages(doc.id)
        doc = doc.to_dict()
        doc['sub_messages'] = sub_data
        data.append(doc)
    json_data = dumps(data)
    return json_data


def get_message(id):
    messages_ref = db.collection("messages")
    doc = messages_ref.document(id).get()
    return doc.to_dict()


def put_message(message, userEmail):
    id = uuid.uuid4().hex
    messages_ref = db.collection("messages").document(id)
    res = {'message': message, 'id': id, 'userEmail': userEmail, 'likes': 0,
           'isChanged': False, 'date': datetime.datetime.now().timestamp()}
    messages_ref.set(res)
    return get_messages()


def put_sub_message(message_id, message, userEmail):
    id = uuid.uuid4().hex
    sub_messages_ref = db.collection("messages").document(
        message_id).collection("sub_messages").document(id)
    res = {'message': message, 'id': id, 'userEmail': userEmail, 'likes': 0,
           'isChanged': False, 'date': datetime.datetime.now().timestamp()}
    sub_messages_ref.set(res)
    return get_messages()


def update_message(message_id, message):
    messages_ref = db.collection("messages")
    messages_ref.document(message_id).update(
        {'message': message, 'isChanged': True})
    return get_messages()


def update_sub_message(message_id, sub_message_id, message):
    sub_messages_ref = db.collection("messages").document(
        message_id).collection("sub_messages")
    sub_messages_ref.document(sub_message_id).update(
        {'message': message, 'isChanged': True})
    return get_messages()


def delete_message(message_id, sub_message_id):
    print(message_id, sub_message_id is None)
    # get message by id
    if(sub_message_id is None):
        messages_ref = db.collection("messages")
        messages_ref.document(message_id).delete()
    else:
        sub_messages_ref = db.collection(
            "messages").document(message_id).collection("sub_messages")
        sub_messages_ref.document(sub_message_id).delete()
    return get_messages()


def get_sub_messages(messgaes_id):
    sub_messages_ref = db.collection("messages").document(
        messgaes_id).collection("sub_messages")
    data = []
    docs = sub_messages_ref.order_by("likes").get()
    for doc in docs:
        data.append(doc.to_dict())
    return data


def like_message(message_id, is_like):
    messages_ref = db.collection("messages")
    if is_like:
        messages_ref.document(message_id).update(
            {'likes': firestore.Increment(1)})
    else:
        messages_ref.document(message_id).update(
            {'likes': firestore.Increment(-1)})
    return get_messages()


def like_sub_message(message_id, sub_message_id, isLike):
    sub_messages_ref = db.collection("messages").document(
        message_id).collection("sub_messages")
    if isLike:
        sub_messages_ref.document(sub_message_id).update(
            {'likes': firestore.Increment(1)})
    else:
        sub_messages_ref.document(sub_message_id).update(
            {'likes': firestore.Increment(-1)})
    return get_messages()
