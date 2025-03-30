use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use std::f32::consts::PI;
use std::sync::{Arc, Mutex};
use std::time::Duration;

fn main() {
    // Seleccionar el dispositivo de salida de audio predeterminado
    let host = cpal::default_host();
    let device = host.default_output_device().expect("No se encontró un dispositivo de salida");

    // Obtener el formato de salida predeterminado
    let config = device.default_output_config().expect("No se pudo obtener el formato de salida predeterminado");
    let sample_rate = config.sample_rate().0 as f32;

    // Frecuencia base (ejemplo: "A4" es 440 Hz)
    let frequency = 440.0;

    // Estado compartido para controlar la frecuencia y la reproducción de la onda
    let amplitude = Arc::new(Mutex::new(0.0)); // Controla la amplitud para encender/apagar el sonido
    let freq_control = Arc::new(Mutex::new(frequency));

    // Crear el stream de audio
    let amplitude_clone = Arc::clone(&amplitude);
    let freq_control_clone = Arc::clone(&freq_control);
    let stream = device.build_output_stream(
        &config.into(),
        move |data: &mut [f32], _: &cpal::OutputCallbackInfo| {
            let amp = *amplitude_clone.lock().unwrap();
            let freq = *freq_control_clone.lock().unwrap();
            let mut sample_clock = 0f32;
            for sample in data.iter_mut() {
                *sample = amp * (2.0 * PI * freq * sample_clock / sample_rate).sin();
                sample_clock = (sample_clock + 1.0) % sample_rate;
            }
        },
        |err| eprintln!("Error en el stream de audio: {}", err),
        Some(Duration::from_millis(10)), // Aquí se especifica la duración del timeout
    ).expect("Error al construir el stream");

    // Iniciar el stream de audio
    stream.play().expect("No se pudo iniciar el stream de audio");

    // Escuchar el teclado y cambiar la frecuencia o encender/apagar la nota
    loop {
        println!("Presiona una tecla para cambiar la frecuencia (ejemplo: 'z' para Do3, 'x' para Re3, etc.), 'q' para salir:");

        let mut input = String::new();
        std::io::stdin().read_line(&mut input).expect("Error al leer entrada");
        let input = input.trim();

        // Mapear algunas teclas a frecuencias de piano
        let new_frequency = match input {
            "z" => 261.63, // Do3
            "x" => 293.66, // Re3
            "c" => 329.63, // Mi3
            "v" => 349.23, // Fa3
            "b" => 392.00, // Sol3
            "n" => 440.00, // La3
            "m" => 493.88, // Si3
            "a" => 523.25, // Do4
            " " => { // Espacio para activar/desactivar el sonido
                let mut amp = amplitude.lock().unwrap();
                if *amp > 0.0 {
                    *amp = 0.0; // Apagar el sonido
                } else {
                    *amp = 0.2; // Encender el sonido
                }
                continue;
            },
            "q" => break, // Salir
            _ => continue,
        };

        // Actualizar la frecuencia de la nota
        {
            let mut freq = freq_control.lock().unwrap();
            *freq = new_frequency;
        }
    }
}
