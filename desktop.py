#!/usr/bin/env python3
"""
Desktop Control Skill | 桌面控制技能
OpenClaw Skill for Windows desktop automation
"""

import sys
import os
import json
import base64
import argparse
import time
from pathlib import Path

# Add Windows-specific check
if sys.platform != "win32":
    print(json.dumps({
        "error": "This skill only works on Windows",
        "platform": sys.platform
    }))
    sys.exit(1)

try:
    import pyautogui
    import mss
    from PIL import Image
    import numpy as np
    import cv2
except ImportError as e:
    print(json.dumps({
        "error": f"Missing dependency: {e}",
        "install": "pip install pyautogui mss pillow opencv-python numpy"
    }))
    sys.exit(1)

# Configure pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

# Set DPI aware
try:
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass


class DesktopController:
    """Desktop automation controller"""
    
    def screenshot(self, x=0, y=0, w=1920, h=1080, full=False, output=None):
        """Capture screen or region"""
        try:
            if full:
                size = pyautogui.size()
                w, h = size.width, size.height
            
            with mss.mss() as sct:
                mon = {"left": x, "top": y, "width": w, "height": h}
                raw = sct.grab(mon)
                img = Image.frombytes("RGB", raw.size, raw.rgb)
                
                # Convert to bytes
                import io
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                png_bytes = buf.getvalue()
                
                result = {
                    "success": True,
                    "size": {"width": w, "height": h},
                    "format": "png"
                }
                
                # Save to file if output specified
                if output:
                    with open(output, "wb") as f:
                        f.write(png_bytes)
                    result["saved_to"] = output
                
                # Return base64
                result["image_base64"] = base64.b64encode(png_bytes).decode()
                return result
                
        except Exception as e:
            return {"error": str(e)}
    
    def click(self, x, y, button="left", clicks=1):
        """Click at coordinates"""
        try:
            pyautogui.click(x=x, y=y, clicks=clicks, button=button)
            return {
                "success": True,
                "action": "click",
                "position": {"x": x, "y": y},
                "button": button,
                "clicks": clicks
            }
        except Exception as e:
            return {"error": str(e)}
    
    def type_text(self, text, interval=0.01):
        """Type text"""
        try:
            pyautogui.typewrite(text, interval=interval)
            return {
                "success": True,
                "action": "type",
                "text_length": len(text)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def keypress(self, key=None, hotkey=None):
        """Press key or hotkey"""
        try:
            if hotkey:
                keys = hotkey.split(",")
                pyautogui.hotkey(*keys)
                return {
                    "success": True,
                    "action": "hotkey",
                    "keys": keys
                }
            else:
                pyautogui.press(key)
                return {
                    "success": True,
                    "action": "keypress",
                    "key": key
                }
        except Exception as e:
            return {"error": str(e)}
    
    def scroll(self, clicks, x=None, y=None):
        """Scroll mouse wheel"""
        try:
            if x is not None and y is not None:
                pyautogui.moveTo(x, y)
                time.sleep(0.05)
            pyautogui.scroll(clicks)
            return {
                "success": True,
                "clicks": clicks,
                "position": {"x": x, "y": y} if x else None
            }
        except Exception as e:
            return {"error": str(e)}
    
    def move(self, x, y, duration=0.5):
        """Move mouse cursor"""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return {
                "success": True,
                "position": {"x": x, "y": y},
                "duration": duration
            }
        except Exception as e:
            return {"error": str(e)}
    
    def locate(self, image_path, confidence=0.9):
        """Find image on screen"""
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                return {
                    "success": True,
                    "found": True,
                    "position": {
                        "left": location.left,
                        "top": location.top,
                        "width": location.width,
                        "height": location.height,
                        "center_x": location.left + location.width // 2,
                        "center_y": location.top + location.height // 2
                    }
                }
            else:
                return {
                    "success": True,
                    "found": False
                }
        except Exception as e:
            return {"error": str(e)}
    
    def click_image(self, image_path, confidence=0.9):
        """Find and click image"""
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center_x = location.left + location.width // 2
                center_y = location.top + location.height // 2
                pyautogui.click(center_x, center_y)
                return {
                    "success": True,
                    "clicked": True,
                    "position": {"x": center_x, "y": center_y}
                }
            else:
                return {
                    "success": True,
                    "clicked": False,
                    "error": "Image not found"
                }
        except Exception as e:
            return {"error": str(e)}
    
    def screen_size(self):
        """Get screen dimensions"""
        try:
            size = pyautogui.size()
            return {
                "success": True,
                "width": size.width,
                "height": size.height
            }
        except Exception as e:
            return {"error": str(e)}
    
    def mouse_pos(self):
        """Get current mouse position"""
        try:
            pos = pyautogui.position()
            return {
                "success": True,
                "x": pos.x,
                "y": pos.y
            }
        except Exception as e:
            return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Desktop Control Skill")
    parser.add_argument("command", choices=[
        "screenshot", "click", "type", "keypress", "scroll",
        "move", "locate", "click_image", "screen_size", "mouse_pos"
    ])
    
    # Screenshot args
    parser.add_argument("--x", type=int, default=0)
    parser.add_argument("--y", type=int, default=0)
    parser.add_argument("--w", type=int, default=1920)
    parser.add_argument("--h", type=int, default=1080)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=str)
    
    # Click args
    parser.add_argument("--button", type=str, default="left")
    parser.add_argument("--clicks", type=int, default=1)
    
    # Type args
    parser.add_argument("--text", type=str)
    parser.add_argument("--interval", type=float, default=0.01)
    
    # Keypress args
    parser.add_argument("--key", type=str)
    parser.add_argument("--hotkey", type=str)
    
    # Image args
    parser.add_argument("--image", type=str)
    parser.add_argument("--confidence", type=float, default=0.9)
    
    # Move args
    parser.add_argument("--duration", type=float, default=0.5)
    
    args = parser.parse_args()
    
    controller = DesktopController()
    
    # Route command
    if args.command == "screenshot":
        result = controller.screenshot(
            args.x, args.y, args.w, args.h,
            full=args.full, output=args.output
        )
    elif args.command == "click":
        result = controller.click(args.x, args.y, args.button, args.clicks)
    elif args.command == "type":
        result = controller.type_text(args.text, args.interval)
    elif args.command == "keypress":
        result = controller.keypress(args.key, args.hotkey)
    elif args.command == "scroll":
        result = controller.scroll(args.clicks, args.x if args.x != 0 else None, args.y if args.y != 0 else None)
    elif args.command == "move":
        result = controller.move(args.x, args.y, args.duration)
    elif args.command == "locate":
        result = controller.locate(args.image, args.confidence)
    elif args.command == "click_image":
        result = controller.click_image(args.image, args.confidence)
    elif args.command == "screen_size":
        result = controller.screen_size()
    elif args.command == "mouse_pos":
        result = controller.mouse_pos()
    else:
        result = {"error": f"Unknown command: {args.command}"}
    
    # Output JSON
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
