#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Define utilities to work with files."""

# pylint: disable=invalid-name,dangerous-default-value
# pylint: disable=too-many-locals,unused-argument,unnecessary-lambda

from typing import Dict, List, Union

import altair as alt
import pandas as pd


def configure_chart(
    chart: alt.Chart,
    label_fontsize: int = 12,
    show_grid: bool = True,
    grid_opacity: float = 0.5,
    label_opacity: float = 1,
    domain: bool = False,
    ticks: bool = False,
    label_fontweight: str = "normal",
    title_fontweight: str = "bold",
    label_font_color: str = "grey",
    title_font_color: str = "black",
) -> alt.Chart:
    """."""
    chart = (
        chart.configure_view(strokeWidth=0)
        .configure_axisX(labelPadding=10, labelOpacity=label_opacity)
        .configure_axis(
            labelFontSize=label_fontsize,
            labelFontWeight=label_fontweight,
            labelColor=label_font_color,
            titleFontSize=label_fontsize,
            titleFontWeight=title_fontweight,
            titleColor=title_font_color,
            grid=show_grid,
            gridOpacity=grid_opacity,
            domain=domain,
            ticks=ticks,
        )
    )
    return chart


def plot_bar_chart(
    df: pd.DataFrame,
    xvar: str,
    yvar: str,
    xtitle: str,
    y_axis_sort: List[str],
    color_by_col: str,
    color_labels: List[str],
    color_values: List[str],
    ptitle: alt.TitleParams,
    axis_label_fontsize: int,
    fig_size: Dict[str, int],
) -> alt.Chart:
    """."""
    chart = (
        alt.Chart(data=df, title=ptitle)
        .mark_bar()
        .encode(
            x=alt.X(xvar, title=xtitle),
            y=alt.Y(yvar, title=None, sort=y_axis_sort),
            color=alt.Color(
                color_by_col,
                title=None,
                legend=None,
                scale=alt.Scale(domain=color_labels, range=color_values),
            ),
        )
        .properties(**fig_size)
    )
    chart = configure_chart(
        chart, show_grid=False, label_fontsize=axis_label_fontsize
    )
    return chart


def plot_grouped_bar_chart(
    df: pd.DataFrame,
    xvar: str,
    yvar: str,
    ytitle: str,
    color_by_col: str,
    column_var: str,
    color_labels: List[str],
    color_values: List[str],
    ptitle: alt.TitleParams,
    axis_label_fontsize: int,
    facet_column_spacing: int,
    fig_size: Dict[str, int],
) -> alt.Chart:
    """."""
    chart = (
        alt.Chart(data=df, title=ptitle)
        .mark_bar()
        .encode(
            x=alt.X(xvar, title=None, sort="y", axis=alt.Axis(labels=False)),
            y=alt.Y(yvar, title=ytitle),
            color=alt.Color(
                color_by_col,
                title=None,
                scale=alt.Scale(domain=color_labels, range=color_values),
                legend=alt.Legend(
                    titleFontSize=axis_label_fontsize,
                    labelFontSize=axis_label_fontsize,
                ),
            ),
            column=alt.Column(
                column_var,
                title=None,
                spacing=facet_column_spacing,
                header=alt.Header(
                    labelFontSize=axis_label_fontsize, labelOrient="bottom"
                ),
            ),
        )
        .properties(**fig_size)
    )
    chart = configure_chart(chart, axis_label_fontsize)
    return chart


def plot_line_charts_with_shaded_area(
    df: pd.DataFrame,
    xvar: str,
    yvar: str,
    yvar2: str,
    xvar_areas: str,
    xvar_areas2: str,
    color_by_col_areas: str,
    y_max: int,
    xtitle: str,
    ytitle: str,
    axis_label_fontsize: int,
    ptitle: alt.TitleParams,
    annotation_text: str,
    annotation_text_color: str,
    annotation_text_opacity: float,
    annotation_text_x_loc: int,
    annotation_text_y_loc: int,
    annotation_text_solid: Dict[str, int],
    annotation_text_dashed: Dict[str, int],
    areas_opacity: float,
    axis_label_color: str,
    axis_tick_label_color: str,
    axis2_label_color: str,
    axis2_tick_label_color: str,
    line_color: str,
    line_color2: str,
    marker_size: int,
    marker_fill: str,
    marker_edge_color: str,
    marker_edge_color2: str,
    fig_size: Dict[str, int] = dict(width=675, height=300),
) -> alt.Chart:
    """."""
    areas_cols = [c.replace(":O", "") for c in [xvar_areas, xvar_areas2]]
    df_areas = df[areas_cols].drop_duplicates()
    df_line_annotations = df[[xvar.split(":")[0]]].head(1)
    y_axis = alt.Axis(
        title=xtitle,
        titleColor=axis_label_color,
        labelColor=axis_tick_label_color,
        domainWidth=1,
    )
    base = (
        alt.Chart(data=df, title=ptitle)
        .encode(x=alt.X(xvar, title=None, axis=alt.Axis(labelAngle=0)))
        .properties(**fig_size)
    )
    non_tick_label_yvars = ["num_stations", "frac_neighs_with_bikeshare"]
    if all([tl not in yvar for tl in non_tick_label_yvars]):
        y_axis.labelExpr = 'datum.value / 1E6 + "M"'
    left = base.mark_line(
        color=line_color,
        point={
            "filled": False,
            "fill": marker_fill,
            "stroke": marker_edge_color,
            "size": marker_size,
        },
    ).encode(alt.Y(yvar, axis=y_axis, scale=alt.Scale(domain=[0, y_max])))
    right = base.mark_line(
        color=line_color2,
        point={
            "filled": False,
            "fill": marker_fill,
            "stroke": marker_edge_color2,
            "size": marker_size,
        },
        strokeDash=[6, 1],
    ).encode(
        alt.Y(
            yvar2,
            axis=alt.Axis(
                title=ytitle,
                titleColor=axis2_label_color,
                labelColor=axis2_tick_label_color,
                domainWidth=1,
                domainDash=[12, 1],
            ),
        )
    )

    areas = (
        alt.Chart(data=df_areas)
        .mark_rect(opacity=areas_opacity)
        .encode(
            x=alt.X(xvar_areas, axis=alt.Axis(labelAngle=0)),
            x2=xvar_areas2,
            y=alt.value(0),
            y2=alt.value(fig_size["height"] - 10),
            color=alt.Color(color_by_col_areas, title=None, legend=None),
        )
    )
    text = (
        alt.Chart(data=df_areas)
        .mark_text(
            text=annotation_text,
            align="right",
            color=annotation_text_color,
            fontSize=axis_label_fontsize,
            opacity=annotation_text_opacity,
            dx=annotation_text_x_loc,
            dy=annotation_text_y_loc,
        )
        .encode(x=alt.X(xvar_areas, title=None, axis=alt.Axis(labelAngle=0)))
    )
    text_solid = (
        alt.Chart(data=df_line_annotations)
        .mark_text(
            text=xtitle.split(" (")[0].replace(", %", ""),
            align="right",
            color=axis_label_color,
            fontSize=axis_label_fontsize,
            opacity=annotation_text_opacity,
            **annotation_text_solid,
        )
        .encode(x=alt.X(xvar, title=None, axis=alt.Axis(labelAngle=0)))
    )
    text_dashed = (
        alt.Chart(data=df_line_annotations)
        .mark_text(
            text=ytitle.split(" (")[0],
            align="right",
            color=axis_label_color,
            fontSize=axis_label_fontsize,
            opacity=annotation_text_opacity,
            **annotation_text_dashed,
        )
        .encode(x=alt.X(xvar, title=None, axis=alt.Axis(labelAngle=0)))
    )
    chart = alt.layer(areas, left, right, text, text_solid, text_dashed)
    chart = configure_chart(chart, axis_label_fontsize)
    return chart.resolve_scale(y="independent")


def plot_multi_axis_line_chart(
    df: pd.DataFrame,
    data_text: pd.DataFrame,
    data_areas: pd.DataFrame,
    xvar: str,
    yvar: str,
    xvar_rule: str,
    yvar2: str,
    xvar_areas: str,
    xvar_areas2: str,
    color_by_col_areas: str,
    axis_label_fontsize: int,
    legend: alt.Legend,
    xtitle: str,
    ytitle: str,
    areas_opacity: float,
    y_axis_range: List[int],
    y2_axis_range: List[int],
    axis_label_color: str,
    axis_tick_label_color: str,
    axis2_label_color: str,
    axis2_tick_label_color: str,
    line_color: str,
    line_color2: str,
    ptitle: alt.TitleParams,
    text_reords: List[Dict],
    fig_size: Dict[str, int] = dict(width=675, height=300),
) -> alt.Chart:
    """."""
    base = (
        alt.Chart(data=df, title=ptitle)
        .encode(alt.X(xvar, title=None))
        .properties(**fig_size)
    )
    trips = base.mark_line(color=line_color).encode(
        alt.Y(
            yvar,
            axis=alt.Axis(
                title=xtitle,
                titleColor=axis_label_color,
                labelColor=axis_tick_label_color,
                domainWidth=1,
            ),
            scale=alt.Scale(domain=y_axis_range),
        )
    )
    stations = base.mark_line(color=line_color2, strokeDash=[6, 1]).encode(
        alt.Y(
            yvar2,
            axis=alt.Axis(
                title=ytitle,
                titleColor=axis2_label_color,
                labelColor=axis2_tick_label_color,
                domainWidth=1,
                domainDash=[12, 1],
            ),
            scale=alt.Scale(domain=y2_axis_range),
        )
    )
    texts = {
        record["text"]: (
            alt.Chart(data=data_text)
            .mark_text(
                text=record["text"],
                align="right",
                color=record["color"],
                fontSize=axis_label_fontsize,
                opacity=record["opacity"],
                dy=record["dy"],
            )
            .encode(
                x=alt.X2(xvar_rule, title=None, axis=alt.Axis(labelAngle=0))
            )
        )
        for record in text_reords
    }
    areas = (
        alt.Chart(data=data_areas)
        .mark_rect(opacity=areas_opacity)
        .encode(
            x=alt.X(xvar_areas, axis=alt.Axis(labelAngle=0)),
            x2=xvar_areas2,
            y=alt.value(0),
            y2=alt.value(fig_size["height"] - 10),
            color=alt.Color(color_by_col_areas, title=None, legend=legend),
        )
    )
    chart = alt.layer(trips, stations, *list(texts.values()), areas)
    chart = configure_chart(chart, axis_label_fontsize)
    chart = chart.resolve_scale(y="independent")
    return chart


def plot_grouped_line_charts(
    df: pd.DataFrame,
    df_line: pd.DataFrame,
    xvar: str,
    yvar: str,
    color_by_col: str,
    color_labels: List[str],
    color_values: List[str],
    legend: alt.Legend,
    annotation_text: str,
    annotation_text_color: str,
    annotation_text_opacity: float,
    annotation_text_x_loc: int,
    annotation_text_y_loc: int,
    xvar_rule: str,
    color_rule: str,
    title_text: str,
    sub_title_text_color: str = "#7f7f7f",
    sub_title_vertical_padding: int = 5,
    axis_label_fontsize: int = 14,
    x_axis_ticks: Union[List, None] = None,
    concat: str = "column",
    fig_size: Dict[str, int] = dict(width=375, height=300),
) -> alt.Chart:
    """."""
    charts = {}
    for k, fstype in enumerate(["top-performer", "others"]):
        if concat == "row":
            show_x_labels = False if k == 0 else True
        else:
            show_x_labels = True
        if x_axis_ticks:
            x_axis = alt.Axis(
                values=x_axis_ticks, labels=show_x_labels, labelAngle=-45
            )
        else:
            x_axis = alt.Axis(labels=show_x_labels, labelAngle=-45)
        ptitle_text = title_text if k == 0 else " "
        ptitle = alt.TitleParams(
            text=ptitle_text,
            subtitle=fstype,
            subtitleFontSize=axis_label_fontsize,
            subtitleColor=sub_title_text_color,
            subtitlePadding=sub_title_vertical_padding,
            fontSize=axis_label_fontsize,
        )
        data = df.query(f"station_type == '{fstype}'")
        chart = (
            alt.Chart()
            .mark_line()
            .encode(
                x=alt.X(xvar, title=None, axis=x_axis),
                y=alt.Y(yvar, title=None, axis=alt.Axis(labels=True)),
                color=alt.Color(
                    color_by_col,
                    title=None,
                    legend=legend,
                    scale=alt.Scale(domain=color_labels, range=color_values),
                ),
            )
            .properties(**fig_size)
        )
        layer = [chart]
        if xvar_rule:
            rules = (
                alt.Chart()
                .mark_rule(
                    stroke=color_rule, strokeWidth=1.25, strokeDash=[12, 1]
                )
                .encode(x=alt.X2(xvar_rule, title=None, axis=x_axis))
            )
            layer += [rules]
        if annotation_text:
            text = (
                alt.Chart(data=df_line)
                .mark_text(
                    text=annotation_text,
                    align="center",
                    color=annotation_text_color,
                    fontSize=axis_label_fontsize,
                    opacity=annotation_text_opacity,
                    dx=annotation_text_x_loc,
                    dy=annotation_text_y_loc,
                )
                .encode(x=alt.X2(xvar, title=None, axis=x_axis))
            )
            # rules, text, chart
            layer = layer + [text] if k == 0 else layer
        # layer = [rules, text] + layer if k == 0 else [rules] + layer
        charts[fstype] = alt.layer(*layer, data=data, title=ptitle)

    # combine charts
    combo = (
        alt.vconcat(*charts.values())
        if concat == "row"
        else alt.hconcat(*charts.values())
    )
    # configure combined chart
    chart = configure_chart(
        combo.configure_concat(spacing=0), label_fontsize=axis_label_fontsize
    )
    return chart


def plot_bar_chart_array(
    df: pd.DataFrame,
    xvar: str,
    yvar: str,
    color_by_col: str,
    color_labels: List[str],
    color_values: List[str],
    legend: alt.Legend,
    title_text: str,
    column_var: str,
    column_spacing: int,
    column_label_position: str,
    column_label_color: str,
    column_sort: List[str] = [],
    sub_title_text_color: str = "#7f7f7f",
    sub_title_vertical_padding: int = 5,
    axis_label_fontsize: int = 14,
    concat: str = "column",
    column_label_angle: int = 0,
    column_label_align: str = "center",
    fig_size: Dict[str, int] = dict(width=375, height=300),
) -> alt.Chart:
    """."""
    header = alt.Header(
        labelFontSize=axis_label_fontsize,
        labelOrient=column_label_position,
        labelColor=column_label_color,
        labelAlign=column_label_align,
    )
    if concat == "row":
        header.labelAngle = column_label_angle

    # create charts
    charts = {"Annual": {}, "Casual": {}}
    for user_type in ["Annual", "Casual"]:
        for k, fstype in enumerate(["top-performer", "others"]):
            data = df.query(
                f"(user_type == '{user_type}') & (station_type == '{fstype}')"
            )
            ptitle_text = title_text[user_type] if k == 0 else " "
            ptitle = alt.TitleParams(
                text=ptitle_text,
                anchor="middle",
                subtitle=fstype,
                subtitleFontSize=axis_label_fontsize,
                subtitleColor=sub_title_text_color,
                subtitlePadding=sub_title_vertical_padding,
                fontSize=axis_label_fontsize,
            )
            chart = (
                alt.Chart(data=data, title=ptitle)
                .mark_bar()
                .encode(
                    x=alt.X(
                        xvar,
                        title=None,
                        sort=column_sort if column_sort else None,
                        axis=alt.Axis(labels=False),
                    ),
                    y=alt.Y(yvar, title=None),
                    color=alt.Color(
                        color_by_col,
                        title=None,
                        legend=legend,
                        scale=alt.Scale(
                            domain=color_labels[user_type],
                            range=color_values[user_type],
                        ),
                    ),
                    column=alt.Column(
                        column_var,
                        title=None,
                        spacing=column_spacing,
                        header=header,
                    ),
                )
                .properties(**fig_size)
            )
            charts[user_type][fstype] = chart

    # format charts
    charts_formatted = {}
    station_types = ["top-performer", "others"]
    for user_type in ["Annual", "Casual"]:
        charts_list = [charts[user_type][st] for st in station_types]
        charts_formatted[user_type] = configure_chart(
            (
                alt.vconcat(*charts_list)
                if concat == "row"
                else alt.hconcat(*charts_list)
            )
            .resolve_scale(y="independent")
            .configure_concat(spacing=0),
            show_grid=False,
            label_fontsize=axis_label_fontsize,
        )
    return charts_formatted


def plot_scatter_chart_grid(
    df: pd.DataFrame,
    xvar: str,
    yvar: str,
    row_var: str,
    color_by_col: str,
    col_var: str,
    row_sort: List[int],
    facet_label_color: str,
    color_labels: List[str],
    color_values: List[str],
    legend: alt.Legend,
    y_scale: str,
    ptitle: alt.TitleParams,
    marker_size: int,
    annotation_text_color: str,
    annotation_text_x_loc_var: int,
    annotation_text_y_loc_var: int,
    annotation_text_color_by_col: int,
    axis_label_fontsize: int = 14,
    fig_size: Dict[str, int] = dict(width=375, height=300),
) -> alt.Chart:
    """."""
    chart = (
        alt.Chart()
        .mark_point(size=marker_size)
        .encode(
            x=alt.X(xvar, title=None),
            y=alt.Y(
                yvar,
                title=None,
                scale=alt.Scale(type=y_scale),
            ),
            color=alt.Color(
                color_by_col,
                legend=legend,
                scale=alt.Scale(domain=color_labels, range=color_values),
            ),
        )
        .properties(**fig_size)
    )
    text = (
        alt.Chart()
        .mark_text(color=annotation_text_color, angle=270, fontSize=40)
        .encode(
            x=alt.X(annotation_text_x_loc_var, title=None),
            y=alt.Y(annotation_text_y_loc_var, title=None),
            text=alt.Text(annotation_text_color_by_col),
        )
    )
    combo = (
        alt.layer(chart, text, data=df)
        .facet(
            title=ptitle,
            row=alt.Row(
                row_var,
                title=None,
                sort=row_sort,
                header=alt.Header(
                    labelFontSize=axis_label_fontsize,
                    labelOrient="left",
                    labelColor=facet_label_color,
                ),
            ),
            column=alt.Column(
                col_var,
                title=None,
                sort=["top-performer", "others"],
                header=alt.Header(
                    labelFontSize=axis_label_fontsize,
                    labelOrient="top",
                    labelColor=facet_label_color,
                ),
            ),
        )
        .configure_facet(spacing=5)
    )
    combo = configure_chart(combo, axis_label_fontsize)
    combo = combo.resolve_scale(y="independent")
    return combo


def plot_faceted_line_chart(
    df: pd.DataFrame,
    xvar: str,
    yvar: str,
    color_by_col: str,
    column_col: str,
    column_spacing: str,
    column_sort: List[str],
    color_labels: List[str],
    color_values: List[str],
    legend: alt.Legend,
    ptitle: alt.TitleParams,
    marker_size: int,
    marker_opacity: float,
    tooltip: alt.Tooltip,
    axis_label_fontsize: int = 14,
    fig_size: Dict[str, int] = dict(width=375, height=300),
) -> alt.Chart:
    """."""
    chart = (
        alt.Chart(data=df, title=ptitle)
        .mark_line(
            point={
                "filled": False,
                "size": marker_size,
                "strokeOpacity": marker_opacity,
            }
        )
        .encode(
            x=alt.X(xvar, title=None, axis=alt.Axis()),
            y=alt.Y(yvar, title=None, scale=alt.Scale(type="linear")),
            color=alt.Color(
                color_by_col,
                title=None,
                scale=alt.Scale(domain=color_labels, range=color_values),
                legend=legend,
            ),
            column=alt.Column(
                column_col,
                title=None,
                sort=column_sort,
                header=alt.Header(
                    labelFontSize=axis_label_fontsize, labelColor="grey"
                ),
                spacing=column_spacing,
            ),
            tooltip=tooltip,
        )
        .properties(**fig_size)
        .interactive()
    )
    chart = configure_chart(chart, axis_label_fontsize)
    chart = chart.resolve_scale(y="independent")
    return chart


def plot_line_chart_grid(
    df: pd.DataFrame,
    xvar: str,
    yvars: str,
    xvar_areas: str,
    xvar_areas2: str,
    color_by_col_areas: str,
    areas_opacity: float,
    axis_label_color: str,
    axis_tick_label_color: str,
    annotation_text_color: str,
    ptitles: Dict[str, str],
    ptitles_x_locs: Dict[str, int],
    ytitles: Dict[str, str],
    line_color: str,
    marker_size: int,
    marker_fill: str,
    marker_edge_color: str,
    annotation_text_y_loc: int,
    annotation_text_opacity: float,
    concat_spacing: int,
    axis_label_opacity: float = 0.7,
    axis_label_fontsize: int = 14,
    fig_size: Dict[str, int] = dict(width=375, height=300),
) -> List[Union[alt.Chart, Dict[str, alt.Chart]]]:
    """."""
    charts_dict = {}
    for k, yvar in enumerate(yvars):
        yvar_name = yvar.split(":")[0]
        ptitle = alt.TitleParams(
            ptitles[yvar_name],
            anchor="start",
            dx=ptitles_x_locs[yvar_name],
            dy=10,
            fontSize=axis_label_fontsize,
        )
        if "trips" in yvar:
            annotation_text = "Projected"
            annotation_text_x_loc = 120
        else:
            annotation_text = "Four-Year Growth Plan"
            annotation_text_x_loc = 160

        areas_cols = [c.replace(":O", "") for c in [xvar_areas, xvar_areas2]]
        df_areas = df[areas_cols].drop_duplicates()
        y_axis = alt.Axis(
            title=ytitles[yvar_name],
            titleColor=axis_label_color,
            titleFontWeight="normal",
            labelColor=axis_tick_label_color,
            labelOpacity=axis_label_opacity,
            domainWidth=1,
        )
        if k < len(yvars) - 1:
            x_axis = alt.Axis(labels=False)
        else:
            x_axis = alt.Axis(
                labelAngle=0, labelOpacity=axis_label_opacity - 0.3
            )
        base = (
            alt.Chart(data=df, title=ptitle)
            .encode(x=alt.X(xvar, title=None, axis=x_axis))
            .properties(**fig_size)
        )
        if "trips" in yvar:
            y_axis.labelExpr = 'datum.value / 1E6 + "M"'

        line = base.mark_line(
            color=line_color,
            point={
                "filled": False,
                "fill": marker_fill,
                "stroke": marker_edge_color,
                "size": marker_size,
            },
        ).encode(alt.Y(yvar, axis=y_axis))
        areas = (
            alt.Chart(data=df_areas)
            .mark_rect(opacity=areas_opacity)
            .encode(
                x=alt.X(xvar_areas, axis=x_axis),
                x2=xvar_areas2,
                y=alt.value(0),
                y2=alt.value(fig_size["height"]),
                color=alt.Color(color_by_col_areas, title=None, legend=None),
            )
        )
        text = (
            alt.Chart(data=df_areas)
            .mark_text(
                text=annotation_text,
                align="right",
                color=annotation_text_color,
                fontSize=axis_label_fontsize,
                opacity=annotation_text_opacity,
                dx=annotation_text_x_loc,
                dy=annotation_text_y_loc,
            )
            .encode(x=alt.X(xvar_areas, title=None, axis=x_axis))
        )
        chart = alt.layer(areas, line, text)
        charts_dict[yvar_name] = chart
    combo = (
        alt.vconcat(*[charts_dict[y.split(":")[0]] for y in yvars])
        .resolve_scale(y="independent")
        .configure_concat(spacing=concat_spacing)
    )
    combo = configure_chart(combo, axis_label_fontsize)
    return [combo, charts_dict]


def plot_non_grouped_bar_chart_grid(
    df: pd.DataFrame,
    rows_labels_colors: Dict[str, Dict[str, List[str]]],
    xvar: str,
    yvar: str,
    color_by_col: str,
    legend_label_font_color: str,
    title_text: str,
    xtitle_text: str,
    title_fontweight: str = "bold",
    title_font_color: str = "black",
    axis_label_fontsize: int = 14,
    ptitle_xloc: int = 55,
    fig_size: Dict[str, int] = dict(width=375, height=300),
) -> alt.Chart:
    """."""
    charts = {}
    for k, (st, v) in enumerate(rows_labels_colors.items()):
        legend = legend = (
            alt.Legend(
                title=None,
                labelFontSize=axis_label_fontsize,
                labelColor=legend_label_font_color,
            )
            if k == 0
            else None
        )
        ptitle = (
            alt.TitleParams(
                title_text,
                anchor="start",
                dx=ptitle_xloc,
                fontSize=axis_label_fontsize,
            )
            if k == 0
            else ""
        )
        chart = (
            alt.Chart(data=df.query(f"station_type == '{st}'"))
            .mark_bar()
            .encode(
                x=alt.X(xvar, title=xtitle_text if k > 0 else None),
                y=alt.Y(
                    yvar,
                    title=st,
                    sort=v["labels"],
                    axis=alt.Axis(labels=False),
                ),
                color=alt.Color(
                    color_by_col,
                    scale=alt.Scale(domain=v["labels"], range=v["colors"]),
                    legend=legend,
                ),
            )
            .properties(**fig_size, title=ptitle)
        )
        charts[st] = chart
    chart = alt.vconcat(*list(charts.values()))
    chart = configure_chart(
        chart.configure_concat(spacing=10),
        axis_label_fontsize,
        label_opacity=1,
        title_fontweight=title_fontweight,
        title_font_color=title_font_color,
    )
    chart = chart.configure_axisX(titleFontWeight="bold", titleColor="black")
    chart = chart.resolve_scale(y="independent")
    return chart


def plot_simple_heatmap(
    df: pd.DataFrame,
    xvar: str,
    yvar: str,
    color_by_col: str = "y:Q",
    color_scale: str = "linear",
    annot_color_threshold: float = 0.8,
    grid_linewidth: float = 0.75,
    grid_line_color: str = "white",
    ptitle_text: str = "Title text",
    axis_label_fontsize: int = 14,
    fig_size: Dict[str, int] = dict(width=510, height=115),
) -> alt.Chart:
    """."""
    ptitle = alt.TitleParams(
        text=ptitle_text,
        fontSize=axis_label_fontsize,
    )
    base = (
        alt.Chart(df)
        .encode(
            x=alt.X(xvar, title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y(yvar, title=None),
        )
        .properties(**fig_size)
    )
    heatmap = base.mark_rect(
        stroke=grid_line_color, strokeWidth=grid_linewidth
    ).encode(
        color=alt.Color(
            color_by_col,
            legend=None,
            scale=alt.Scale(type=color_scale, scheme="yelloworangered"),
        ),
    )
    text = base.mark_text(baseline="middle", size=14).encode(
        alt.Text(color_by_col, format=".3f"),
        color=alt.condition(
            alt.datum.y > annot_color_threshold,
            alt.value("white"),
            alt.value("black"),
        ),
    )
    chart = alt.layer(heatmap, text, title=ptitle)
    chart = configure_chart(
        chart,
        axis_label_fontsize,
        show_grid=False,
        title_fontweight="bold",
    )
    return chart


def plot_multi_axis_line_chart_grid(
    df: pd.DataFrame,
    xvar: str,
    line_colors: Dict[str, str],
    y1var: str = "avg_trips_per_station:Q",
    y2var_min: str = "tmin:Q",
    y2var_max: str = "tmax:Q",
    y_title_text: str = "Title text",
    y2_title_text: str = "Title text",
    title_text: str = "Title text",
    sub_title_text_color: str = "#7f7f7f",
    sub_title_vertical_padding: int = 5,
    shading_opacity: float = 0.5,
    shading_color: float = "lightgrey",
    axis_label_fontsize: int = 14,
    fig_size: Dict[str, int] = dict(width=700, height=360),
) -> alt.Chart:
    """."""
    charts = {}
    for k, fstype in enumerate(["top-performer", "others"]):
        ptitle_text = title_text if k == 0 else " "
        ptitle = alt.TitleParams(
            text=ptitle_text,
            subtitle=fstype,
            subtitleFontSize=axis_label_fontsize,
            subtitleColor=sub_title_text_color,
            subtitlePadding=sub_title_vertical_padding,
            fontSize=axis_label_fontsize,
        )
        base = (
            alt.Chart(data=df.query(f"station_type == '{fstype}'"))
            .encode(
                x=alt.X(
                    xvar,
                    title=None,
                    axis=(
                        alt.Axis(labelAngle=-45)
                        if k > 0
                        else alt.Axis(labels=False)
                    ),
                )
            )
            .properties(**fig_size)
        )
        line = base.mark_line(color=line_colors[fstype]).encode(
            y=alt.Y(
                y1var,
                title=y_title_text if k > 0 else None,
                axis=alt.Axis(titleColor=line_colors[fstype]),
            ),
        )
        area = base.mark_area(
            opacity=shading_opacity, color=shading_color
        ).encode(
            alt.Y(
                y2var_min,
                title=y2_title_text if k > 0 else None,
                axis=alt.Axis(titleColor="grey"),
            ),
            alt.Y2(y2var_max, title=None),
        )
        chart = alt.layer(line, area, title=ptitle).resolve_scale(
            y="independent"
        )
        charts[fstype] = chart
    chart = configure_chart(
        alt.vconcat(*list(charts.values())).configure_concat(spacing=0),
        axis_label_fontsize,
        show_grid=False,
        title_fontweight="bold",
    )
    return chart


def plot_pie_chart(
    df: pd.DataFrame,
    yvar: str,
    color_by_col: str,
    ptitle: alt.TitleParams,
    label_non_white_color: str,
    radius: int,
    text_radius_offset: int,
    axis_label_fontsize: int,
    annotation_label_fontsize: int,
    annotation_radius: int,
    yvar_non_white_threshold: int,
    stroke_thickness: int,
    x_loc_annotation: int,
    x_loc_label: int,
    colors: Dict[str, str],
) -> alt.Chart:
    """."""
    base = alt.Chart(df, title=ptitle).encode(
        theta=alt.Theta(yvar, stack=True),
        color=alt.Color(
            color_by_col,
            scale=alt.Scale(
                range=list(colors.values()),
                domain=list(colors),
            ),
            legend=None,
        ),
    )
    pie = base.mark_arc(
        outerRadius=radius,
        stroke="white",
        strokeWidth=stroke_thickness,
        innerRadius=0,
        padAngle=0.0,
    )
    labels = base.mark_text(
        radius=text_radius_offset,
        size=axis_label_fontsize,
        dx=x_loc_label,
        fontWeight="bold",
    ).encode(
        text=alt.Text(color_by_col),
        color=alt.condition(
            alt.datum.station_type == label_non_white_color,
            alt.value("darkgreen"),
            alt.value("#74c476"),
        ),
    )
    annotations = base.mark_text(
        radius=annotation_radius,
        size=annotation_label_fontsize,
        dx=x_loc_annotation,
    ).encode(
        text=alt.Text(
            yvar,
            type="quantitative",
            format=",.0f",
        ),
        color=alt.condition(
            alt.datum.frac_stations_overall < yvar_non_white_threshold,
            alt.value("black"),
            alt.value("white"),
        ),
    )
    chart = alt.layer(pie, labels, annotations)
    return chart


def plot_line_chart(
    data: pd.DataFrame,
    xvar: str = "num_stations:Q",
    yvar: str = "frac_trips_last_year:Q",
    xvar_line: str = "num_stations_selected:Q",
    xtitle: str = "Number of Top-Performing Stations",
    ytitle: str = "Fraction of 2022 Trips (%)",
    line_color: str = "darkgreen",
    vertical_line_color: str = "red",
    annotation_text: str = "Chosen Number of Top-Performers",
    annotation_text_color: str = "red",
    annotation_text_opacity: float = 0.5,
    annotation_text_loc: Dict[str, int] = dict(dx=200, dy=25),
    axis_label_fontsize: int = 14,
    title_loc: int = 45,
    fig_size: Dict[str, int] = dict(width=450, height=270),
) -> alt.Chart:
    """."""
    frac_market_pen = data.query("num_stations == num_stations_selected")[
        "frac_trips_last_year"
    ].squeeze()
    n_stations_top = data["num_stations_selected"].head(1).squeeze()
    ptitle = alt.Title(
        (
            f"Top {n_stations_top} stations captured "
            f"{frac_market_pen:.1f}% market share in 2022"
        ),
        anchor="start",
        dx=title_loc,
        fontSize=axis_label_fontsize,
    )

    df_line_annotations = data[[xvar_line.split(":")[0]]].head(1)
    base = alt.Chart(data=data, title=ptitle).encode().properties(**fig_size)
    chart = base.mark_line(color=line_color).encode(
        x=alt.X(xvar, title=xtitle),
        y=alt.Y(yvar, title=ytitle),
    )
    rule = base.mark_rule(color=vertical_line_color, strokeDash=[6, 1]).encode(
        x=alt.X(xvar_line)
    )
    text = (
        alt.Chart(data=df_line_annotations)
        .mark_text(
            text=annotation_text,
            align="right",
            color=annotation_text_color,
            fontSize=axis_label_fontsize,
            opacity=annotation_text_opacity,
            **annotation_text_loc,
        )
        .encode(x=alt.X(xvar_line, axis=alt.Axis(labelAngle=0)))
    )
    chart = configure_chart(alt.layer(chart, rule, text), axis_label_fontsize)
    return chart
