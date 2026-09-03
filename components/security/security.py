import os
import streamlit.components.v1 as components

frontend_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "frontend"
    )
)

security_monitor = components.declare_component(
    name="security_monitor",
    path=frontend_dir
)