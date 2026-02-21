"""
Template product adapter — extend this for products with complex UIs.

For simple web apps, GenericWebAppAdapter + config.yaml is sufficient
and you don't need to create a custom adapter at all. Only create one
when you need:
  - Multi-step modal wizards
  - SPA tab switching
  - Complex navigation flows that can't be expressed in config
  - Product-specific CSS selectors for element finding
  - Post-action hooks (e.g., saving after typing)

To use:
  1. Rename the class to match your product (e.g., MyProductAdapter)
  2. Override only the methods you need
  3. The universal agent will auto-discover this file
"""

import sys
import os

# Add parent dirs to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from universal_screenshot_agent.product_adapter import GenericWebAppAdapter


class MyProductAdapter(GenericWebAppAdapter):
    """Custom adapter for My Product.

    Override methods from GenericWebAppAdapter as needed.
    Delete methods you don't need to customize — the defaults will be used.
    """

    # def navigate_to_section(self, page, heading, steps=None, prev_context=""):
    #     """Custom section navigation logic."""
    #     # Call super() for config-driven navigation, then add custom logic
    #     super().navigate_to_section(page, heading, steps, prev_context)

    # def ensure_correct_tab(self, page, step):
    #     """Switch tabs before element search if needed."""
    #     pass

    # def get_element_strategies(self, page, target, context, action):
    #     """Return product-specific element-finding strategies."""
    #     strategies = []
    #     # Add custom strategies here...
    #     # strategies.append(("my-strategy", lambda: page.locator("...")))
    #     return strategies

    # def advance_modal(self, page, target):
    #     """Advance multi-step modal wizard to the form step."""
    #     pass

    # def post_action_hook(self, page, step, action):
    #     """Run after step actions (e.g., save modal, enter course)."""
    #     pass

    # def get_sample_text(self, step):
    #     """Custom sample text for type actions."""
    #     return super().get_sample_text(step)
