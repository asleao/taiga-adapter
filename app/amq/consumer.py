import threading

import pika

from .controller import setup, callback_project, callback_collaborator


class Consumer(object):
    """ Background thread for consuming queues
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self):
        """ Constructor
        """

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self):
        params_amq = setup()
        connection = pika.BlockingConnection(params_amq)
        channel = connection.channel()  # start a channel
        channel.queue_declare(queue='Taiga_Repository_Test')
        channel.queue_declare(queue='Taiga_Collaborator')
        channel.basic_consume('Taiga_Repository_Test', callback_project, auto_ack=True)
        channel.basic_consume('Taiga_Collaborator', callback_collaborator, auto_ack=True)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()

        connection.close()
