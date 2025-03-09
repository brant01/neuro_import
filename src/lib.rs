use pyo3::prelude::*;
use intan_importer::{self, load};
use std::collections::HashMap;
use std::path::Path;

#[pyclass]
struct RHSResult {
    #[pyo3(get)]
    data_present: bool,
    #[pyo3(get)]
    frequency_parameters: HashMap<String, f32>,
    #[pyo3(get)]
    notes: HashMap<String, String>,
    #[pyo3(get)]
    reference_channel: String,
    #[pyo3(get)]
    stim_parameters: HashMap<String, f32>,
    #[pyo3(get)]
    amplifier_channels: Vec<HashMap<String, String>>,
    #[pyo3(get)]
    board_adc_channels: Vec<HashMap<String, String>>,
    #[pyo3(get)]
    board_dac_channels: Vec<HashMap<String, String>>,
    #[pyo3(get)]
    board_dig_in_channels: Vec<HashMap<String, String>>,
    #[pyo3(get)]
    board_dig_out_channels: Vec<HashMap<String, String>>,
    #[pyo3(get)]
    t: Vec<f32>,
    #[pyo3(get)]
    amplifier_data: Option<Vec<Vec<f32>>>,
    #[pyo3(get)]
    dc_amplifier_data: Option<Vec<Vec<f32>>>,
    #[pyo3(get)]
    stim_data: Option<Vec<Vec<f32>>>,
    #[pyo3(get)]
    compliance_limit_data: Option<Vec<Vec<bool>>>,
    #[pyo3(get)]
    charge_recovery_data: Option<Vec<Vec<bool>>>,
    #[pyo3(get)]
    amp_settle_data: Option<Vec<Vec<bool>>>,
    #[pyo3(get)]
    board_adc_data: Option<Vec<Vec<f32>>>,
    #[pyo3(get)]
    board_dac_data: Option<Vec<Vec<f32>>>,
    #[pyo3(get)]
    board_dig_in_data: Option<Vec<Vec<bool>>>,
    #[pyo3(get)]
    board_dig_out_data: Option<Vec<Vec<bool>>>,
    #[pyo3(get)]
    spike_triggers: Vec<HashMap<String, f32>>,
}

/// Load an Intan RHS file using the Rust-based implementation.
/// 
/// This function provides a high-performance implementation for reading and parsing
/// Intan RHS files, using the intan_importer Rust crate.
#[pyfunction]
fn load_rhs_file(_py: Python<'_>, filename: &str) -> PyResult<RHSResult> {
    // Check if file exists
    if !Path::new(filename).exists() {
        return Err(pyo3::exceptions::PyFileNotFoundError::new_err(
            format!("File not found: {}", filename),
        ));
    }

    // Load file using intan_importer crate
    let rhs_file = match load(filename) {
        Ok(file) => file,
        Err(e) => {
            return Err(pyo3::exceptions::PyIOError::new_err(
                format!("Error loading RHS file: {}", e),
            ));
        }
    };

    // Extract header and data from the loaded file
    let header = &rhs_file.header;
    let data_present = rhs_file.data_present;
    
    // Convert header and data to Python objects
    let mut result = RHSResult {
        data_present,
        frequency_parameters: convert_frequency_parameters(header),
        notes: convert_notes(header),
        reference_channel: header.reference_channel.clone(),
        stim_parameters: convert_stim_parameters(header),
        amplifier_channels: convert_amplifier_channels(header),
        board_adc_channels: convert_board_adc_channels(header),
        board_dac_channels: convert_board_dac_channels(header),
        board_dig_in_channels: convert_board_dig_in_channels(header),
        board_dig_out_channels: convert_board_dig_out_channels(header),
        t: Vec::new(), // Will be populated if data is present
        amplifier_data: None,
        dc_amplifier_data: None,
        stim_data: None,
        compliance_limit_data: None,
        charge_recovery_data: None,
        amp_settle_data: None,
        board_adc_data: None,
        board_dac_data: None,
        board_dig_in_data: None,
        board_dig_out_data: None,
        spike_triggers: convert_spike_triggers(header),
    };

    // Process data if present
    if data_present {
        let data = rhs_file.data.as_ref().unwrap();
        
        // Convert timestamps to seconds
        result.t = data.timestamps.iter()
            .map(|&t| t as f32 / header.sample_rate)
            .collect();
            
        // Process and convert other data types
        result.amplifier_data = Some(convert_amplifier_data(data));
        
        if header.dc_amplifier_data_saved {
            result.dc_amplifier_data = Some(convert_dc_amplifier_data(data));
        }
        
        // Convert stimulation data
        let stim_conversion = convert_stim_data(data);
        result.stim_data = Some(stim_conversion.stim_data);
        result.compliance_limit_data = Some(stim_conversion.compliance_limit_data);
        result.charge_recovery_data = Some(stim_conversion.charge_recovery_data);
        result.amp_settle_data = Some(stim_conversion.amp_settle_data);
        
        // Convert board data
        result.board_adc_data = Some(convert_board_adc_data(data));
        result.board_dac_data = Some(convert_board_dac_data(data));
        result.board_dig_in_data = Some(convert_board_dig_in_raw(data, header));
        result.board_dig_out_data = Some(convert_board_dig_out_raw(data, header));
    }

    Ok(result)
}

// Helper functions for converting Rust data structures to Python equivalents
fn convert_frequency_parameters(header: &intan_importer::RhsHeader) -> HashMap<String, f32> {
    let mut freq_params = HashMap::new();
    
    freq_params.insert("amplifier_sample_rate".to_string(), header.sample_rate);
    freq_params.insert("board_adc_sample_rate".to_string(), header.sample_rate);
    freq_params.insert("board_dig_in_sample_rate".to_string(), header.sample_rate);
    
    freq_params.insert("desired_dsp_cutoff_frequency".to_string(), header.desired_dsp_cutoff_frequency);
    freq_params.insert("actual_dsp_cutoff_frequency".to_string(), header.actual_dsp_cutoff_frequency);
    freq_params.insert("dsp_enabled".to_string(), header.dsp_enabled as f32);
    
    freq_params.insert("desired_lower_bandwidth".to_string(), header.desired_lower_bandwidth);
    freq_params.insert("actual_lower_bandwidth".to_string(), header.actual_lower_bandwidth);
    
    freq_params.insert("desired_lower_settle_bandwidth".to_string(), header.desired_lower_settle_bandwidth);
    freq_params.insert("actual_lower_settle_bandwidth".to_string(), header.actual_lower_settle_bandwidth);
    
    freq_params.insert("desired_upper_bandwidth".to_string(), header.desired_upper_bandwidth);
    freq_params.insert("actual_upper_bandwidth".to_string(), header.actual_upper_bandwidth);
    
    if let Some(nf) = header.notch_filter_frequency {
        freq_params.insert("notch_filter_frequency".to_string(), nf as f32);
    } else {
        freq_params.insert("notch_filter_frequency".to_string(), 0.0);
    }
    
    freq_params.insert("desired_impedance_test_frequency".to_string(), header.desired_impedance_test_frequency);
    freq_params.insert("actual_impedance_test_frequency".to_string(), header.actual_impedance_test_frequency);
    
    freq_params
}

fn convert_notes(header: &intan_importer::RhsHeader) -> HashMap<String, String> {
    let mut notes = HashMap::new();
    notes.insert("note1".to_string(), header.notes.note1.clone());
    notes.insert("note2".to_string(), header.notes.note2.clone());
    notes.insert("note3".to_string(), header.notes.note3.clone());
    notes
}

fn convert_stim_parameters(header: &intan_importer::RhsHeader) -> HashMap<String, f32> {
    let mut stim_params = HashMap::new();
    stim_params.insert("stim_step_size".to_string(), header.stim_step_size);
    stim_params.insert("charge_recovery_current_limit".to_string(), header.recovery_current_limit);
    stim_params.insert("charge_recovery_target_voltage".to_string(), header.recovery_target_voltage);
    stim_params.insert("amp_settle_mode".to_string(), header.amp_settle_mode as f32);
    stim_params.insert("charge_recovery_mode".to_string(), header.charge_recovery_mode as f32);
    stim_params
}

fn convert_amplifier_channels(header: &intan_importer::RhsHeader) -> Vec<HashMap<String, String>> {
    let mut channels = Vec::new();
    
    for channel in &header.amplifier_channels {
        let mut channel_dict = HashMap::new();
        channel_dict.insert("native_channel_name".to_string(), channel.native_channel_name.clone());
        channel_dict.insert("custom_channel_name".to_string(), channel.custom_channel_name.clone());
        channel_dict.insert("native_order".to_string(), channel.native_order.to_string());
        channel_dict.insert("custom_order".to_string(), channel.custom_order.to_string());
        channel_dict.insert("chip_channel".to_string(), channel.chip_channel.to_string());
        channel_dict.insert("board_stream".to_string(), channel.board_stream.to_string());
        channel_dict.insert("electrode_impedance_magnitude".to_string(), channel.electrode_impedance_magnitude.to_string());
        channel_dict.insert("electrode_impedance_phase".to_string(), channel.electrode_impedance_phase.to_string());
        
        // Add port information
        channel_dict.insert("port_name".to_string(), channel.port_name.clone());
        channel_dict.insert("port_prefix".to_string(), channel.port_prefix.clone());
        channel_dict.insert("port_number".to_string(), channel.port_number.to_string());
        
        channels.push(channel_dict);
    }
    
    channels
}

fn convert_board_adc_channels(header: &intan_importer::RhsHeader) -> Vec<HashMap<String, String>> {
    let mut channels = Vec::new();
    
    for channel in &header.board_adc_channels {
        let mut channel_dict = HashMap::new();
        channel_dict.insert("native_channel_name".to_string(), channel.native_channel_name.clone());
        channel_dict.insert("custom_channel_name".to_string(), channel.custom_channel_name.clone());
        channel_dict.insert("native_order".to_string(), channel.native_order.to_string());
        channel_dict.insert("custom_order".to_string(), channel.custom_order.to_string());
        channel_dict.insert("board_stream".to_string(), channel.board_stream.to_string());
        
        // Add port information
        channel_dict.insert("port_name".to_string(), channel.port_name.clone());
        channel_dict.insert("port_prefix".to_string(), channel.port_prefix.clone());
        channel_dict.insert("port_number".to_string(), channel.port_number.to_string());
        
        channels.push(channel_dict);
    }
    
    channels
}

fn convert_board_dac_channels(header: &intan_importer::RhsHeader) -> Vec<HashMap<String, String>> {
    let mut channels = Vec::new();
    
    for channel in &header.board_dac_channels {
        let mut channel_dict = HashMap::new();
        channel_dict.insert("native_channel_name".to_string(), channel.native_channel_name.clone());
        channel_dict.insert("custom_channel_name".to_string(), channel.custom_channel_name.clone());
        channel_dict.insert("native_order".to_string(), channel.native_order.to_string());
        channel_dict.insert("custom_order".to_string(), channel.custom_order.to_string());
        channel_dict.insert("board_stream".to_string(), channel.board_stream.to_string());
        
        // Add port information
        channel_dict.insert("port_name".to_string(), channel.port_name.clone());
        channel_dict.insert("port_prefix".to_string(), channel.port_prefix.clone());
        channel_dict.insert("port_number".to_string(), channel.port_number.to_string());
        
        channels.push(channel_dict);
    }
    
    channels
}

fn convert_board_dig_in_channels(header: &intan_importer::RhsHeader) -> Vec<HashMap<String, String>> {
    let mut channels = Vec::new();
    
    for channel in &header.board_dig_in_channels {
        let mut channel_dict = HashMap::new();
        channel_dict.insert("native_channel_name".to_string(), channel.native_channel_name.clone());
        channel_dict.insert("custom_channel_name".to_string(), channel.custom_channel_name.clone());
        channel_dict.insert("native_order".to_string(), channel.native_order.to_string());
        channel_dict.insert("custom_order".to_string(), channel.custom_order.to_string());
        channel_dict.insert("board_stream".to_string(), channel.board_stream.to_string());
        
        // Add port information
        channel_dict.insert("port_name".to_string(), channel.port_name.clone());
        channel_dict.insert("port_prefix".to_string(), channel.port_prefix.clone());
        channel_dict.insert("port_number".to_string(), channel.port_number.to_string());
        
        channels.push(channel_dict);
    }
    
    channels
}

fn convert_board_dig_out_channels(header: &intan_importer::RhsHeader) -> Vec<HashMap<String, String>> {
    let mut channels = Vec::new();
    
    for channel in &header.board_dig_out_channels {
        let mut channel_dict = HashMap::new();
        channel_dict.insert("native_channel_name".to_string(), channel.native_channel_name.clone());
        channel_dict.insert("custom_channel_name".to_string(), channel.custom_channel_name.clone());
        channel_dict.insert("native_order".to_string(), channel.native_order.to_string());
        channel_dict.insert("custom_order".to_string(), channel.custom_order.to_string());
        channel_dict.insert("board_stream".to_string(), channel.board_stream.to_string());
        
        // Add port information
        channel_dict.insert("port_name".to_string(), channel.port_name.clone());
        channel_dict.insert("port_prefix".to_string(), channel.port_prefix.clone());
        channel_dict.insert("port_number".to_string(), channel.port_number.to_string());
        
        channels.push(channel_dict);
    }
    
    channels
}

fn convert_spike_triggers(header: &intan_importer::RhsHeader) -> Vec<HashMap<String, f32>> {
    let mut triggers = Vec::new();
    
    for trigger in &header.spike_triggers {
        let mut trigger_dict = HashMap::new();
        trigger_dict.insert("voltage_trigger_mode".to_string(), trigger.voltage_trigger_mode as f32);
        trigger_dict.insert("voltage_threshold".to_string(), trigger.voltage_threshold as f32);
        trigger_dict.insert("digital_trigger_channel".to_string(), trigger.digital_trigger_channel as f32);
        trigger_dict.insert("digital_edge_polarity".to_string(), trigger.digital_edge_polarity as f32);
        
        triggers.push(trigger_dict);
    }
    
    triggers
}

struct StimDataConversion {
    stim_data: Vec<Vec<f32>>,
    compliance_limit_data: Vec<Vec<bool>>,
    charge_recovery_data: Vec<Vec<bool>>,
    amp_settle_data: Vec<Vec<bool>>,
}

fn convert_amplifier_data(data: &intan_importer::RhsData) -> Vec<Vec<f32>> {
    if let Some(ref amp_data) = data.amplifier_data {
        let num_channels = amp_data.shape()[0];
        let num_samples = amp_data.shape()[1];
        
        let mut result = vec![vec![0.0; num_samples]; num_channels];
        
        for i in 0..num_channels {
            for j in 0..num_samples {
                // Scale to microvolts: 0.195 * (sample - 32768)
                let sample = amp_data[[i, j]];
                result[i][j] = 0.195 * (sample as i32 - 32768) as f32;
            }
        }
        
        result
    } else {
        Vec::new()
    }
}

fn convert_dc_amplifier_data(data: &intan_importer::RhsData) -> Vec<Vec<f32>> {
    if let Some(ref dc_amp_data) = data.dc_amplifier_data {
        let num_channels = dc_amp_data.shape()[0];
        let num_samples = dc_amp_data.shape()[1];
        
        let mut result = vec![vec![0.0; num_samples]; num_channels];
        
        for i in 0..num_channels {
            for j in 0..num_samples {
                // Scale to volts: -0.01923 * (sample - 512)
                let sample = dc_amp_data[[i, j]];
                result[i][j] = -0.01923 * (sample as i32 - 512) as f32;
            }
        }
        
        result
    } else {
        Vec::new()
    }
}

fn convert_stim_data(data: &intan_importer::RhsData) -> StimDataConversion {
    if let Some(ref stim_data_arr) = data.stim_data {
        let num_channels = stim_data_arr.shape()[0];
        let num_samples = stim_data_arr.shape()[1];
        
        let mut stim_data = vec![vec![0.0; num_samples]; num_channels];
        let mut compliance_limit_data = vec![vec![false; num_samples]; num_channels];
        let mut charge_recovery_data = vec![vec![false; num_samples]; num_channels];
        let mut amp_settle_data = vec![vec![false; num_samples]; num_channels];
        
        for i in 0..num_channels {
            for j in 0..num_samples {
                let sample = stim_data_arr[[i, j]];
                
                // Extract compliance limit bit (bit 15)
                compliance_limit_data[i][j] = (sample & 0x8000) != 0;
                
                // Extract charge recovery bit (bit 14)
                charge_recovery_data[i][j] = (sample & 0x4000) != 0;
                
                // Extract amp settle bit (bit 13)
                amp_settle_data[i][j] = (sample & 0x2000) != 0;
                
                // Extract polarity bit (bit 8)
                let polarity = if (sample & 0x0100) != 0 { -1i32 } else { 1i32 };
                
                // Extract current amplitude (bits 0-7)
                let current_amp = (sample & 0x00FF) as i32;
                
                // Combine polarity and amplitude
                stim_data[i][j] = (current_amp * polarity) as f32;
            }
        }
        
        StimDataConversion {
            stim_data,
            compliance_limit_data,
            charge_recovery_data,
            amp_settle_data,
        }
    } else {
        StimDataConversion {
            stim_data: Vec::new(),
            compliance_limit_data: Vec::new(),
            charge_recovery_data: Vec::new(),
            amp_settle_data: Vec::new(),
        }
    }
}

fn convert_board_adc_data(data: &intan_importer::RhsData) -> Vec<Vec<f32>> {
    if let Some(ref adc_data) = data.board_adc_data {
        let num_channels = adc_data.shape()[0];
        let num_samples = adc_data.shape()[1];
        
        if num_channels == 0 {
            return Vec::new();
        }
        
        let mut result = vec![vec![0.0; num_samples]; num_channels];
        
        for i in 0..num_channels {
            for j in 0..num_samples {
                // Scale to volts: 312.5e-6 * (sample - 32768)
                let sample = adc_data[[i, j]];
                result[i][j] = 312.5e-6 * (sample as i32 - 32768) as f32;
            }
        }
        
        result
    } else {
        Vec::new()
    }
}

fn convert_board_dac_data(data: &intan_importer::RhsData) -> Vec<Vec<f32>> {
    if let Some(ref dac_data) = data.board_dac_data {
        let num_channels = dac_data.shape()[0];
        let num_samples = dac_data.shape()[1];
        
        if num_channels == 0 {
            return Vec::new();
        }
        
        let mut result = vec![vec![0.0; num_samples]; num_channels];
        
        for i in 0..num_channels {
            for j in 0..num_samples {
                // Scale to volts: 312.5e-6 * (sample - 32768)
                let sample = dac_data[[i, j]];
                result[i][j] = 312.5e-6 * (sample as i32 - 32768) as f32;
            }
        }
        
        result
    } else {
        Vec::new()
    }
}

fn convert_board_dig_in_raw(data: &intan_importer::RhsData, header: &intan_importer::RhsHeader) -> Vec<Vec<bool>> {
    let num_channels = header.board_dig_in_channels.len();
    if num_channels == 0 {
        return Vec::new();
    }
    
    if let Some(ref dig_in_raw) = data.board_dig_in_raw {
        let num_samples = dig_in_raw.len();
        if num_samples == 0 {
            return Vec::new();
        }
        
        let mut result = vec![vec![false; num_samples]; num_channels];
        
        for i in 0..num_channels {
            let native_order = header.board_dig_in_channels[i].native_order;
            
            for j in 0..num_samples {
                let sample = dig_in_raw[j];
                result[i][j] = (sample & (1 << native_order)) != 0;
            }
        }
        
        result
    } else {
        Vec::new()
    }
}

fn convert_board_dig_out_raw(data: &intan_importer::RhsData, header: &intan_importer::RhsHeader) -> Vec<Vec<bool>> {
    let num_channels = header.board_dig_out_channels.len();
    if num_channels == 0 {
        return Vec::new();
    }
    
    if let Some(ref dig_out_raw) = data.board_dig_out_raw {
        let num_samples = dig_out_raw.len();
        if num_samples == 0 {
            return Vec::new();
        }
        
        let mut result = vec![vec![false; num_samples]; num_channels];
        
        for i in 0..num_channels {
            let native_order = header.board_dig_out_channels[i].native_order;
            
            for j in 0..num_samples {
                let sample = dig_out_raw[j];
                result[i][j] = (sample & (1 << native_order)) != 0;
            }
        }
        
        result
    } else {
        Vec::new()
    }
}

/// Register the Python module
#[pymodule]
fn neuro_import(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_rhs_file, py)?)?;
    m.add_class::<RHSResult>()?;
    
    Ok(())
}