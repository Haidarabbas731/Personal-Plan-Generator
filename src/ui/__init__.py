from .header import render_header
from .inputs import render_goal_inputs, render_time_inputs
from .model_picker import render_model_picker
from .result import render_result
from .styles import inject_styles

__all__ = [
    "inject_styles",
    "render_header",
    "render_model_picker",
    "render_goal_inputs",
    "render_time_inputs",
    "render_result",
]
