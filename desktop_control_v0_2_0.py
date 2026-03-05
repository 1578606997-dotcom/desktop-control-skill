"""
Desktop Control Skill v0.2.0 - Core Improvements
Based on learnings from Turix and Fara-7B

Key improvements:
1. Multi-model architecture (inspired by Turix)
2. Direct coordinate prediction (inspired by Fara)
3. Small model support (inspired by Fara-7B efficiency)
4. Step optimization (reduced action steps)
"""

import pyautogui
import time
from typing import Tuple, Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import json
import os

# Configuration for multi-model support (inspired by Turix)
class ModelConfig:
    """Model configuration for different tasks"""
    
    # Large model for complex reasoning
    LARGE_MODEL = {
        "provider": "moonshot",
        "model": "kimi-k2.5",
        "use_for": ["complex_reasoning", "ui_understanding", "error_recovery"]
    }
    
    # Small model for simple actions (inspired by Fara-7B)
    SMALL_MODEL = {
        "provider": "moonshot",
        "model": "kimi-k2.5",  # Can be replaced with smaller model
        "use_for": ["simple_clicks", "text_input", "scrolling"],
        "max_tokens": 512,  # Limit tokens for speed
        "temperature": 0.1   # Lower randomness for reliability
    }
    
    # Vision model for screen understanding
    VISION_MODEL = {
        "provider": "moonshot",
        "model": "kimi-k2.5",
        "use_for": ["screenshot_analysis", "element_detection", "coordinate_prediction"]
    }


@dataclass
class Action:
    """Optimized action representation (inspired by Fara direct prediction)"""
    action_type: str  # "click", "type", "scroll", "wait"
    coordinates: Optional[Tuple[int, int]] = None  # Direct x, y prediction
    text: Optional[str] = None
    duration: Optional[float] = None
    
    def execute(self) -> bool:
        """Execute the action with error handling"""
        try:
            if self.action_type == "click" and self.coordinates:
                pyautogui.click(self.coordinates[0], self.coordinates[1])
            elif self.action_type == "type" and self.text:
                pyautogui.typewrite(self.text, interval=0.01)
            elif self.action_type == "scroll" and self.coordinates:
                pyautogui.scroll(self.coordinates[1], self.coordinates[0])
            elif self.action_type == "wait" and self.duration:
                time.sleep(self.duration)
            return True
        except Exception as e:
            print(f"Action failed: {e}")
            return False


class StepOptimizer:
    """Optimize action steps (inspired by Fara: 16 steps vs 41 steps)"""
    
    @staticmethod
    def merge_actions(actions: List[Action]) -> List[Action]:
        """Merge consecutive actions to reduce steps"""
        optimized = []
        i = 0
        while i < len(actions):
            current = actions[i]
            
            # Merge multiple text inputs into one
            if current.action_type == "type" and i + 1 < len(actions):
                texts = [current.text]
                j = i + 1
                while j < len(actions) and actions[j].action_type == "type":
                    texts.append(actions[j].text)
                    j += 1
                if len(texts) > 1:
                    merged_text = "".join(texts)
                    optimized.append(Action("type", text=merged_text))
                    i = j
                    continue
            
            # Skip unnecessary wait actions
            if current.action_type == "wait" and current.duration and current.duration < 0.1:
                i += 1
                continue
            
            optimized.append(current)
            i += 1
        
        return optimized
    
    @staticmethod
    def predict_efficient_path(start: Tuple[int, int], target: Tuple[int, int]) -> List[Action]:
        """Predict most efficient path (inspired by Fara efficiency)"""
        # Instead of multiple small moves, predict direct jump if possible
        distance = ((target[0] - start[0])**2 + (target[1] - start[1])**2) ** 0.5
        
        if distance < 50:
            # Small distance - direct move
            return [Action("click", coordinates=target)]
        else:
            # Large distance - might need intermediate steps for visual feedback
            mid_x = (start[0] + target[0]) // 2
            mid_y = (start[1] + target[1]) // 2
            return [
                Action("click", coordinates=(mid_x, mid_y)),
                Action("wait", duration=0.1),
                Action("click", coordinates=target)
            ]


class CoordinatePredictor:
    """Direct coordinate prediction (inspired by Fara-7B)"""
    
    @staticmethod
    def predict_from_screenshot(screenshot_path: str, target_description: str) -> Optional[Tuple[int, int]]:
        """
        Predict click coordinates from screenshot
        Inspired by Fara-7B's direct coordinate prediction without accessibility tree
        """
        # Placeholder for vision model integration
        # In practice, this would use a vision model to predict coordinates
        # based on the screenshot and target description
        
        # For now, return None to indicate manual fallback
        return None
    
    @staticmethod
    def calculate_relative_position(
        screen_size: Tuple[int, int], 
        element_position: Tuple[float, float]
    ) -> Tuple[int, int]:
        """Calculate absolute coordinates from relative position (0-1 range)"""
        x = int(screen_size[0] * element_position[0])
        y = int(screen_size[1] * element_position[1])
        return (x, y)


class MultiModelController:
    """Multi-model architecture (inspired by Turix)"""
    
    def __init__(self):
        self.action_history: List[Action] = []
        self.step_count = 0
        self.max_steps = 50  # Limit to prevent infinite loops
    
    def select_model_for_task(self, task_description: str) -> Dict[str, Any]:
        """Select appropriate model based on task complexity"""
        task_lower = task_description.lower()
        
        # Simple tasks -> small model
        simple_keywords = ["click", "type", "scroll", "wait", "move"]
        if any(keyword in task_lower for keyword in simple_keywords):
            return ModelConfig.SMALL_MODEL
        
        # Complex reasoning -> large model
        complex_keywords = ["analyze", "decide", "plan", "error", "fix"]
        if any(keyword in task_lower for keyword in complex_keywords):
            return ModelConfig.LARGE_MODEL
        
        # Default to large model for safety
        return ModelConfig.LARGE_MODEL
    
    def execute_task(self, task: str) -> Dict[str, Any]:
        """Execute task with step optimization"""
        result = {
            "success": False,
            "steps_taken": 0,
            "actions": [],
            "errors": []
        }
        
        # Select model
        model_config = self.select_model_for_task(task)
        print(f"Using model: {model_config['model']} for task: {task}")
        
        # Generate actions (placeholder - would call actual model)
        # In real implementation, this would use the selected model
        actions = self._generate_actions(task)
        
        # Optimize steps (inspired by Fara efficiency)
        optimized_actions = StepOptimizer.merge_actions(actions)
        
        # Execute
        for action in optimized_actions:
            if self.step_count >= self.max_steps:
                result["errors"].append("Max steps reached")
                break
            
            success = action.execute()
            if success:
                result["steps_taken"] += 1
                result["actions"].append(action)
                self.action_history.append(action)
            else:
                result["errors"].append(f"Action failed: {action}")
            
            self.step_count += 1
        
        result["success"] = len(result["errors"]) == 0
        return result
    
    def _generate_actions(self, task: str) -> List[Action]:
        """Generate actions from task (placeholder)"""
        # In real implementation, this would parse model output
        # and convert to Action objects
        return []


# Utility functions for common operations
class DesktopUtils:
    """Utility functions for desktop automation"""
    
    @staticmethod
    def get_screen_size() -> Tuple[int, int]:
        """Get current screen size"""
        return pyautogui.size()
    
    @staticmethod
    def take_screenshot(path: str) -> str:
        """Take screenshot and save"""
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return path
    
    @staticmethod
    def safe_click(x: int, y: int, duration: float = 0.2) -> bool:
        """Safe click with fallback"""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            pyautogui.click()
            return True
        except Exception as e:
            print(f"Click failed at ({x}, {y}): {e}")
            return False


if __name__ == "__main__":
    # Test the improvements
    controller = MultiModelController()
    
    print("Desktop Control Skill v0.2.0")
    print("Improvements based on Turix and Fara-7B research")
    print("- Multi-model architecture")
    print("- Direct coordinate prediction")
    print("- Step optimization")
    print("- Small model support")
