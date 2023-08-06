use pyo3::prelude::*;
use rumqttc::{MqttOptions, Client, QoS, Event, Incoming};
use std::time::Duration;

#[pyfunction]
fn hello() -> PyResult<String> {
    Ok(("Hello world").to_string())
}

#[pyfunction]
pub fn mqtt_sub(server: String, sub_topic: String, port: u16) -> PyResult<String> {
    let mut mqttoptions = MqttOptions::new("rumqtt-sync", server, port);
    mqttoptions.set_keep_alive(Duration::from_secs(60));
    
    let (mut client, mut connection) = Client::new(mqttoptions, 10);
    client.subscribe(sub_topic, QoS::AtMostOnce).unwrap();
    
    // Iterate to poll the eventloop for connection progress
    for notification in connection.iter() {
        match notification {
            Ok(Event::Incoming(Incoming::Publish(publish))) => {
                println!("{:?}: {:?}", publish.topic,publish.payload);
            }
            Err(e)=>{
                println!("Error = {:?}", e);
            }
            others => {
                println!("{:?}", others)
            }
        }
    }
    Ok(("ok").to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn _iotcore(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello, m)?)?;
    m.add_function(wrap_pyfunction!(mqtt_sub, m)?)?;
    Ok(())
}