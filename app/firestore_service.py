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
    return messgaes_ref.order_by("likes").get()


def put_message(message, userEmail):
    messages_ref = db.collection("messages")
    res = {'message': message, 'id': uuid.uuid4(
    ).hex, 'userEmail': userEmail, 'likes': 0, 'isChanged': False, 'date': dumps(datetime.datetime.now(), default=json_serial)}
    messages_ref.add(res)
    return res


def put_sub_message(message_id, message, userEmail):
    sub_messages_ref = db.collection("messages").document(
        message_id).collection("sub_messages")

    return sub_messages_ref.add({'message': message, 'id': uuid.uuid4(
    ), 'userEmail': userEmail, 'likes': 0, 'isChanged': False})


def update_message(message_id, message):
    messages_ref = db.collection("messages")
    return messages_ref.document(message_id).update(
        {'message': message, 'isChanged': True})


def update_sub_message(message_id, sub_message_id, message):
    sub_messages_ref = db.collection("messages").document(
        message_id).collection("sub_messages")
    return sub_messages_ref.document(sub_message_id).update(
        {'message': message, 'isChanged': True})


def delete_message(message_id):
    messages_ref = db.collection("messages")
    messages_ref.document(message_id).delete()
    return({'message_id': message_id})


def delete_sub_message(message_id, sub_message_id):
    sub_messages_ref = db.collection("messages").document(
        message_id).collection("sub_messages")
    sub_messages_ref.document(sub_message_id).delete()
    return({'sub_message_id': sub_message_id})
