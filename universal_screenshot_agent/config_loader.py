# Dependency: pip install pyyaml
"""
Config loader for Universal Screenshot Agent.
Loads product-specific YAML configurations with environment variable interpolation.
"""

import os
import re
import sys
import yaml
from typing import Dict, List, Optional


def _interpolate_env_vars(value):
    """Replace ${VAR:-default} patterns with environment variable values.
    
    Supports:
      ${VAR}         - required env var (error if missing)
      ${VAR:-default} - env var with default fallback
    """
    if isinstance(value, str):
        def replacer(match):
            var_name = match.group(1)
            default = match.group(3)  # group 3 is the default value after :-
            env_val = os.environ.get(var_name)
            if env_val is not None:
                return env_val
            if default is not None:
                return default
            return match.group(0)  # Leave unreplaced if no default and not in env
        return re.sub(r'\$\{([A-Za-z_][A-Za-z0-9_]*)(:-(.*?))?\}', replacer, value)
    elif isinstance(value, dict):
        return {k: _interpolate_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_interpolate_env_vars(item) for item in value]
    return value


def _get_products_dir() -> str:
    """Return the absolute path to the products/ directory."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "products")


def load_product_config(product_slug: str, products_dir: str = None) -> Dict:
    """Load and validate a product's config.yaml.
    
    Args:
        product_slug: e.g., "my_product"
        products_dir: Path to the products/ directory. 
                      Defaults to universal_screenshot_agent/products/
    
    Returns:
        Parsed config dict with env var interpolation applied.
    
    Raises:
        FileNotFoundError: If config.yaml doesn't exist
        ValueError: If required fields are missing
    """
    if products_dir is None:
        products_dir = _get_products_dir()
    
    config_path = os.path.join(products_dir, product_slug, "config.yaml")
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Product config not found: {config_path}\n"
            f"Create it by copying products/_template/config.yaml"
        )
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # Interpolate environment variables
    config = _interpolate_env_vars(config)
    
    # Validate required fields
    errors = validate_config(config)
    if errors:
        raise ValueError(
            f"Config validation failed for '{product_slug}':\n" +
            "\n".join(f"  - {e}" for e in errors)
        )
    
    return config


def validate_config(config: Dict) -> List[str]:
    """Validate required config fields. Returns list of error messages."""
    errors = []
    
    # Required top-level sections
    required_sections = ["product", "local_site", "browser"]
    for section in required_sections:
        if section not in config:
            errors.append(f"Missing required section: '{section}'")
    
    # Product info
    if "product" in config:
        for field in ["name", "slug"]:
            if field not in config["product"]:
                errors.append(f"Missing product.{field}")
    
    # Local site
    if "local_site" in config:
        if "url" not in config["local_site"]:
            errors.append("Missing local_site.url")
        if "admin_entry" not in config["local_site"]:
            errors.append("Missing local_site.admin_entry")
    
    return errors


def get_product_paths(product_slug: str, products_dir: str = None) -> Dict[str, str]:
    """Return standard paths for a product.
    
    Returns dict with keys:
        config, docs, specs, screenshots, adapter, wp_posts
    """
    if products_dir is None:
        products_dir = _get_products_dir()
    
    base = os.path.join(products_dir, product_slug)
    return {
        "root": base,
        "config": os.path.join(base, "config.yaml"),
        "docs": os.path.join(base, "docs"),
        "specs": os.path.join(base, "specs"),
        "screenshots": os.path.join(base, "screenshots"),
        "adapter": os.path.join(base, "adapter.py"),
        "wp_posts": os.path.join(base, "wp_posts.json"),
    }


def load_adapter(product_slug: str, config: Dict, products_dir: str = None):
    """Dynamically load a product's adapter class.
    
    Looks for products/{slug}/adapter.py containing a class that extends ProductAdapter.
    Falls back to GenericWebAppAdapter if no custom adapter exists.
    
    Args:
        product_slug: e.g., "my_product"
        config: Parsed config dict
        products_dir: Path to the products/ directory
    
    Returns:
        An instantiated ProductAdapter subclass
    """
    from .product_adapter import GenericWebAppAdapter
    
    if products_dir is None:
        products_dir = _get_products_dir()
    
    adapter_path = os.path.join(products_dir, product_slug, "adapter.py")
    
    if os.path.exists(adapter_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            f"products.{product_slug}.adapter", adapter_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find the first class that isn't GenericWebAppAdapter
        from .product_adapter import ProductAdapter
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) 
                and issubclass(attr, ProductAdapter)
                and attr is not ProductAdapter
                and attr is not GenericWebAppAdapter):
                print(f"  Loaded adapter: {attr.__name__} from {adapter_path}")
                return attr(config)
        
        print(f"  No custom adapter class found in {adapter_path}, using GenericWebAppAdapter")
    
    return GenericWebAppAdapter(config)
