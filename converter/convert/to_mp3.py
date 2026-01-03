import pika
import json
import tempfile
import os
from bson.objectid import ObjectId
from moviepy import VideoFileClip


def start(message, fs_videos, fs_mp3, channel):
    message = json.loads(message)

    # create temp file for video
    tf = tempfile.NamedTemporaryFile(delete=False)
    
    # get video from GridFS
    out = fs_videos.get(ObjectId(message['video_fid']))
    tf.write(out.read())
    tf.close()

    # extract audio
    video = VideoFileClip(tf.name)
    audio = video.audio

    # create temp mp3 file
    tf_path = os.path.join(tempfile.gettempdir(), f"{message['video_fid']}.mp3")
    audio.write_audiofile(tf_path)

    video.close()
    audio.close()

    # store mp3 in GridFS
    with open(tf_path, "rb") as f:
        fid = fs_mp3.put(f, filename=f"{message['video_fid']}.mp3")

    # cleanup temp files
    os.remove(tf.name)
    os.remove(tf_path)

    message['mp3_fid'] = str(fid)

    try:
        channel.basic_publish(
            exchange='',
            routing_key=os.getenv("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )
    except Exception:
        fs_mp3.delete(fid)
        return "failed to queue mp3 file", 500
