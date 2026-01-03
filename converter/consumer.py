import pika
import sys
import os
import time
import gridfs
from pymongo import MongoClient
from convert import to_mp3


def main():
    client = MongoClient("mongo", 27017)

    db_videos = client.videos
    db_mp3s = client.mp3s

    fs_video = gridfs.GridFS(db_videos)
    fs_mp3 = gridfs.GridFS(db_mp3s)

    # RabbitMQ connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = to_mp3.start(body, fs_video, fs_mp3,ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    queue_name = os.getenv("VIDEO_QUEUE")

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False,
    )


    print(" [*] Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
