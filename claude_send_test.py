#!/usr/bin/env python3
"""
Claude Send Method Test Script
Simple test to find the working send mechanism for Claude interface
Tests: Type character → Try different send methods → Observe results
"""

import pyautogui
import time

# Disable failsafe
pyautogui.FAILSAFE = False

# Claude coordinates (your tested coordinates)
CLAUDE_CLICK = (1138, 907)

def test_send_method(method_name, send_function):
    """Test a specific send method"""
    print(f"\n🧪 Testing: {method_name}")
    print("=" * 40)
    
    # Click to focus Claude
    print("🎯 Clicking Claude interface...")
    pyautogui.click(CLAUDE_CLICK[0], CLAUDE_CLICK[1])
    time.sleep(0.5)
    
    # Focus input with Shift+X
    print("📥 Focusing inbox with Shift+X...")
    pyautogui.hotkey('shift', 'x')
    time.sleep(0.5)
    
    # Type test character
    test_char = f"Test-{method_name}"
    print(f"⌨️  Typing: {test_char}")
    pyautogui.typewrite(test_char)
    time.sleep(0.5)
    
    # Try the send method
    print(f"📤 Attempting send with: {method_name}")
    send_function()
    
    # Wait and check
    print("⏳ Waiting 2 seconds to observe result...")
    time.sleep(2)
    print(f"✅ {method_name} test complete")
    print("👀 Did the message send? Check Claude interface!")
    
    # Wait for user to observe
    input("Press Enter to continue to next test...")

def main():
    print("🔧 CLAUDE SEND METHOD TESTER")
    print("=" * 50)
    print("This script will test different send methods for Claude")
    print("Watch your Claude interface to see which method works!")
    print("\nMake sure Claude interface is visible...")
    input("Press Enter when ready to start tests...")
    
    # Test Method 1: Simple Enter
    test_send_method("Simple Enter", lambda: pyautogui.press('enter'))
    
    # Test Method 2: Double Enter
    test_send_method("Double Enter", lambda: (
        pyautogui.press('enter'),
        time.sleep(0.2),
        pyautogui.press('enter')
    ))
    
    # Test Method 3: Shift+Enter
    test_send_method("Shift+Enter", lambda: pyautogui.hotkey('shift', 'enter'))
    
    # Test Method 4: Command+Enter
    test_send_method("Command+Enter", lambda: pyautogui.hotkey('command', 'enter'))
    
    # Test Method 5: Tab then Space
    test_send_method("Tab then Space", lambda: (
        pyautogui.press('tab'),
        time.sleep(0.3),
        pyautogui.press('space')
    ))
    
    # Test Method 6: Tab then Enter
    test_send_method("Tab then Enter", lambda: (
        pyautogui.press('tab'),
        time.sleep(0.3),
        pyautogui.press('enter')
    ))
    
    # Test Method 7: Return key
    test_send_method("Return Key", lambda: pyautogui.press('return'))
    
    # Test Method 8: Long wait then Enter
    test_send_method("Long Wait + Enter", lambda: (
        time.sleep(1.0),
        pyautogui.press('enter')
    ))
    
    print("\n🎉 ALL TESTS COMPLETE!")
    print("=" * 50)
    print("Which method worked for sending in Claude?")
    print("That's the one we'll use in Waypoint 3!")

if __name__ == "__main__":
    main()