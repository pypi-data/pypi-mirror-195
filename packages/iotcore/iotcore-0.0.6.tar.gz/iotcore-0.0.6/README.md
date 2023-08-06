# iot-core

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