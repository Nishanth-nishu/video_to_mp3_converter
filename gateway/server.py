import os, gridfs, pika, json
from flask import Flask, request, jsonify, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage.util import upload as upload_util
from bson.objectid import ObjectId

server = Flask(__name__)


mongo_video= PyMongo(server, uri='mongodb://mongo:27017/videos')
mongo_mp3= PyMongo(server, uri='mongodb://mongo:27017/mp3s')

fs_video = gridfs.GridFS(mongo_video.db)
fs_mp3 = gridfs.GridFS(mongo_mp3.db)


connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()
@server.route('/login', methods=['POST'])
def login():
    token, err = access.login(request)
    if not err:
        return token
    else:    
        return err

@server.route('/upload', methods=['POST'])
def upload():
    access_data, err = validate.token(request)
    if err:
        return err
    access = json.loads(access_data)

    if access['admin']:
        if len(request.files) > 1 or len(request.files) < 0:
            return jsonify({"error": "only one file allowed"}), 400

        for _, file in request.files.items():
            err = upload_util(file, fs_video, channel, access)
            if err:
                return err        
        return jsonify({"status": "file uploaded"}), 200
    else:
        return jsonify({"error": "admin access required"}), 403

@server.route('/download', methods=['GET'])
def download():
    access_data, err = validate.token(request)
    if err:
        return err
    access = json.loads(access_data)

    if access['admin']:
        fid_string = request.args.get('fid', default=None)
        if not fid_string:
            return jsonify({"error": "missing fid parameter"}), 400
        try:
            out = fs_mp3.get(ObjectId(fid_string))
            return send_file(
                out,
                download_name=F"{fid_string}.mp3",
                as_attachment=True
            )
        except Exception as err:
            print("Mongo/GridFS error:", err)
            return jsonify({"error": "file not found"}), 404

    return jsonify({"error": "admin access required"}), 403
   
if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)