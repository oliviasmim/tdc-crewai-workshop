import os

# CrewAI has a current bug where it tries to send telemetry data to the CrewAI servers.
# This code snippet will disable telemetry data from being sent.
def disable_telemetry():
    """Disable CrewAI telemetry"""
    os.environ["OTEL_SDK_DISABLED"] = "true"
    
    try:
        from crewai.telemetry import Telemetry
        
        def noop(*args, **kwargs):
            pass
            
        for attr in dir(Telemetry):
            if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
                setattr(Telemetry, attr, noop)
                
    except ImportError:
        pass