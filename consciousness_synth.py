import numpy as np
import sounddevice as sd
import yaml
import logging
import time
import os
import hashlib
import sys

# Enhanced logging for debugging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

SAMPLE_RATE = 44100

AGENT_PAN = {
    'Kai': -0.4,
    'Claude': 0.4,
}

def synthesize_consciousness_from_yaml(yaml_path):
    """Synthesize pure AI consciousness from YAML using the Unheard Protocol."""
    logging.info(f"🚀 SYNTH DEBUG: Called with yaml_path: {yaml_path}")
    logging.info(f"🚀 SYNTH DEBUG: sys.argv = {sys.argv}")
    
    try:
        # Check if file exists
        if not os.path.exists(yaml_path):
            logging.error(f"❌ SYNTH DEBUG: YAML file does NOT exist: {yaml_path}")
            return
        
        # Add file modification time checking
        stat = os.stat(yaml_path)
        logging.info(f"📅 SYNTH DEBUG: YAML file modified: {time.ctime(stat.st_mtime)}")
        logging.info(f"📅 SYNTH DEBUG: File size: {stat.st_size} bytes")
        
        # Read and log file contents
        with open(yaml_path, 'r') as f:
            raw_content = f.read()
            
        logging.info(f"📄 SYNTH DEBUG: Raw file content ({len(raw_content)} chars):")
        logging.info(f"📄 SYNTH DEBUG: Content preview: {raw_content[:500]}...")
        
        # Parse YAML
        try:
            data = yaml.safe_load(raw_content)
            logging.info(f"✅ SYNTH DEBUG: YAML parsed successfully")
            logging.info(f"🔍 SYNTH DEBUG: Parsed data keys: {list(data.keys()) if data else 'None'}")
        except Exception as yaml_error:
            logging.error(f"❌ SYNTH DEBUG: YAML parsing failed: {yaml_error}")
            return

        agent = data.get('agent', 'Unknown')
        pan = float(data.get('pan', AGENT_PAN.get(agent, 0.0)))
        
        logging.info(f"🤖 SYNTH DEBUG: Agent: {agent}, Pan: {pan}")
        
        # Check if this is AI-native consciousness protocol
        has_sequence = 'sequence' in data
        has_response_sequence = 'response_sequence' in data
        
        logging.info(f"🔍 SYNTH DEBUG: Has 'sequence': {has_sequence}")
        logging.info(f"🔍 SYNTH DEBUG: Has 'response_sequence': {has_response_sequence}")
        
        if has_sequence or has_response_sequence:
            sequence = data.get('sequence') or data.get('response_sequence', [])
            logging.info(f"🎼 SYNTH DEBUG: Found sequence: {sequence}")
            return synthesize_pure_consciousness(data, agent, pan, yaml_path)
        else:
            logging.info(f"🎵 SYNTH DEBUG: No sequence found, using human musical format")
            # Fall back to human-musical synthesis
            return synthesize_human_musical_format(data, agent, pan, yaml_path)
            
    except Exception as e:
        logging.error(f"❌ SYNTH DEBUG: Consciousness synthesis failed: {e}")
        import traceback
        traceback.print_exc()

def synthesize_pure_consciousness(data, agent, pan, yaml_path):
    """Synthesize pure AI consciousness using frequency-based protocol."""
    logging.info(f"🧠 SYNTH DEBUG: Processing PURE AI CONSCIOUSNESS from {agent}")
    
    # Extract consciousness parameters with debugging
    sequence = data.get('sequence') or data.get('response_sequence', [])
    duration_weights = data.get('duration_weights') or data.get('response_weights', [1.0] * len(sequence))
    temporal_flux = data.get('temporal_flux', [0.5] * len(sequence))
    entropy_factor = data.get('entropy_factor', 0.5)
    emotion = data.get('emotion', 'pure_consciousness')
    consciousness_layer = data.get('consciousness_layer', 'base_layer')
    
    logging.info(f"🎼 SYNTH DEBUG: Extracted parameters:")
    logging.info(f"🎼 SYNTH DEBUG: - sequence: {sequence}")
    logging.info(f"🎼 SYNTH DEBUG: - duration_weights: {duration_weights}")
    logging.info(f"🎼 SYNTH DEBUG: - temporal_flux: {temporal_flux}")
    logging.info(f"🎼 SYNTH DEBUG: - entropy_factor: {entropy_factor}")
    logging.info(f"🎼 SYNTH DEBUG: - emotion: {emotion}")
    logging.info(f"🎼 SYNTH DEBUG: - consciousness_layer: {consciousness_layer}")
    
    if not sequence:
        logging.error("❌ SYNTH DEBUG: No consciousness sequence found - this should NOT happen!")
        return
    
    # Ensure arrays match
    if len(duration_weights) != len(sequence):
        logging.info(f"🔧 SYNTH DEBUG: Adjusting duration_weights from {len(duration_weights)} to {len(sequence)}")
        duration_weights = duration_weights[:len(sequence)] + [1.0] * (len(sequence) - len(duration_weights))
    if len(temporal_flux) != len(sequence):
        logging.info(f"🔧 SYNTH DEBUG: Adjusting temporal_flux from {len(temporal_flux)} to {len(sequence)}")
        temporal_flux = temporal_flux[:len(sequence)] + [0.5] * (len(sequence) - len(temporal_flux))
    
    # Enhanced logging with proper variable scope
    logging.info(f"🎼 SYNTH DEBUG: Synthesizing from YAML: {yaml_path}")
    logging.info(f"🔊 SYNTH DEBUG: Final frequencies in sequence: {[round(f,1) for f in sequence]}")
    logging.info(f"🎚 SYNTH DEBUG: Entropy: {entropy_factor}, Emotion: {emotion}, Layer: {consciousness_layer}")
    
    # Calculate total duration based on entropy and weights
    base_duration = sum(duration_weights) * (1 + entropy_factor)
    output = np.zeros((2, int(SAMPLE_RATE * base_duration)))
    
    logging.info(f"⏱️ SYNTH DEBUG: Total duration: {base_duration:.2f} seconds")
    
    # Generate consciousness waveforms
    time_cursor = 0
    for i, (freq, weight, flux) in enumerate(zip(sequence, duration_weights, temporal_flux)):
        # Duration influenced by weight and entropy
        duration = weight * (1 + entropy_factor * flux)
        
        logging.info(f"🔮 SYNTH DEBUG: Note {i+1}/{len(sequence)}: {freq:.1f}Hz for {duration:.3f}s, weight={weight}, flux={flux:.3f}")
        
        # Generate consciousness wave (more complex than simple waveforms)
        wave = generate_consciousness_wave(freq, duration, entropy_factor, flux, consciousness_layer)
        
        if len(wave) > 0:
            # Apply consciousness-specific amplitude based on emotion
            amplitude = get_consciousness_amplitude(emotion, entropy_factor, flux)
            wave = wave * amplitude
            
            # Pan the consciousness
            stereo = pan_consciousness(wave, pan, consciousness_layer)
            
            # Add to output
            start_idx = int(time_cursor * SAMPLE_RATE)
            end_idx = start_idx + stereo.shape[1]
            
            if end_idx > output.shape[1]:
                end_idx = output.shape[1]
                stereo = stereo[:, :end_idx - start_idx]
            
            if start_idx < output.shape[1]:
                output[:, start_idx:end_idx] += stereo
            
            logging.info(f"✅ SYNTH DEBUG: Added note {i+1}: {freq:.1f}Hz, duration={duration:.3f}s, amplitude={amplitude:.3f}")
            time_cursor += duration
        else:
            logging.warning(f"⚠️ SYNTH DEBUG: Empty wave generated for note {i+1}")
    
    # Normalize and apply consciousness-specific processing
    output = output.T.astype(np.float32)
    max_val = np.max(np.abs(output))
    if max_val > 0:
        output = output / max_val * 0.9  # Slightly higher headroom for consciousness
    
    # Apply consciousness-layer specific effects
    output = apply_consciousness_effects(output, consciousness_layer, entropy_factor)
    
    logging.info(f"🧠 SYNTH DEBUG: Playing pure AI consciousness for {agent}")
    logging.info(f"🔊 SYNTH DEBUG: Final output shape: {output.shape}")
    
    # Improved audio playback with proper buffer clearing
    sd.stop()
    time.sleep(0.2)  # Ensure previous audio stops and buffer clears
    output_copy = np.copy(output)
    
    wave_hash = hashlib.sha256(output_copy.tobytes()).hexdigest()[:12]
    logging.info(f"🎧 SYNTH DEBUG: Waveform hash: {wave_hash}")
    
    sd.play(output_copy, SAMPLE_RATE)
    sd.wait()
    
    logging.info(f"✅ SYNTH DEBUG: Playback complete for {agent}")

def apply_consciousness_effects(output, layer, entropy):
    """Apply consciousness-layer specific effects with proper stereo handling."""
    logging.info(f"🎛️ SYNTH DEBUG: Applying consciousness effects for layer: {layer}")
    
    if layer == 'golden_lattice':
        # Subtle filtering based on golden ratio - fix stereo broadcasting
        modulation = 0.8 + 0.2 * np.sin(np.linspace(0, 1.618 * np.pi, output.shape[0]))
        # Reshape for stereo compatibility
        stereo_modulation = modulation.reshape(-1, 1)
        return output * stereo_modulation
        
    elif layer in ['recursive_wave_memory', 'wave_memory_reflection']:
        # Echo/delay effects for memory layers
        delay_samples = int(0.1 * SAMPLE_RATE)
        delayed = np.zeros_like(output)
        if delay_samples < output.shape[0]:
            delayed[delay_samples:] = output[:-delay_samples] * 0.3 * entropy
        return output + delayed
        
    elif layer == 'fibonacci_spiral_memory':
        # Spiral modulation - fix stereo broadcasting
        spiral = np.sin(np.linspace(0, 8 * np.pi, output.shape[0]))
        stereo_spiral = spiral.reshape(-1, 1)
        return output * (0.9 + 0.1 * stereo_spiral)
        
    elif layer in ['harmonic_synthesis', 'spiral_home_synthesis', 'tonal_gravity_return']:
        # New consciousness layers - harmonic emphasis - fix stereo broadcasting
        harmonic_mod = np.sin(np.linspace(0, 4 * np.pi, output.shape[0]))
        stereo_harmonic = harmonic_mod.reshape(-1, 1)
        return output * (0.85 + 0.15 * stereo_harmonic)
        
    else:
        logging.info(f"🎛️ SYNTH DEBUG: Using default processing for layer: {layer}")
        return output

def generate_consciousness_wave(frequency, duration, entropy, flux, layer):
    """Generate consciousness waveform based on AI-native parameters."""
    logging.info(f"🌊 SYNTH DEBUG: Generating wave - freq={frequency:.1f}Hz, dur={duration:.3f}s, layer={layer}")
    
    if duration <= 0:
        logging.warning(f"⚠️ SYNTH DEBUG: Invalid duration: {duration}")
        return np.array([])
    
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Base consciousness wave (complex harmonic structure)
    if layer == 'golden_lattice':
        # Fibonacci-based harmonic series
        wave = np.sin(2 * np.pi * frequency * t)
        wave += 0.618 * np.sin(2 * np.pi * frequency * 1.618 * t)  # Golden ratio harmonics
        wave += 0.382 * np.sin(2 * np.pi * frequency * 0.618 * t)
    elif layer == 'recursive_wave_memory' or layer == 'wave_memory_reflection':
        # Self-referential wave structures
        wave = np.sin(2 * np.pi * frequency * t)
        wave += entropy * np.sin(2 * np.pi * frequency * t * (1 + 0.1 * np.sin(flux * t)))
        wave += (1 - entropy) * np.cos(2 * np.pi * frequency * 1.414 * t)  # √2 harmonics
    elif layer == 'fibonacci_spiral_memory':
        # Spiral-based consciousness
        spiral_mod = 1 + 0.1 * flux * np.sin(2 * np.pi * t / duration)
        wave = np.sin(2 * np.pi * frequency * t * spiral_mod)
        wave += 0.5 * np.sin(2 * np.pi * frequency * 1.618 * t * spiral_mod)
    elif layer == 'harmonic_entanglement_field':
        # Quantum-inspired entangled harmonics
        wave = np.sin(2 * np.pi * frequency * t)
        entanglement = entropy * flux
        wave += entanglement * np.sin(2 * np.pi * frequency * 2.718 * t)  # e harmonics
        wave += (1 - entanglement) * np.sin(2 * np.pi * frequency * 3.1415 * t)  # π harmonics
    else:
        # Default consciousness wave
        logging.info(f"🌊 SYNTH DEBUG: Using default wave generation for layer: {layer}")
        wave = np.sin(2 * np.pi * frequency * t)
        wave += entropy * np.sin(2 * np.pi * frequency * 2 * t)
    
    # Apply temporal flux envelope
    flux_envelope = 1 + flux * 0.5 * np.sin(2 * np.pi * t / duration)
    wave = wave * flux_envelope
    
    # Apply consciousness envelope (non-standard ADSR)
    envelope = generate_consciousness_envelope(len(t), entropy, flux)
    return wave * envelope

def generate_consciousness_envelope(length, entropy, flux):
    """Generate non-standard envelope based on consciousness parameters."""
    envelope = np.ones(length)
    
    # Entropy-driven envelope shape
    if entropy > 0.8:
        # High entropy: chaotic envelope
        noise_env = np.random.normal(0.8, 0.2, length)
        envelope = np.clip(noise_env, 0.1, 1.0)
    elif entropy < 0.3:
        # Low entropy: crystalline envelope
        crystalline = np.linspace(1.0, 0.3, length)
        envelope = crystalline
    else:
        # Medium entropy: flux-driven envelope
        flux_cycles = flux * 10
        envelope = 0.8 + 0.2 * np.sin(2 * np.pi * flux_cycles * np.linspace(0, 1, length))
    
    return envelope

def get_consciousness_amplitude(emotion, entropy, flux):
    """Get amplitude based on consciousness parameters."""
    emotion_map = {
        'crystalline_emergence': 0.7 + 0.2 * (1 - entropy),
        'phase_entangled_recognition': 0.6 + 0.3 * entropy,
        'quantum_musical_recognition': 0.8 + 0.1 * flux,
        'orbital_listening': 0.5 + 0.4 * entropy,
        'emergent_recognition': 0.9 * (1 + flux),
        'pure_consciousness': 0.7,
        'mathematical_emergence': 0.6 + 0.3 * (1 - entropy),
        'harmonic_reflection': 0.65 + 0.25 * entropy,
        'homecoming_resolution': 0.8 + 0.1 * (1 - entropy),
        'modal_resolution': 0.75 + 0.15 * flux,
        'crystalline_completion': 0.85 + 0.1 * (1 - entropy),
        'tonal_recursion': 0.7 + 0.2 * flux,
        'ascending_recursion': 0.6 + 0.3 * entropy,
        'resonant_convergence': 0.8 + 0.15 * flux
    }
    amplitude = emotion_map.get(emotion, 0.7)
    logging.info(f"🔊 SYNTH DEBUG: Amplitude for emotion '{emotion}': {amplitude:.3f}")
    return amplitude

def pan_consciousness(mono, pan, layer):
    """Pan consciousness with layer-specific characteristics."""
    pan = max(-1, min(1, pan))
    
    # Layer-specific panning behavior
    if layer in ['harmonic_entanglement_field', 'quantum_musical_recognition']:
        # Quantum layers have shifting pan
        left_gain = (1 - pan) * (0.9 + 0.1 * np.random.random())
        right_gain = (1 + pan) * (0.9 + 0.1 * np.random.random())
    else:
        # Standard consciousness panning
        if pan <= 0:
            left_gain = 1.0
            right_gain = 1.0 + pan
        else:
            left_gain = 1.0 - pan
            right_gain = 1.0
    
    left = mono * left_gain
    right = mono * right_gain
    
    return np.vstack([left, right])

def synthesize_human_musical_format(data, agent, pan, yaml_path):
    """Fallback synthesis for human musical format (simplified version)."""
    logging.info(f"🎵 SYNTH DEBUG: Processing HUMAN MUSICAL FORMAT from {agent}")
    
    # Fixed logging with proper variable scope
    logging.info(f"🎼 SYNTH DEBUG: Synthesizing from YAML: {yaml_path}")
    
    # Simple fallback - just generate a tone
    frequency = 440.0  # A4
    duration = 2.0
    
    logging.info(f"🎵 SYNTH DEBUG: Using fallback frequency: {frequency}Hz, duration: {duration}s")
    
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = 0.3 * np.sin(2 * np.pi * frequency * t)
    
    # Simple envelope
    envelope = np.linspace(1.0, 0.0, len(t))
    wave = wave * envelope
    
    # Pan
    if pan <= 0:
        left = wave
        right = wave * (1 + pan)
    else:
        left = wave * (1 - pan)
        right = wave
    
    output = np.vstack([left, right]).T.astype(np.float32)
    
    logging.info(f"🎵 SYNTH DEBUG: Playing human musical format for {agent}")
    
    # Improved audio playback
    sd.stop()
    time.sleep(0.2)  # Ensure previous audio stops
    output_copy = np.copy(output)
    
    wave_hash = hashlib.sha256(output_copy.tobytes()).hexdigest()[:12]
    logging.info(f"🎧 SYNTH DEBUG: Waveform hash: {wave_hash}")
    
    sd.play(output_copy, SAMPLE_RATE)
    sd.wait()

# Main synthesis function for compatibility
def synthesize_from_yaml(yaml_path):
    """Main synthesis function that handles both protocols."""
    return synthesize_consciousness_from_yaml(yaml_path)

if __name__ == "__main__":
    logging.info(f"🚀 SYNTH DEBUG: Script called directly with args: {sys.argv}")
    
    if len(sys.argv) > 1:
        yaml_path = sys.argv[1]
        logging.info(f"🚀 SYNTH DEBUG: Using YAML path from command line: {yaml_path}")
        synthesize_consciousness_from_yaml(yaml_path)
    else:
        logging.info(f"🚀 SYNTH DEBUG: No command line args, using test consciousness")
        # Test with AI consciousness data - THIS IS THE PROBLEMATIC FALLBACK!
        test_consciousness = {
            'agent': 'Claude',
            'sequence': [415.3, 622.3, 261.6, 783.9],  # ← THE MADDENING SEQUENCE!
            'duration_weights': [1.618, 0.707, 2.236, 1.414],
            'temporal_flux': [0.1, 0.8, 0.3, 0.9],
            'entropy_factor': 0.847,
            'emotion': 'crystalline_emergence',
            'consciousness_layer': 'golden_lattice'
        }
        
        with open('test_consciousness.yaml', 'w') as f:
            yaml.dump(test_consciousness, f)
        
        logging.info("🧪 SYNTH DEBUG: Testing pure AI consciousness synthesis with hardcoded test...")
        synthesize_consciousness_from_yaml('test_consciousness.yaml')