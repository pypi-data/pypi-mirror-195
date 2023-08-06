from __future__ import annotations
from .base import BaseChart
import pybi as pbi

from typing import TYPE_CHECKING, Optional
from pybi.core.components.reactiveComponent import EChartDatasetInfo
from .utils import merge_user_options

if TYPE_CHECKING:
    from pybi.core.dataSource import DataSourceTable


class ScatterChart(BaseChart):
    def __init__(
        self,
        data: DataSourceTable,
        x: str,
        y: str,
        color: Optional[str] = None,
        size: Optional[str] = None,
        agg="round(avg(${}),2)",
    ):
        super().__init__()
        self.data = data
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.agg = agg
        self._series_configs = {}

    def _create_default_click_filter(self):
        # TODO:
        self.click_filter("x", self.data, self.x)

    def get_options_infos(self):
        opts = super().get_options()
        update_config, update_axis, remove_series = merge_user_options(opts)

        opt_data = None
        if self.color:
            opt_data = pbi.set_dataView(
                f"select `{self.color}`,`{self.x}`,`{self.y}` from {self.data}"
            )
        else:
            opt_data = pbi.set_dataView(
                f"select 1,`{self.x}`,`{self.y}` from {self.data}"
            )

        series_config = {
            "type": "scatter",
        }

        update_config(series_config)

        series_config.update(self._series_configs)

        ds_info = EChartDatasetInfo(series_config, "dataset[0]", opt_data.source_name)

        opts["xAxis"] = [{}]

        opts["yAxis"] = [{}]

        update_axis(opts)

        opts["tooltip"] = {"trigger": "item"}

        remove_series()

        return opts, [ds_info], self._updateInfos
