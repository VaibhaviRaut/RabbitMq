try:
    import pika
    import ast
except Exception as e:
    print("Some modules are missing {}".format(e))

class MetaClass(type):
    _instance = {}
    def __call__(cls, *args, **kwargs):
        """
        Singleton Design Pattern
        :param args:
        :param kwargs:
        :return:
        """
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]

class RabbitMqServerConfigure(metaclass=MetaClass):
    def __init__(self, host='localhost', queue='hello'):
        """ Server initialization """
        self.host = host
        self.queue = queue


class rabbitmqServer():

    def __init__(self, server):
        """

        :param server: object of class RabbitMqServerConfigure
        """
        self.server = server
        self._connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        self._temp = self._channel.queue_declare(queue=self.server.queue)
        print("Server started waiting for Messages ")

    def callback(self, ch,method,properties,body):
        Payload = body.decode("utf-8")
        Payload = ast.literal_eval(Payload)
        print(type(Payload))
        with open("recevived.png","wb") as f:
            f.write(Payload)


    def startServer(self):

        # here you can write the code for database in case
        # you want to store the data in a database
        self._channel.basic_consume(queue=self.server.queue,
                      on_message_callback=self.callback,
                      auto_ack=True)
        self._channel.start_consuming()


if __name__=='__main__':
    servercofigure = RabbitMqServerConfigure(host='localhost',
                                             queue='hello')
    server = rabbitmqServer(server=servercofigure)
    server.startServer()

