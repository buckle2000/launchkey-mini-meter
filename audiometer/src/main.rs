extern crate libpulse_binding as pulse;
extern crate libpulse_simple_binding as psimple;

use psimple::Simple;
use pulse::sample;
use pulse::stream::Direction;

fn report<T>(error: pulse::error::PAErr) -> Result<T, ()> {
    panic!(format!("{}", error.to_string().unwrap()));
}

const CHANNEL_COUNT: usize = 2;
const BUFFER_LEN: usize = 1024;

fn main() {
    let spec = sample::Spec {
        format: sample::SAMPLE_FLOAT32,
        channels: CHANNEL_COUNT as u8,
        rate: 44100,
    };
    assert!(spec.is_valid());

    let mut buffer = [0u8; BUFFER_LEN];

    let s = Simple::new(
        None,                                                       // Use the default server
        "FooApp",                                                   // Our application’s name
        Direction::Record,                                          // We want a record stream
        Some("alsa_output.pci-0000_00_1b.0.analog-stereo.monitor"), // Use the default device
        "Music",                                                    // Description of our stream
        &spec,                                                      // Our sample format
        None,                                                       // Use default channel map
        None,
    )
    .or_else(report)
    .unwrap();

    loop {
        s.read(&mut buffer).or_else(report).unwrap();
        let buffer: [f32; BUFFER_LEN / 4] = unsafe { std::mem::transmute(buffer) };
        let mut levels = [0.0; CHANNEL_COUNT];
        for channel in 0..2 {
            for sample_idx in 0..buffer.len() / CHANNEL_COUNT {
                let sample = buffer[sample_idx * CHANNEL_COUNT + channel];
                if sample > levels[channel] {
                    levels[channel] = sample;
                }
            }
        }
        println!("{:.2} {:.2}", levels[0], levels[1]);
    }
}
