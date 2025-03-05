import comtypes.client
from typing import Tuple, Any

def get_ui_automation_interfaces() -> Tuple[Any, Any]:
    """
    Initialize and return UI Automation interfaces.
    
    Returns:
        Tuple containing (IUIAutomation, UIAutomationCore)
    """
    UIAutomationCore = comtypes.client.GetModule("UIAutomationCore.dll")
    IUIAutomation = comtypes.client.CreateObject("{ff48dba4-60ef-4201-aa87-54103eef594e}", 
                                               interface=UIAutomationCore.IUIAutomation)
    return IUIAutomation, UIAutomationCore

def get_element_name(element) -> str:
    """
    Safely get the name of a UI Automation element.
    
    Args:
        element: UI Automation element
        
    Returns:
        Name of the element or empty string if not available
    """
    try:
        return element.CurrentName
    except:
        return ""
