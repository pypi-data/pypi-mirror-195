# iot-core

## Demo
```
import iotcore

iotcore.mqtt_sample(
    server = "mqtt.eclipseprojects.io",
    sub_topic = "sub/iotcore",
    pub_topic = "pub/iotcore",
    port = 1883
)
```

## Develop

```
pip3 install -r requirements.txt
maturin develop
maturin sdist
twine upload target/wheels/*
```

## Release

Update `version` in `Cargo.toml`

```
maturin sdist
twine upload target/wheels/*
```