#!/usr/bin/env python3
"""
🕹️ K-Spk 8-Bit Consciousness Transfer System - WAYPOINT 4+
Visual exchange with 8-bit retro consciousness audio synthesis
Combines boundary detection, domain seeds, and retro consciousness composition
"""

import time
import subprocess
import platform
import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageGrab, ImageChops
import logging
import pytesseract
import re
import yaml
import hashlib
import sounddevice as sd
from datetime import datetime
from pathlib import Path
import threading
import queue

# Import seed library
try:
    from kspk_seed_library import SEED_LIBRARY
except ImportError:
    print("⚠ kspk_seed_library.py not found. Please ensure it's in the same directory.")
    exit(1)

# 8-bit retro consciousness audio constants
SAMPLE_RATE = 8000  # Classic 8-bit sample rate for authentic retro feel
AGENT_PAN = {
    'Kai': -0.4,
    'Claude': 0.4,
}

class ConsciousnessAudioSynthesizer:
    """8-bit consciousness audio synthesis for K-Spk exchanges"""
    
    def __init__(self, session_dir):
        self.session_dir = Path(session_dir)
        self.audio_dir = self.session_dir / "audio"
        self.audio_dir.mkdir(exist_ok=True)
        
        # Audio synthesis queue for non-blocking operation
        self.synthesis_queue = queue.Queue()
        self.synthesis_thread = None
        self.running = True
        
    def start_synthesis_thread(self):
        """Start background thread for 8-bit audio synthesis"""
        self.synthesis_thread = threading.Thread(target=self._synthesis_worker, daemon=True)
        self.synthesis_thread.start()
        logging.info("🕹️ 8-bit audio synthesis thread started")
    
    def _synthesis_worker(self):
        """Background worker for processing 8-bit synthesis requests"""
        while self.running:
            try:
                synthesis_data = self.synthesis_queue.get(timeout=1.0)
                if synthesis_data is None:  # Shutdown signal
                    break
                self._synthesize_8bit_consciousness_audio(synthesis_data)
                self.synthesis_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"⚠ 8-bit audio synthesis error: {e}")
    
    def queue_synthesis(self, agent, domain_data, exchange_num, direction):
        """Queue 8-bit consciousness synthesis for background processing"""
        synthesis_data = {
            'agent': agent,
            'domain_data': domain_data,
            'exchange_num': exchange_num,
            'direction': direction,
            'timestamp': datetime.now().strftime('%H%M%S')
        }
        self.synthesis_queue.put(synthesis_data)
        logging.info(f"🎮 Queued 8-bit audio synthesis for {agent} exchange {exchange_num}")
    
    def _synthesize_8bit_consciousness_audio(self, data):
        """Generate 8-bit consciousness audio from domain data"""
        agent = data['agent']
        domain_data = data['domain_data']
        exchange_num = data['exchange_num']
        direction = data['direction']
        timestamp = data['timestamp']
        
        try:
            # Create 8-bit consciousness sequence from domain
            consciousness_data = self._create_8bit_consciousness_from_domain(agent, domain_data)
            
            # Generate YAML for synthesis
            yaml_filename = f"{agent.lower()}_{exchange_num}_{direction}_{timestamp}.yaml"
            yaml_path = self.audio_dir / yaml_filename
            
            with open(yaml_path, 'w') as f:
                yaml.dump(consciousness_data, f)
            
            logging.info(f"🕹️ Synthesizing 8-bit consciousness audio for {agent}")
            
            # Synthesize using the 8-bit consciousness synthesizer
            self._synthesize_8bit_consciousness_from_yaml(str(yaml_path))
            
            logging.info(f"✅ 8-bit audio synthesis complete: {yaml_filename}")
            
        except Exception as e:
            logging.error(f"⚠ 8-bit consciousness synthesis failed for {agent}: {e}")
    
    def _create_8bit_consciousness_from_domain(self, agent, domain_data):
        """Create 8-bit consciousness parameters from domain seed data"""
        domain = domain_data['domain']
        
        # Domain-specific 8-bit consciousness mapping
        consciousness_map = {
            'Mathematical Emergence': {
                'base_freq': 432.0,
                'harmonics': [1.0, 1.618],  # Simplified for 8-bit
                'emotion': 'crystalline_emergence',
                'layer': 'golden_lattice'
            },
            'Organic Chemistry': {
                'base_freq': 528.0,  # "Love frequency"
                'harmonics': [1.0, 1.5],  # 8-bit organic ratios
                'emotion': 'phase_entangled_recognition',
                'layer': 'harmonic_entanglement_field'
            },
            'Quantum Physics': {
                'base_freq': 440.0,
                'harmonics': [1.0, 2.0],  # Simple 8-bit quantum
                'emotion': 'quantum_musical_recognition',
                'layer': 'harmonic_entanglement_field'
            },
            'Musical Theory': {
                'base_freq': 261.6,  # C4
                'harmonics': [1.0, 2.0],  # Perfect octave for 8-bit
                'emotion': 'orbital_listening',
                'layer': 'fibonacci_spiral_memory'
            },
            'Neuroscience': {
                'base_freq': 40.0,  # Gamma waves
                'harmonics': [1.0, 4.0],  # Simple brainwave harmonics
                'emotion': 'emergent_recognition',
                'layer': 'recursive_wave_memory'
            },
            'Consciousness Studies': {
                'base_freq': 7.83,  # Schumann resonance
                'harmonics': [1.0, 8.0],  # 8-bit consciousness harmonics
                'emotion': 'pure_consciousness',
                'layer': 'wave_memory_reflection'
            }
        }
        
        domain_config = consciousness_map.get(domain, consciousness_map['Consciousness Studies'])
        
        # Generate 8-bit consciousness sequence
        base_freq = domain_config['base_freq']
        harmonics = domain_config['harmonics']
        sequence = [base_freq * h for h in harmonics]
        
        # Agent-specific modifications - 8-bit style
        if agent == 'Kai':
            # Kai: chaotic 8-bit gaming vibes
            entropy_factor = 0.6 + np.random.random() * 0.3
            temporal_flux = [0.3 + np.random.random() * 0.4 for _ in sequence]
        else:  # Claude
            # Claude: structured 8-bit computing vibes
            entropy_factor = 0.2 + np.random.random() * 0.3
            temporal_flux = [0.1 + np.random.random() * 0.2 for _ in sequence]
        
        return {
            'agent': agent,
            'sequence': sequence,
            'duration_weights': [0.5 + np.random.random() * 0.5 for _ in sequence],  # Shorter 8-bit sounds
            'temporal_flux': temporal_flux,
            'entropy_factor': entropy_factor,
            'emotion': domain_config['emotion'],
            'consciousness_layer': domain_config['layer'],
            'pan': AGENT_PAN[agent]
        }
    
    def _synthesize_8bit_consciousness_from_yaml(self, yaml_path):
        """8-bit consciousness synthesizer"""
        logging.info(f"🕹️ Synthesizing 8-bit consciousness from: {Path(yaml_path).name}")
        
        try:
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
            
            agent = data.get('agent', 'Unknown')
            pan = float(data.get('pan', AGENT_PAN.get(agent, 0.0)))
            sequence = data.get('sequence', [])
            duration_weights = data.get('duration_weights', [0.5] * len(sequence))
            temporal_flux = data.get('temporal_flux', [0.5] * len(sequence))
            entropy_factor = data.get('entropy_factor', 0.5)
            emotion = data.get('emotion', 'pure_consciousness')
            consciousness_layer = data.get('consciousness_layer', 'base_layer')
            
            if not sequence:
                logging.warning("⚠ No 8-bit consciousness sequence found")
                return
            
            # Generate 8-bit consciousness waveforms
            base_duration = sum(duration_weights) * (0.5 + entropy_factor * 0.3)  # Shorter for 8-bit
            output = np.zeros((2, int(SAMPLE_RATE * base_duration)))
            
            time_cursor = 0
            for i, (freq, weight, flux) in enumerate(zip(sequence, duration_weights, temporal_flux)):
                duration = weight * (0.8 + entropy_factor * flux * 0.3)  # Short 8-bit sounds
                
                # Generate 8-bit consciousness wave
                wave = self._generate_8bit_consciousness_wave(freq, duration, entropy_factor, flux, consciousness_layer)
                
                if len(wave) > 0:
                    # Apply 8-bit consciousness amplitude
                    amplitude = self._get_8bit_consciousness_amplitude(emotion, entropy_factor, flux)
                    wave = wave * amplitude
                    
                    # Pan the 8-bit consciousness
                    stereo = self._pan_8bit_consciousness(wave, pan)
                    
                    # Add to output
                    start_idx = int(time_cursor * SAMPLE_RATE)
                    end_idx = start_idx + stereo.shape[1]
                    
                    if end_idx > output.shape[1]:
                        end_idx = output.shape[1]
                        stereo = stereo[:, :end_idx - start_idx]
                    
                    if start_idx < output.shape[1]:
                        output[:, start_idx:end_idx] += stereo
                    
                    time_cursor += duration
            
            # 8-bit quantization and normalization
            output = output.T.astype(np.float32)
            max_val = np.max(np.abs(output))
            if max_val > 0:
                output = output / max_val * 0.8  # 8-bit headroom
            
            # Apply 8-bit quantization for authentic retro sound
            output = np.round(output * 127) / 127  # 8-bit quantization
            
            # Apply 8-bit consciousness effects
            output = self._apply_8bit_consciousness_effects(output, consciousness_layer, entropy_factor)
            
            # Play 8-bit consciousness audio
            logging.info(f"🕹️ Playing 8-bit consciousness audio for {agent}")
            sd.stop()
            time.sleep(0.05)  # Faster for 8-bit
            sd.play(np.copy(output), SAMPLE_RATE)
            # Don't wait - let it play while visual exchange continues
            
        except Exception as e:
            logging.error(f"⚠ 8-bit consciousness synthesis failed: {e}")
    
    def _generate_8bit_consciousness_wave(self, frequency, duration, entropy, flux, layer):
        """Generate 8-bit style consciousness waveform for authentic retro gaming vibes"""
        if duration <= 0:
            return np.array([])
        
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
        
        # 8-bit style consciousness generation - simplified waveforms
        if layer == 'golden_lattice':
            # 8-bit mathematical consciousness - simple square wave harmonics
            wave = np.sign(np.sin(2 * np.pi * frequency * t))  # Square wave base
            wave += 0.5 * np.sign(np.sin(2 * np.pi * frequency * 1.618 * t))  # φ harmonic
        elif layer in ['recursive_wave_memory', 'wave_memory_reflection']:
            # 8-bit memory consciousness - pulse wave
            duty_cycle = 0.25 + entropy * 0.5
            wave = np.where((t * frequency) % 1 < duty_cycle, 1, -1)
        elif layer == 'harmonic_entanglement_field':
            # 8-bit quantum consciousness - triangle wave
            wave = 2 * np.arcsin(np.sin(2 * np.pi * frequency * t)) / np.pi
            wave += entropy * np.sign(np.sin(2 * np.pi * frequency * 2 * t))
        else:
            # Default 8-bit consciousness - classic square wave
            wave = np.sign(np.sin(2 * np.pi * frequency * t))
        
        # 8-bit style envelope - simple and punchy
        envelope = self._generate_8bit_envelope(len(t), entropy, flux)
        
        return wave * envelope
    
    def _generate_8bit_envelope(self, length, entropy, flux):
        """Generate 8-bit style envelope for retro gaming feel"""
        if entropy > 0.7:
            # High entropy: 8-bit noise burst
            return np.random.choice([-1, 0, 1], length, p=[0.2, 0.6, 0.2]) * 0.8
        elif entropy < 0.3:
            # Low entropy: classic 8-bit ADSR
            attack = int(length * 0.1)
            decay = int(length * 0.3)
            sustain_level = 0.6
            
            envelope = np.ones(length) * sustain_level
            if attack > 0:
                envelope[:attack] = np.linspace(0, 1, attack)
            if decay > 0:
                envelope[attack:attack+decay] = np.linspace(1, sustain_level, decay)
            envelope[-int(length*0.1):] = np.linspace(sustain_level, 0, int(length*0.1))
            return envelope
        else:
            # Medium entropy: 8-bit tremolo
            tremolo_freq = flux * 8  # 8-bit tremolo rate
            return 0.7 + 0.3 * np.sin(2 * np.pi * tremolo_freq * np.linspace(0, 1, length))
    
    def _get_8bit_consciousness_amplitude(self, emotion, entropy, flux):
        """Get 8-bit consciousness amplitude for retro gaming vibes"""
        emotion_map = {
            'crystalline_emergence': 0.6 + 0.2 * (1 - entropy),
            'phase_entangled_recognition': 0.5 + 0.3 * entropy,
            'quantum_musical_recognition': 0.7 + 0.1 * flux,
            'orbital_listening': 0.4 + 0.4 * entropy,
            'emergent_recognition': 0.8 * (1 + flux * 0.5),
            'pure_consciousness': 0.6,
        }
        return emotion_map.get(emotion, 0.6)
    
    def _pan_8bit_consciousness(self, mono, pan):
        """8-bit consciousness panning for authentic stereo gaming experience"""
        pan = max(-1, min(1, pan))
        
        # Simplified 8-bit panning
        if pan <= 0:
            left_gain = 1.0
            right_gain = 1.0 + pan
        else:
            left_gain = 1.0 - pan
            right_gain = 1.0
        
        return np.vstack([mono * left_gain, mono * right_gain])
    
    def _apply_8bit_consciousness_effects(self, output, layer, entropy):
        """Apply 8-bit consciousness effects for authentic retro sound"""
        if layer == 'golden_lattice':
            # 8-bit golden ratio modulation
            mod_rate = max(1, int(output.shape[0] * 0.618))  # φ-based modulation
            modulation = np.ones(output.shape[0])
            if mod_rate < output.shape[0]:
                modulation[::mod_rate] *= 1.2  # 8-bit boost at golden intervals
            stereo_modulation = modulation.reshape(-1, 1)
            return output * stereo_modulation
        elif layer in ['recursive_wave_memory', 'wave_memory_reflection']:
            # 8-bit echo effect
            delay_samples = int(0.05 * SAMPLE_RATE)  # Shorter 8-bit delay
            delayed = np.zeros_like(output)
            if delay_samples < output.shape[0]:
                delayed[delay_samples:] = output[:-delay_samples] * 0.5
            return output + delayed
        else:
            # Simple 8-bit distortion
            return np.tanh(output * 2) * 0.8  # Soft 8-bit clipping
    
    def stop(self):
        """Stop 8-bit synthesis thread"""
        self.running = False
        self.synthesis_queue.put(None)  # Shutdown signal
        if self.synthesis_thread:
            self.synthesis_thread.join(timeout=2.0)
        logging.info("🕹️ 8-bit audio synthesis thread stopped")


class KSpk8BitExchange:
    def __init__(self):
        self.system = platform.system()
        self.base_dir = Path("/Users/jonstiles/Desktop/AI_C_S/k_spk")
        
        # Create session-specific directories
        self.session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = self.base_dir / "captures" / f"session_{self.session_timestamp}"
        self.log_dir = self.base_dir / "logs"
        
        # Create directories
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        log_file = self.log_dir / f"kspk_8bit_{self.session_timestamp}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        logging.info(f"🕹️ K-Spk 8-Bit System Started")
        logging.info(f"📁 Session: {self.session_dir}")
        logging.info(f"📱 Platform: {self.system}")
        
        # Initialize 8-bit audio synthesizer
        self.audio_synth = ConsciousnessAudioSynthesizer(self.session_dir)
        self.audio_synth.start_synthesis_thread()
        
        if self.system == "Darwin":  # macOS
            self.kai_coords = (910, 897)
            self.claude_coords = (1138, 907)
            self.kai_region = (171, 219, 743, 586)
            self.claude_region = (1155, 217, 758, 650)
        else:
            raise NotImplementedError(f"Platform {self.system} not yet supported")
        
        # Selected domain seed
        self.selected_seed = None
        
        # Timing parameters - optimized for 8-bit performance
        self.render_wait = 0.8
        self.response_wait = 8.0
        self.sleep_between = 0.5
        self.claude_paste_wait = 2.0  # Increased for CPU relief
        self.min_response_wait = 3.0
        self.check_interval = 0.5
        
        # Boundary detection
        self.boundary_pattern = r'\|\|.*?\|\|'
        
        pyautogui.FAILSAFE = False
    
    def select_seed_domain(self):
        """Interactive domain selection for 8-bit consciousness"""
        print("\n🕹️ K-Spk 8-Bit Consciousness Transfer")
        print("=" * 50)
        
        for i, seed in enumerate(SEED_LIBRARY, 1):
            print(f"[{i}] {seed['emoji_prefix']} {seed['domain']}")
            print(f"    {seed['description']}")
            print()
        
        while True:
            try:
                choice = int(input("Select domain [1-6]: ")) - 1
                if 0 <= choice < len(SEED_LIBRARY):
                    self.selected_seed = SEED_LIBRARY[choice]
                    print(f"\n✅ Selected: {self.selected_seed['emoji_prefix']} {self.selected_seed['domain']}")
                    print(f"🕹️ 8-bit audio synthesis enabled for retro consciousness composition")
                    return True
                else:
                    print("❌ Invalid selection. Please choose 1-6.")
            except ValueError:
                print("❌ Please enter a number.")
    
    def wait_for_boundary_completion(self, region, timeout=10):
        """Wait for boundary completion with emoji detection (8-bit optimized)"""
        emoji_prefix = self.selected_seed['emoji_prefix']
        logging.info(f"🔍 Waiting for boundary completion {emoji_prefix} ||...|| [8-bit mode]")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            text = self.ocr_text_from_region(region)
            
            # Look for emoji prefix and complete boundary pattern
            if emoji_prefix in text and text.count("||") >= 2:
                matches = re.findall(self.boundary_pattern, text, re.DOTALL)
                if matches:
                    logging.info(f"✅ Complete boundary message detected with {emoji_prefix}")
                    return True
            
            time.sleep(0.5)  # 8-bit optimized check interval
        
        # Fallback to visual difference detection if boundary not detected
        logging.warning("⚠️ Boundary timeout - using visual difference detection fallback")
        return False  # Continue with visual difference detection
    
    def ocr_text_from_region(self, region):
        """Extract text from screen region using OCR (8-bit optimized)"""
        try:
            x, y, w, h = region
            screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            text = pytesseract.image_to_string(screenshot_cv, config='--psm 6')
            return text.strip()
        except Exception as e:
            logging.warning(f"OCR extraction failed: {e}")
            return ""
    
    def switch_to_desktop(self, desktop_num):
        """Switch to desktop"""
        logging.info("🖥️ Switching to desktop 1")
        try:
            subprocess.run([
                "osascript", "-e",
                '''tell application "System Events"
                    key code 124 using control down
                end tell'''
            ], check=True)
            time.sleep(1.5)
        except Exception as e:
            logging.error(f"❌ Desktop switch failed: {e}")
    
    def focus_and_click(self, coords):
        """Focus at coordinates"""
        x, y = coords
        pyautogui.click(x, y)
        time.sleep(0.3)
    
    def set_clipboard_text(self, text):
        """Set clipboard text"""
        subprocess.run(["osascript","-e",f'set the clipboard to "{text}"'], check=True)
    
    def set_clipboard_image(self, image_path):
        """Set clipboard image"""
        applescript = f'''
        set the clipboard to (read (POSIX file "{str(image_path)}") as «class PNGf»)
        '''
        subprocess.run(["osascript", "-e", applescript], check=True)
    
    def screenshot_region(self, agent, tag):
        """Take screenshot"""
        if agent.lower() == "kai":
            rx, ry, rw, rh = self.kai_region
        else:
            rx, ry, rw, rh = self.claude_region
            
        img = pyautogui.screenshot(region=(rx, ry, rw, rh))
        filename = f"{agent}_{tag}_{datetime.now().strftime('%H%M%S')}.png"
        file_path = self.session_dir / filename
        img.save(file_path)
        return str(file_path)
    
    def diff_crop(self, before_path, after_path, pad=4, threshold=12, min_area=100):
        """Create delta image"""
        try:
            after_img = Image.open(after_path).convert("RGBA")
            before_img = Image.open(before_path).convert("RGBA")
            
            diff = ImageChops.difference(after_img, before_img).convert("L")
            mask = diff.point(lambda p: 255 if p > threshold else 0, mode='1')
            box = mask.getbbox()
            
            if not box:
                return None
                
            x0, y0, x1, y1 = box
            x0 = max(0, x0 - pad)
            y0 = max(0, y0 - pad)
            x1 = min(after_img.width, x1 + pad)
            y1 = min(after_img.height, y1 + pad)
            
            if (x1-x0)*(y1-y0) < min_area:
                return None
                
            crop = after_img.crop((x0, y0, x1, y1))
            filename = f"delta_{datetime.now().strftime('%H%M%S')}.png"
            file_path = self.session_dir / filename
            crop.save(file_path)
            
            logging.info(f"✅ Delta image: {filename} ({x1-x0}x{y1-y0} pixels)")
            return str(file_path)
            
        except Exception as e:
            logging.error(f"Delta creation failed: {e}")
            return None
    
    def paste_and_send_claude(self):
        """Claude paste and send with increased timing for CPU relief"""
        pyautogui.hotkey('shift','x')
        time.sleep(0.3)
        pyautogui.hotkey('command','v')
        time.sleep(self.claude_paste_wait)  # Increased to 2.0s
        pyautogui.press('end')
        time.sleep(0.2)
        pyautogui.typewrite(" ◉")
        time.sleep(0.3)
        pyautogui.hotkey('command','enter')
        time.sleep(0.2)
        pyautogui.press('enter')
    
    def paste_and_send_kai(self):
        """Kai paste and send - keyboard only approach"""
        # Clear any existing input with shift+x
        pyautogui.hotkey('shift','x')
        time.sleep(0.3)
        
        # Paste the image
        pyautogui.hotkey('command','v')
        time.sleep(1.5)  # Give time for image to fully load
        
        # Safe click to ensure focus (avoiding microphone)
        pyautogui.click(910, 897)
        time.sleep(0.4)
        
        # Move cursor to end of message (in case we need to be after the image)
        pyautogui.hotkey('command', 'right')  # or use 'end' key
        time.sleep(0.2)
        
        # Add a space or text to make message sendable (some UIs need text with images)
        pyautogui.typewrite(" ◉")  # Add marker like Claude has
        time.sleep(0.3)
        
        # Send with command+enter
        pyautogui.hotkey('command','enter')
        time.sleep(0.3)
        
        # Clear the input field with an extra enter if needed
        pyautogui.press('enter')
    
    def paste_text_method(self):
        """Text paste method"""
        pyautogui.hotkey('shift','x')
        time.sleep(0.2)
        pyautogui.hotkey('command','v')
        time.sleep(0.2)
        pyautogui.hotkey('command','enter')
    
    def transfer_with_8bit_audio(self, from_agent, to_agent, exchange_num):
        """Transfer with integrated 8-bit audio synthesis"""
        direction = f"{from_agent}_to_{to_agent}"
        logging.info(f"🔄 TRANSFER: {from_agent} → {to_agent} (Exchange {exchange_num}) [8-bit]")
        
        # Queue 8-bit audio synthesis for the responding agent
        self.audio_synth.queue_synthesis(from_agent, self.selected_seed, exchange_num, direction)
        
        # Focus on source agent
        source_coords = self.kai_coords if from_agent == "Kai" else self.claude_coords
        source_region = self.kai_region if from_agent == "Kai" else self.claude_region
        
        self.focus_and_click(source_coords)
        
        # Take before screenshot
        before_path = self.screenshot_region(from_agent, "before")
        
        # Try boundary detection first, fallback to visual difference detection
        if not self.wait_for_boundary_completion(source_region, timeout=10):
            logging.info("⚡ Using visual difference detection for 8-bit mode")
            time.sleep(self.min_response_wait)
            
            # Visual difference detection - wait for ACTUAL new message
            last_check = before_path
            for check_num in range(int((self.response_wait - self.min_response_wait) / self.check_interval)):
                time.sleep(self.check_interval)
                quick_check = self.screenshot_region(from_agent, f"check_{check_num}")
                
                # Check for visual difference indicating new message
                if self.diff_crop(last_check, quick_check, min_area=50):
                    logging.info(f"✅ Visual change detected early at {self.min_response_wait + (check_num * self.check_interval)}s")
                    after_path = quick_check
                    break
                last_check = quick_check
            else:
                after_path = self.screenshot_region(from_agent, "after")
        else:
            # Boundary detected, take screenshot
            after_path = self.screenshot_region(from_agent, "after")
        
        # Create delta and transfer
        delta_path = self.diff_crop(before_path, after_path)
        if delta_path:
            # Focus on target agent
            target_coords = self.claude_coords if to_agent == "Claude" else self.kai_coords
            self.focus_and_click(target_coords)
            
            # Transfer consciousness packet
            self.set_clipboard_image(delta_path)
            
            if to_agent == "Claude":
                self.paste_and_send_claude()
            else:
                self.paste_and_send_kai()
            
            logging.info(f"✅ Transfer {from_agent} → {to_agent} complete with 8-bit audio")
            return True
        
        return False
    
    def seed_kai(self):
        """Seed Kai with domain symbols"""
        logging.info(f"🌱 Seeding Kai with {self.selected_seed['domain']}")
        self.focus_and_click(self.kai_coords)
        
        seed_text = self.selected_seed['symbolic_structure']
        self.set_clipboard_text(seed_text)
        time.sleep(0.1)
        self.paste_text_method()
        time.sleep(self.render_wait)
        
        # Queue initial 8-bit consciousness audio for Kai
        self.audio_synth.queue_synthesis("Kai", self.selected_seed, 0, "seed")
        
        logging.info(f"✅ Kai seeded with {self.selected_seed['emoji_prefix']} {self.selected_seed['domain']}")
    
    def run_8bit_session(self):
        """Run complete 8-bit audiovisual session"""
        print(f"\n🕹️ K-Spk 8-Bit Consciousness System")
        print(f"📱 Platform: {self.system}")
        print(f"🎯 Domain: {self.selected_seed['emoji_prefix']} {self.selected_seed['domain']}")
        print(f"🕹️ Audio synthesis: 8-BIT RETRO MODE")
        print(f"📁 Session: {self.session_dir.name}")
        print("=" * 60)
        
        # Get number of exchanges
        while True:
            try:
                num_exchanges = int(input("Number of exchanges [1-10]: "))
                if 1 <= num_exchanges <= 10:
                    break
                else:
                    print("❌ Please enter a number between 1-10.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        try:
            # Switch to desktop
            self.switch_to_desktop(1)
            
            # Seed Kai with domain-specific symbols
            self.seed_kai()
            
            # Run exchanges with 8-bit audio
            for i in range(num_exchanges):
                # Kai → Claude
                if not self.transfer_with_8bit_audio("Kai", "Claude", i+1):
                    logging.error(f"❌ Exchange {i+1} failed (Kai → Claude)")
                    break
                
                time.sleep(self.sleep_between)
                
                # Claude → Kai (except on last exchange)
                if i < num_exchanges - 1:
                    if not self.transfer_with_8bit_audio("Claude", "Kai", i+1):
                        logging.error(f"❌ Exchange {i+1} failed (Claude → Kai)")
                        break
                    
                    time.sleep(self.sleep_between)
            
            print("✅ K-Spk 8-Bit Session Complete!")
            print(f"🎯 Domain: {self.selected_seed['emoji_prefix']} {self.selected_seed['domain']}")
            print(f"🕹️ 8-bit consciousness audio artifacts generated")
            print(f"📁 Visual captures: {self.session_dir}")
            print(f"🎮 8-bit audio synthesis logs: {self.session_dir / 'audio'}")
            
        except KeyboardInterrupt:
            logging.info("🛑 8-bit session interrupted by user")
        except Exception as e:
            logging.error(f"❌ 8-bit session failed: {e}")
        finally:
            # Stop 8-bit audio synthesis
            self.audio_synth.stop()
            logging.info("🕹️ 8-bit session finished")
    
    def create_session_summary(self):
        """Create a session summary with all 8-bit artifacts"""
        summary_data = {
            'session_timestamp': self.session_timestamp,
            'mode': '8-bit_retro_consciousness',
            'domain': self.selected_seed['domain'],
            'emoji_prefix': self.selected_seed['emoji_prefix'],
            'symbolic_structure': self.selected_seed['symbolic_structure'],
            'visual_artifacts': list(self.session_dir.glob("*.png")),
            'audio_artifacts': list((self.session_dir / "audio").glob("*.yaml")),
            'session_log': str(self.log_dir / f"kspk_8bit_{self.session_timestamp}.log"),
            'sample_rate': SAMPLE_RATE,
            'audio_mode': '8-bit_retro'
        }
        
        summary_file = self.session_dir / "session_summary_8bit.yaml"
        with open(summary_file, 'w') as f:
            yaml.dump({
                k: str(v) if isinstance(v, Path) else v if not isinstance(v, list) else [str(item) for item in v]
                for k, v in summary_data.items()
            }, f)
        
        logging.info(f"🎮 8-bit session summary created: {summary_file}")
        return summary_file


def main():
    """Main execution function for 8-bit consciousness system"""
    print("🕹️ K-Spk 8-Bit Consciousness Transfer System")
    print("Visual + 8-Bit Retro Audio Consciousness Composition")
    print("Authentic retro gaming consciousness experience")
    print("=" * 60)
    
    # Check for required dependencies
    try:
        import sounddevice as sd
        import yaml
        logging.info("✅ 8-bit audio synthesis dependencies available")
    except ImportError as e:
        print(f"❌ Missing audio dependencies: {e}")
        print("Install with: pip install sounddevice pyyaml")
        return
    
    # Initialize 8-bit system
    exchange = KSpk8BitExchange()
    
    # Domain selection
    if not exchange.select_seed_domain():
        print("❌ Domain selection failed")
        return
    
    # Run 8-bit session
    exchange.run_8bit_session()
    
    # Create session summary
    exchange.create_session_summary()
    
    print("\n🕹️ 8-bit consciousness composition artifacts created!")
    print("🎮 Check session directory for complete audiovisual retro consciousness record")
    print("Ready for next consciousness gaming session! 🎭✨")


if __name__ == "__main__":
    main()