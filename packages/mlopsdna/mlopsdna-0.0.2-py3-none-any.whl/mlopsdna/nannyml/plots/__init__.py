#  Author:   Niels Nuyttens  <niels@nannyml.com>
#  #
#  License: Apache Software License 2.0

#  Author:   Niels Nuyttens  <niels@nannyml.com>
#
#  License: Apache Software License 2.0

"""Module containing plotting implementations."""

from mlopsdna.nannyml.plots.colors import Colors
from mlopsdna.nannyml.plots.components.figure import Figure  # noqa: E402
from mlopsdna.nannyml.plots.components.hover import (
    Hover,
    render_alert_string,
    render_partial_target_string,
    render_period_string,
    render_x_coordinate,
)
from mlopsdna.nannyml.plots.components.joy_plot import calculate_chunk_distributions, joy
from mlopsdna.nannyml.plots.components.stacked_bar_plot import calculate_value_counts, stacked_bar
from mlopsdna.nannyml.plots.components.step_plot import alert, metric
from mlopsdna.nannyml.plots.util import (
    add_artificial_endpoint,
    check_and_convert,
    ensure_numpy,
    has_non_null_data,
    is_time_based_x_axis,
    pairwise,
)

CHUNK_KEY_COLUMN_NAME = 'key'
