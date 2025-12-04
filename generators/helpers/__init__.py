# Helper modules for Flutterator
from .project import get_project_name, validate_flutter_project
from .utils import to_pascal_case, map_field_type
from .feature import (
    create_feature_layers,
    generate_value_objects_and_validators,
    generate_consolidated_value_objects,
    generate_value_validators,
    generate_extensions,
)
from .component import (
    create_component_layers,
    create_component_form_layers,
    generate_component_widget_from_template,
    generate_form_event_from_template,
    generate_form_state_from_template,
    generate_form_bloc_from_template,
)
from .navigation import (
    create_drawer_page,
    update_home_screen_with_drawer,
    create_drawer_widget,
    update_router_for_drawer_item,
    create_bottom_nav_page,
    update_home_screen_with_bottom_nav,
    create_bottom_nav_widget,
)
from .page import generate_page_file, update_router
from .config import (
    FlutteratorConfig,
    load_config,
    apply_cli_overrides,
    create_default_config,
    show_config,
    PROJECT_CONFIG_FILE,
    GLOBAL_CONFIG_FILE,
)

