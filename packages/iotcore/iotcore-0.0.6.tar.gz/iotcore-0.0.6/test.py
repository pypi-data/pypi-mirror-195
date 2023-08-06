import iotcore


iotcore.mqtt_sample(
    server = "mqtt.eclipseprojects.io",
    sub_topic = "sub/iotcore",
    pub_topic = "pub/iotcore",
    port = 1883
)

iotcore.mqtt_sample