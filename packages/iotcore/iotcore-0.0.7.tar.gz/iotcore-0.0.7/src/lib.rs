use pyo3::prelude::*;
use rumqttc::{MqttOptions, Client, QoS};
use std::time::Duration;
use std::{thread};


#[pyfunction]
fn hello() -> PyResult<String> {
    Ok(("Hello world").to_string())
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
pub fn mqtt_sample(server: String, sub_topic: String, pub_topic: String, port: u16) -> PyResult<String> {
    let mut mqttoptions = MqttOptions::new("rumqtt-sync", server, port);
    mqttoptions.set_keep_alive(Duration::from_secs(5));
    
    let (mut client, mut connection) = Client::new(mqttoptions, 10);
    client.subscribe(sub_topic, QoS::AtMostOnce).unwrap();
    thread::spawn(move || for i in 0..10 {
       client.publish(pub_topic.to_string(), QoS::AtLeastOnce, false, vec![i; i as usize]).unwrap();
       thread::sleep(Duration::from_millis(1000));
    });
    
    // Iterate to poll the eventloop for connection progress
    for (i, notification) in connection.iter().enumerate() {
        println!("Notification = {:?}", notification);
    }

    Ok(("ok").to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn _iotcore(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(hello, m)?)?;
    m.add_function(wrap_pyfunction!(mqtt_sample, m)?)?;
    Ok(())
}