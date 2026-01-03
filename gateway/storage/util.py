import pika, json

def upload(file, fs, channel, access):
    try:
            file_id = fs.put(file.stream,
                             filename=file.filename,
                             content_type=file.mimetype
                             )
            
    except Exception as err:
        print("Mongo/GridFS error:", err)
        return {"error": "failed to store file"}, 500 
    message = {
        "video_fid": str(file_id),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            ),
        )
        return None
    except Exception:
        fs.delete(file_id)
        return "error: failed to queue file", 500
