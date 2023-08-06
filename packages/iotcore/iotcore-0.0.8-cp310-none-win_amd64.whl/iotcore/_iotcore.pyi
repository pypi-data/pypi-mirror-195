
def hello()->None:
    """Hello world

    :return: None
    """
    ...

def mqtt_sub(server: str,
             sub_topic: str,
             port: int
             ) -> None:
    """mqtt_sub

    Function for subscribing to a mqtt topic.
    All messages on the given topic will be printed out

    :param server: mqtt server url
    :param sub_topic: subscription topic
    :param port: mqtt server port
    :return: None
    """
    ...
