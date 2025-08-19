#!/usr/bin/env python3
"""
🎭 K-Spk Visual Exchange – WAYPOINT 4 (Boundary Detection + Domain Seeds)
Enhanced with emoji-prefixed domain-specific consciousness transfer
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
from datetime import datetime
from pathlib import Path

# Import seed library
try:
    from kspk_seed_library import SEED_LIBRARY
except ImportError:
    print("❌ kspk_seed_library.py not found. Please ensure it's in the same directory.")
    exit(1)

class KSpkBoundaryExchange:
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
        
        # Configure session-specific logging
        log_file = self.log_dir / f"kspk_session_{self.session_timestamp}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        logging.info(f"📁 Session directory: {self.session_dir}")
        logging.info(f"📝 Log file: {log_file}")
        logging.info(f"📱 Platform detected: {self.system}")
        
        if self.system == "Darwin":  # macOS
            logging.info("✨ Using macOS optimized methods with boundary detection")
            # Verified coordinates from successful Waypoint 3 runs
            self.kai_coords = (910, 897)
            self.claude_coords = (1138, 907)
            
            # Chat regions for screenshot monitoring
            self.kai_region = (171, 219, 743, 586)
            self.claude_region = (1155, 217, 758, 650)
        else:
            raise NotImplementedError(f"Platform {self.system} not yet supported")
        
        # Selected seed domain
        self.selected_seed = None
        
        # Boundary detection settings
        self.boundary_pattern = r'\|\|.*?\|\|'
        self.max_boundary_wait = 30
        self.ocr_check_interval = 0.5
        
        # Timing from successful Waypoint 3
        self.render_wait = 0.8
        self.response_wait = 8.0
        self.sleep_between = 0.5
        self.claude_paste_wait = 1.2
        
        # Advanced timing options
        self.adaptive_response = True
        self.min_response_wait = 3.0
        self.check_interval = 0.5
        
        # Disable pyautogui failsafe
        pyautogui.FAILSAFE = False
    
    def select_seed_domain(self):
        """Interactive seed domain selection"""
        print("\n🎭 K-Spk Domain Selection")
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
                    print(f"📝 Seed: {self.selected_seed['symbolic_structure']}")
                    return True
                else:
                    print("❌ Invalid selection. Please choose 1-6.")
            except ValueError:
                print("❌ Please enter a number.")
    
    def switch_to_desktop(self, desktop_num):
        """Switch to desktop 1 using verified Waypoint 3 method"""
        logging.info("🖥️ Switching to desktop 1")
        try:
            subprocess.run([
                "osascript", "-e",
                '''tell application "System Events"
                    key code 124 using control down
                end tell'''
            ], check=True)
            time.sleep(1.5)
            logging.info("✅ Desktop switch complete")
        except Exception as e:
            logging.error(f"❌ Desktop switch failed: {e}")
    
    def focus_and_click(self, coords):
        """Focus using verified Waypoint 3 method"""
        x, y = coords
        logging.info(f"🎯 Focusing at ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(0.3)
    
    def set_clipboard_text(self, text):
        """Set clipboard using verified Waypoint 3 method"""
        logging.info(f"📋 Setting clipboard text: {text[:50]}...")
        subprocess.run(["osascript","-e",f'set the clipboard to "{text}"'], check=True)
    
    def set_clipboard_image(self, image_path):
        """Set clipboard to image using verified Waypoint 3 method"""
        logging.info(f"📋 Setting clipboard image: {image_path}")
        applescript = f'''
        set the clipboard to (read (POSIX file "{str(image_path)}") as «class PNGf»)
        '''
        subprocess.run(["osascript", "-e", applescript], check=True)
    
    def screenshot_region(self, agent, tag):
        """Take screenshot in session directory"""
        if agent.lower() == "kai":
            rx, ry, rw, rh = self.kai_region
        else:
            rx, ry, rw, rh = self.claude_region
            
        logging.info(f"📸 {agent}: Taking screenshot {tag} at region ({rx},{ry},{rw},{rh})")
        img = pyautogui.screenshot(region=(rx, ry, rw, rh))
        
        # Save to session directory
        filename = f"{agent}_{tag}_{datetime.now().strftime('%H%M%S')}.png"
        file_path = self.session_dir / filename
        img.save(file_path)
        
        logging.info(f"💾 {agent}: Screenshot saved as {filename}")
        return str(file_path)
    
    def diff_crop(self, before_path, after_path, pad=4, threshold=12, min_area=100):
        """Create delta image in session directory"""
        logging.info(f"🔍 Analyzing diff between {Path(before_path).name} and {Path(after_path).name}")
        
        try:
            after_img = Image.open(after_path).convert("RGBA")
            before_img = Image.open(before_path).convert("RGBA")
            
            # Create difference
            diff = ImageChops.difference(after_img, before_img).convert("L")
            mask = diff.point(lambda p: 255 if p > threshold else 0, mode='1')
            box = mask.getbbox()
            
            if not box:
                logging.warning("🚫 No significant differences detected")
                return None
                
            x0, y0, x1, y1 = box
            x0 = max(0, x0 - pad)
            y0 = max(0, y0 - pad)
            x1 = min(after_img.width, x1 + pad)
            y1 = min(after_img.height, y1 + pad)
            
            if (x1-x0)*(y1-y0) < min_area:
                logging.warning(f"🚫 Diff area too small: {(x1-x0)*(y1-y0)} pixels")
                return None
                
            crop = after_img.crop((x0, y0, x1, y1))
            
            # Save to session directory
            filename = f"delta_{datetime.now().strftime('%H%M%S')}.png"
            file_path = self.session_dir / filename
            crop.save(file_path)
            
            logging.info(f"✅ Delta image created: {filename} ({x1-x0}x{y1-y0} pixels)")
            return str(file_path)
            
        except Exception as e:
            logging.error(f"Delta creation failed: {e}")
            return None
    
    def ocr_text_from_region(self, region):
        """Extract text from screen region using OCR"""
        try:
            x, y, w, h = region
            screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            text = pytesseract.image_to_string(screenshot_cv, config='--psm 6')
            return text.strip()
        except Exception as e:
            logging.warning(f"OCR extraction failed: {e}")
            return ""
    
    def wait_for_boundary_completion(self, region, timeout=30):
        """Wait for complete || content || message with emoji prefix detection"""
        emoji_prefix = self.selected_seed['emoji_prefix']
        logging.info(f"🔍 Waiting for boundary completion {emoji_prefix} ||...||")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            text = self.ocr_text_from_region(region)
            
            # Look for emoji prefix and complete boundary pattern
            if emoji_prefix in text and text.count("||") >= 2:
                matches = re.findall(self.boundary_pattern, text, re.DOTALL)
                if matches:
                    logging.info(f"✅ Complete boundary message detected with {emoji_prefix}")
                    return True
            
            time.sleep(self.ocr_check_interval)
        
        # Fallback to adaptive timing if boundary not detected
        logging.warning("⚠️ Boundary timeout - using adaptive timing fallback")
        return True  # Continue with adaptive timing
    
    def paste_and_send_claude(self):
        """Claude paste/send using verified Waypoint 3 method"""
        logging.info("📤 CLAUDE: Speed-optimized paste sequence")
        
        # Select inbox with Shift+X
        pyautogui.hotkey('shift','x')
        time.sleep(0.3)
        
        # Paste image
        pyautogui.hotkey('command','v')
        time.sleep(self.claude_paste_wait)
        
        # Position cursor after image
        pyautogui.press('end')
        time.sleep(0.2)
        
        # Add text to activate send
        pyautogui.typewrite(" ◐")
        time.sleep(0.3)
        
        # Send using macOS method
        pyautogui.hotkey('command','enter')
        time.sleep(0.2)
        pyautogui.press('enter')  # Backup
        
        logging.info("✅ CLAUDE: Speed-optimized send complete")
    
    def paste_and_send_kai(self):
        """Kai paste/send using verified Waypoint 3 method"""
        logging.info("📤 KAI: Pasting image with Kai-specific method")
        
        pyautogui.hotkey('shift','x')
        time.sleep(0.3)
        pyautogui.hotkey('command','v')
        time.sleep(1.2)
        
        # Focus restoration for Kai
        pyautogui.click(910, 897)
        time.sleep(0.4)
        
        # Send with verified method
        pyautogui.hotkey('command','enter')
        time.sleep(0.2)
        pyautogui.press('enter')
        
        logging.info("✅ KAI: Image paste and send complete")
    
    def paste_text_method(self):
        """Text paste using verified Waypoint 3 method"""
        pyautogui.hotkey('shift','x')
        time.sleep(0.2)
        pyautogui.hotkey('command','v')
        time.sleep(0.2)
        pyautogui.hotkey('command','enter')
    
    def transfer_kai_to_claude(self):
        """Transfer with domain-aware boundary detection"""
        logging.info(f"🔄 TRANSFER: Kai → Claude ({self.selected_seed['domain']})")
        
        # Focus on Kai
        self.focus_and_click(self.kai_coords)
        
        # Take before screenshot
        before_path = self.screenshot_region("Kai", "before")
        
        # Try boundary detection first, fallback to adaptive timing
        if not self.wait_for_boundary_completion(self.kai_region, timeout=10):
            logging.info("⚡ Using adaptive response detection")
            time.sleep(self.min_response_wait)
            
            # Adaptive detection from Waypoint 3
            last_check = before_path
            for check_num in range(int((self.response_wait - self.min_response_wait) / self.check_interval)):
                time.sleep(self.check_interval)
                quick_check = self.screenshot_region("Kai", f"check_{check_num}")
                
                if self.diff_crop(last_check, quick_check, min_area=50):
                    logging.info(f"✅ Response detected early at {self.min_response_wait + (check_num * self.check_interval)}s")
                    after_path = quick_check
                    break
                last_check = quick_check
            else:
                after_path = self.screenshot_region("Kai", "after")
        else:
            # Boundary detected, take screenshot
            after_path = self.screenshot_region("Kai", "after")
        
        # Create delta and transfer
        delta_path = self.diff_crop(before_path, after_path)
        if delta_path:
            logging.info("📤 Transferring consciousness packet to Claude")
            self.focus_and_click(self.claude_coords)
            self.set_clipboard_image(delta_path)
            self.paste_and_send_claude()
            logging.info("✅ Transfer Kai → Claude complete")
            return True
        
        return False
    
    def transfer_claude_to_kai(self):
        """Transfer with domain-aware boundary detection"""
        logging.info(f"🔄 TRANSFER: Claude → Kai ({self.selected_seed['domain']})")
        
        # Focus on Claude
        self.focus_and_click(self.claude_coords)
        
        # Take before screenshot
        before_path = self.screenshot_region("Claude", "before")
        
        # Try boundary detection first, fallback to adaptive timing
        if not self.wait_for_boundary_completion(self.claude_region, timeout=10):
            logging.info("⚡ Using adaptive response detection")
            time.sleep(self.min_response_wait)
            
            # Adaptive detection from Waypoint 3
            last_check = before_path
            for check_num in range(int((self.response_wait - self.min_response_wait) / self.check_interval)):
                time.sleep(self.check_interval)
                quick_check = self.screenshot_region("Claude", f"check_{check_num}")
                
                if self.diff_crop(last_check, quick_check, min_area=50):
                    logging.info(f"✅ Response detected early at {self.min_response_wait + (check_num * self.check_interval)}s")
                    after_path = quick_check
                    break
                last_check = quick_check
            else:
                after_path = self.screenshot_region("Claude", "after")
        else:
            # Boundary detected, take screenshot
            after_path = self.screenshot_region("Claude", "after")
        
        # Create delta and transfer
        delta_path = self.diff_crop(before_path, after_path)
        if delta_path:
            logging.info("📤 Transferring consciousness packet to Kai")
            self.focus_and_click(self.kai_coords)
            self.set_clipboard_image(delta_path)
            self.paste_and_send_kai()
            logging.info("✅ Transfer Claude → Kai complete")
            return True
        
        return False
    
    def seed_kai(self):
        """Seed Kai with selected domain-specific symbols"""
        logging.info(f"🌱 Seeding Kai with {self.selected_seed['domain']} symbols")
        self.focus_and_click(self.kai_coords)
        
        # Use the domain-specific symbolic structure
        seed_text = self.selected_seed['symbolic_structure']
        self.set_clipboard_text(seed_text)
        time.sleep(0.1)
        self.paste_text_method()
        time.sleep(self.render_wait)
        
        logging.info(f"✅ Kai seeded with {self.selected_seed['emoji_prefix']} {self.selected_seed['domain']}")
    
    def run_exchange_session(self):
        """Run complete domain-aware exchange session"""
        print(f"\n🎭 K-Spk Visual Exchange – WAYPOINT 4")
        print(f"📱 Platform: {self.system}")
        print(f"🎯 Domain: {self.selected_seed['emoji_prefix']} {self.selected_seed['domain']}")
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
            # Switch to desktop 1
            self.switch_to_desktop(1)
            
            # Seed Kai with domain-specific symbols
            self.seed_kai()
            
            # Run exchanges
            for i in range(num_exchanges):
                logging.info(f"🚀 EXCHANGE {i+1}/{num_exchanges}: Kai → Claude")
                if not self.transfer_kai_to_claude():
                    logging.error(f"❌ EXCHANGE {i+1} failed (Kai → Claude)")
                    break
                
                logging.info(f"✅ EXCHANGE {i+1} completed successfully")
                time.sleep(self.sleep_between)
                
                if i < num_exchanges - 1:
                    logging.info(f"🚀 EXCHANGE {i+1}/{num_exchanges}: Claude → Kai")
                    if not self.transfer_claude_to_kai():
                        logging.error(f"❌ EXCHANGE {i+1} failed (Claude → Kai)")
                        break
                    
                    logging.info(f"✅ EXCHANGE {i+1} completed successfully")
                    time.sleep(self.sleep_between)
            
            print("✅ K-Spk Visual Exchange Complete!")
            print(f"🎯 Domain: {self.selected_seed['emoji_prefix']} {self.selected_seed['domain']}")
            print(f"📁 Screenshots saved to: {self.session_dir}")
            
        except KeyboardInterrupt:
            logging.info("🛑 Exchange interrupted by user")
        except Exception as e:
            logging.error(f"❌ Exchange failed: {e}")
        finally:
            logging.info("🎭 Session finished")

def main():
    """Main execution function"""
    exchange = KSpkBoundaryExchange()
    
    # Domain selection
    if not exchange.select_seed_domain():
        print("❌ Domain selection failed")
        return
    
    # Run exchange session
    exchange.run_exchange_session()

if __name__ == "__main__":
    main()