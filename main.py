import comtypes.client
import time
import threading
from typing import Set, Optional

def initialize_ui_automation():
    """Initialize UI Automation COM interface."""
    UIAutomationCore = comtypes.client.GetModule("UIAutomationCore.dll")
    IUIAutomation = comtypes.client.CreateObject("{ff48dba4-60ef-4201-aa87-54103eef594e}", 
                                               interface=UIAutomationCore.IUIAutomation)
    return IUIAutomation, UIAutomationCore

def get_open_applications(ui_automation, ui_automation_core):
    """Get a list of all open applications."""
    desktop = ui_automation.GetRootElement()
    
    # Create a condition for application windows
    condition = ui_automation.CreatePropertyCondition(
        ui_automation_core.UIA_ControlTypePropertyId,
        ui_automation_core.UIA_WindowControlTypeId
    )
    
    # Find all elements matching the condition
    windows = desktop.FindAll(ui_automation_core.TreeScope_Children, condition)
    
    app_names = set()
    for i in range(windows.Length):
        window = windows.GetElement(i)
        name = window.CurrentName
        if name:
            app_names.add(name)
    
    return app_names

def get_focused_application(ui_automation, ui_automation_core):
    """Get the name of the currently focused application."""
    focused_element = ui_automation.GetFocusedElement()
    if focused_element:
        try:
            current_window = focused_element
            while current_window:
                control_type = current_window.GetCurrentPropertyValue(ui_automation_core.UIA_ControlTypePropertyId)
                if control_type == ui_automation_core.UIA_WindowControlTypeId:
                    return current_window.CurrentName
                
                try:
                    current_window = ui_automation.ElementFromHandle(
                        current_window.GetCurrentPropertyValue(ui_automation_core.UIA_NativeWindowHandlePropertyId)
                    ).GetParent()
                except:
                    return focused_element.CurrentName
        except:
            return focused_element.CurrentName
    
    return None

def focus_monitor():
    """Monitor for focus changes and print when they occur."""
    ui_automation, ui_automation_core = initialize_ui_automation()
    
    # Get initial focused application
    last_focused_app = get_focused_application(ui_automation, ui_automation_core)
    print(f"Currently focused: {last_focused_app}")
    
    while True:
        time.sleep(0.5)  # Check every half second
        current_focused_app = get_focused_application(ui_automation, ui_automation_core)
        
        if current_focused_app != last_focused_app:
            print(f"Focus changed to: {current_focused_app}")
            last_focused_app = current_focused_app

def main():
    # Initialize UI Automation
    ui_automation, ui_automation_core = initialize_ui_automation()
    
    # Get and print all open applications
    open_apps = get_open_applications(ui_automation, ui_automation_core)
    print("Open applications:")
    for app in sorted(open_apps):
        print(f"- {app}")
    
    # Get and print currently focused application
    focused_app = get_focused_application(ui_automation, ui_automation_core)
    print(f"\nCurrently focused: {focused_app}")
    
    # Start monitoring focus changes in a separate thread
    print("\nMonitoring focus changes (press Ctrl+C to exit)...")
    monitor_thread = threading.Thread(target=focus_monitor, daemon=True)
    monitor_thread.start()
    
    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting application...")

if __name__ == "__main__":
    main()
