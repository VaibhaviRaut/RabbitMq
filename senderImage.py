
try:
    import pika
except Exception as e:
    print("Some modules are missing {}".format_map(e))

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

class RabbitMqConfigure(metaclass=MetaClass):

    def __init__(self,queue='hello', host='localhost', routingKey='hello', exchange=''):
        """Configure Rabbit Mq Server"""
        self.queue = queue
        self.host = host
        self.routingKey = routingKey
        self.exchange = exchange



class RabbitMq():

    __slots__ = ["server", "_channel", "_connection"]      #to make code efficient at runtime

    def __init__(self, server: object) -> object:
        """

        :param server: Object of Rabbit MqConfigure class
        """
        self.server = server
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    def __enter__(self):
        print("__enter__")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__")
        self._connection.close()

    def publish(self, payload={}):
        """
        Takes a JSON payload
        :param payload:
        :return:
        """
        self._channel.basic_publish(exchange=self.server.exchange,
                      routing_key=self.server.routingKey,
                      body=str(payload))
        print("Published Message: {}".format(payload))

class Image(object):

    __slots__ = ["filename"]

    def __init__(self, filename):
        self.filename = filename

    #Property Decorator
    @property
    def get(self):
        with open(self.filename, "rb") as f:
            data = f.read()
        return data



if __name__=='__main__':

    server = RabbitMqConfigure(queue='hello',
                               host='localhost',
                               routingKey='hello',
                               exchange='')

    # call image class
    image = Image(filename="/Users/vaibhaviraut/PycharmProjects/RabbitMq/111112.png")
    data = image.get

    #to make code efficient
    with RabbitMq(server) as rabbitmq:
        rabbitmq.publish(payload=data)

    '''
    rabbitmq = RabbitMq(server)
    rabbitmq.publish(payload={"Data":22})
    '''
