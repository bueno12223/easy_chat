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
    docs = messgaes_ref.order_by("likes").get()
    data = []
    for doc in docs:
        sub_data = get_sub_messages(doc.id)
        doc = doc.to_dict()
        doc['sub_messages'] = sub_data
        data.append(doc)

    json_data = dumps(data)
    return json_data


def get_message(message_id):
    messages_ref = db.collection("messages")
    sub_data = get_sub_messages(message_id)
    doc = messages_ref.document(message_id).get().to_dict()
    doc['sub_messages'] = sub_data
    return doc


def put_message(message, userEmail):
    messages_ref = db.collection("messages")
    res = {'message': message, 'id': uuid.uuid4(
    ).hex, 'userEmail': userEmail, 'likes': 0, 'isChanged': False, 'date': dumps(datetime.datetime.now(), default=json_serial)}
    messages_ref.add(res)
    return res


def put_sub_message(message_id, message, userEmail):
    sub_messages_ref = db.collection("messages").document(
        message_id).collection("sub_messages")
    res = {'message': message, 'id': uuid.uuid4(
    ).hex, 'userEmail': userEmail, 'likes': 0, 'isChanged': False, 'date': dumps(datetime.datetime.now(), default=json_serial)}
    sub_messages_ref.add(res)
    return get_message(message_id)


def update_message(message_id, message):
    messages_ref = db.collection("messages")
    messages_ref.document(message_id).update(
        {'message': message, 'isChanged': True})
    return get_message(message_id)


def update_sub_message(message_id, sub_message_id, message):
    sub_messages_ref = db.collection("messages").document(
        message_id).collection("sub_messages")
    sub_messages_ref.document(sub_message_id).update(
        {'message': message, 'isChanged': True})
    return get_message(message_id)


def delete_message(message_id):
    messages_ref = db.collection("messages")
    messages_ref.document(message_id).delete()
    return message_id


def delete_sub_message(message_id, sub_message_id):
    sub_messages_ref = db.collection("messages").document(
        message_id).collection("sub_messages")
    sub_messages_ref.document(sub_message_id).delete()
    return {'message_id': message_id, 'sub_message_id': sub_message_id}


def get_sub_messages(messgaes_id):
    sub_messages_ref = db.collection("messages").document(
        messgaes_id).collection("sub_messages")
    data = []
    docs = sub_messages_ref.order_by("likes").get()
    for doc in docs:
        data.append(doc.to_dict())
    return data


def like_message(message_id, isLike):
    messages_ref = db.collection("messages")
    if isLike:
        messages_ref.document(message_id).update(
            {'likes': firestore.Increment(1)})
    else:
        messages_ref.document(message_id).update(
            {'likes': firestore.Increment(-1)})


def like_sub_message(message_id, sub_message_id, isLike):
    sub_messages_ref = db.collection("messages").document(
        message_id).collection("sub_messages")
    if isLike:
        sub_messages_ref.document(sub_message_id).update(
            {'likes': firestore.Increment(1)})
    else:
        sub_messages_ref.document(sub_message_id).update(
            {'likes': firestore.Increment(-1)})
