from __future__ import annotations

from .base import BaseChart
import pybi as pbi
import pybi.utils.sql as sqlUtils

from typing import TYPE_CHECKING, Optional
from pybi.core.components.reactiveComponent import EChartDatasetInfo
from .utils import merge_user_options

if TYPE_CHECKING:
    from pybi.core.dataSource import DataSourceTable


class BarChart(BaseChart):
    def __init__(
        self,
        data: DataSourceTable,
        x: str,
        y: str,
        color: Optional[str] = None,
        agg="round(avg(${}),2)",
    ):
        super().__init__()
        self.data = data
        self.x = x
        self.y = y
        self.color = color
        self.agg = agg
        self._reverse_axis = False
        self._series_configs = {}

    def reverse_axis(self):
        self._reverse_axis = True
        return self

    def _create_default_click_filter(self):
        valueType, field = "x", self.x
        if self._reverse_axis:
            valueType, field = "y", self.y

        self.click_filter(valueType, self.data, self.x)

    def get_options_infos(self):
        opts = super().get_options()

        update_config, update_axis, remove_series = merge_user_options(opts)

        opt_data = None
        if self.color:
            opt_data = self.data.to_pivot(
                row=self.x, column=self.color, cell=self.y, agg=self.agg
            )
        else:
            agg_field = sqlUtils.apply_agg(self.agg, self.y)

            opt_data = pbi.set_dataView(
                f'select `{self.x}`,{agg_field} as "{self.y}" from {self.data} group by `{self.x}`'
            )

        series_config = {"type": "bar"}
        update_config(series_config)
        series_config.update(self._series_configs)

        ds_info = EChartDatasetInfo(series_config, "dataset[0]", opt_data.source_name)

        valueAxisConfig = {"type": "value"}
        catAxisConfig = {"type": "category"}

        if self._reverse_axis:
            opts["xAxis"] = [valueAxisConfig]
            opts["yAxis"] = [catAxisConfig]
        else:
            opts["xAxis"] = [catAxisConfig]
            opts["yAxis"] = [valueAxisConfig]

        update_axis(opts)

        remove_series()

        return opts, [ds_info], self._updateInfos
