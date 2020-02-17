#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of DTE Calculator and is released under the  MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from matplotlib.dates import MonthLocator, DateFormatter

# Rate reference:
# https://newlook.dteenergy.com/wps/wcm/connect/23195474-a4d1-4d38-aa30-a4426fd3336b/WholeHouseRateOptions.pdf?MOD=AJPERES

# Residential Electric Service Rate
RES_CUTOFF = 17
RES_CAP_RATE_17KWH = 0.03705
RES_NON_CAP_RATE_17KWH = 0.04687

RES_CAP_RATE_ADDITIONAL = 0.05339
RES_NON_CAP_RATE_ADDITIONAL = 0.04687

# Time of Day Rate
TOD_SUMMER_CAP_PEAK = 0.12375
TOD_SUMMER_NON_CAP_PEAK = 0.04554
TOD_SUMMER_CAP_OFF_PEAK = 0.01145
TOD_SUMMER_NON_CAP_OFF_PEAK = 0.04554
TOD_WINTER_CAP_PEAK = 0.09747
TOD_WINTER_NON_CAP_PEAK = 0.04554
TOD_WINTER_CAP_OFF_PEAK = 0.00922
TOD_WINTER_NON_CAP_OFF_PEAK = 0.04554

# Delivery charges
RATE_SERVICE = 7.5
RATE_DISTRIBUTION_KWH = 0.06109
RATE_WASTE_REDUCTION = 0.004487
RATE_LIEAF = 0.92
RATE_NUCLEAR_SURCHARGE = 0.000827
RATE_TRANSITIONAL_RECOVERY = 0.001030
RATE_SALES_TAX = 0.06

# Sample method
SAMPLE_METHOD = 'BMS'   # BMS

# US Average
US_AVERAGE = 867

# Figure settings
TITLE_FONT_SIZE = 10
AXIS_FONT_SIZE = 8


def compute_delivery_charges(kwh_monthly):
    total = RATE_SERVICE
    total += kwh_monthly * RATE_DISTRIBUTION_KWH
    total += kwh_monthly * RATE_WASTE_REDUCTION
    total += kwh_monthly * RATE_NUCLEAR_SURCHARGE
    total += kwh_monthly * RATE_TRANSITIONAL_RECOVERY
    total += RATE_LIEAF

    return total


def compute_ToD_rate(data_raw):
    # Init
    data = data_raw

    data['Cost_Cap'] = 0
    data['Cost_NonCap'] = 0

    # Weekday filter
    index_weekday = data.index.weekday < 5
    index_weekend = data.index.weekday >= 5

    # Season filter
    index_summer = np.logical_and(
        data.index.month >= 6, data.index.month <= 10)
    index_winter = np.logical_or(
        data.index.month >= 11, data.index.month <= 5)

    # Hour filter
    index_peak = np.logical_and(
        data.index.hour >= 11, data.index.hour <= 18, index_weekday)
    index_off_peak = np.logical_or(
        data.index.hour < 11, data.index.hour > 18, index_weekend)

    # Combine filters
    index_summer_peak = np.logical_and(index_summer, index_peak)
    index_summer_off_peak = np.logical_and(index_summer, index_off_peak)
    index_winter_peak = np.logical_and(index_winter, index_peak)
    index_winter_off_peak = np.logical_and(index_winter, index_off_peak)

    # Calculate summer, peak
    summer_peak = data['Total'].loc[index_summer_peak]
    data.loc[index_summer_peak, 'Cost_Cap'] = summer_peak * TOD_SUMMER_CAP_PEAK
    data.loc[index_summer_peak, 'Cost_NonCap'] = summer_peak * \
        TOD_SUMMER_NON_CAP_PEAK

    # Calculate summer, off peak
    summer_off_peak = data['Total'].loc[index_summer_off_peak]
    data.loc[index_summer_off_peak, 'Cost_Cap'] = summer_off_peak * \
        TOD_SUMMER_CAP_OFF_PEAK
    data.loc[index_summer_off_peak, 'Cost_NonCap'] = summer_off_peak * \
        TOD_SUMMER_NON_CAP_OFF_PEAK

    # Calculate winter, peak
    winter_peak = data['Total'].loc[index_winter_peak]
    data.loc[index_winter_peak, 'Cost_Cap'] = winter_peak * \
        TOD_WINTER_CAP_PEAK
    data.loc[index_winter_peak, 'Cost_NonCap'] = winter_peak * \
        TOD_WINTER_NON_CAP_PEAK

    # Calculate winter, off peak
    winter_off_peak = data['Total'].loc[index_winter_off_peak]
    data.loc[index_winter_off_peak, 'Cost_Cap'] = winter_off_peak * \
        TOD_WINTER_CAP_OFF_PEAK
    data.loc[index_winter_off_peak, 'Cost_NonCap'] = winter_off_peak * \
        TOD_WINTER_NON_CAP_OFF_PEAK

    # Calculate delivery charges
    kwh_monthly = data['Total'].resample(SAMPLE_METHOD).sum()
    delivery_charges_monthly = compute_delivery_charges(kwh_monthly)

    # Total cost
    data['Total Cost'] = data['Cost_Cap'] + data['Cost_NonCap']
    cost_monthly = data['Total Cost'].resample(SAMPLE_METHOD).sum()
    sales_tax = cost_monthly * RATE_SALES_TAX
    total = cost_monthly + delivery_charges_monthly + sales_tax

    # Consumption on peak
    consumption_peak = data['Total'].loc[index_peak].resample(
        SAMPLE_METHOD).sum()
    consumption_offpeak = data['Total'].loc[index_off_peak].resample(
        SAMPLE_METHOD).sum()

    return total, consumption_peak, consumption_offpeak


def compute_RES_rate(data_raw):
    # Compute daily total consumption
    data = data_raw['Total'].resample('D').sum().to_frame()

    data['Cost_CAP_17'] = data['Total'] * RES_CAP_RATE_17KWH
    data['Cost_NON_CAP_17'] = data['Total'] * RES_NON_CAP_RATE_17KWH

    data['Cost_CAP_ADD'] = 0
    data['Cost_NON_CAP_ADD'] = 0

    # Filter
    index = data['Total'] > RES_CUTOFF
    data.loc[index, 'Cost_CAP_ADD'] = (
        data['Total'] - RES_CUTOFF) * RES_CAP_RATE_ADDITIONAL
    data.loc[index, 'Cost_NON_CAP_ADD'] = (
        data['Total'] - RES_CUTOFF) * RES_NON_CAP_RATE_ADDITIONAL

    # Compute delivery charges
    kwh_monthly = data['Total'].resample(SAMPLE_METHOD).sum()
    delivery_charges_monthly = compute_delivery_charges(kwh_monthly)

    # Total cost
    data['Total Cost'] = data['Cost_CAP_17'] + data['Cost_NON_CAP_17'] + \
        data['Cost_CAP_ADD'] + data['Cost_NON_CAP_ADD']
    cost_monthly = data['Total Cost'].resample(SAMPLE_METHOD).sum()
    sales_tax = cost_monthly * RATE_SALES_TAX
    total = cost_monthly + delivery_charges_monthly + sales_tax

    return total


def format_plots(plot_object):
    # Set label
    plot_object.set_xlabel('Date')

    # Change label sizes
    plot_object.title.set_size(TITLE_FONT_SIZE)
    plot_object.xaxis.label.set_size(AXIS_FONT_SIZE)
    plot_object.yaxis.label.set_size(AXIS_FONT_SIZE)
    plot_object.tick_params(labelsize=AXIS_FONT_SIZE)

    # Change tick spacing
    plot_object.set_xticks(plot_object.get_xticks()[::1])
    plot_object.xaxis.set_major_locator(
        MonthLocator(range(1, 13), bymonthday=1, interval=1))
    plot_object.xaxis.set_major_formatter(DateFormatter("%b"))


def dte_calculator(filename):
    register_matplotlib_converters()

    # Style
    sns.set(style="darkgrid")
    f, axarr = plt.subplots(2, 2)

    # Import data
    data = pd.read_csv(filename, parse_dates=[['Day', 'Hour of Day']])
    data = data.set_index(data['Day_Hour of Day'])
    data.index.rename('Date', inplace=True)
    data.rename(columns={'Hourly Total': 'Total'}, inplace=True)

    # Compute cost for the Residential Electric Service Rate
    cost_monthly_res = compute_RES_rate(data)

    # Compute cost for the Time of Day Service Rate
    cost_monthly_ToD, consumption_peak, consumption_offpeak = compute_ToD_rate(
        data)

    # Compute consumption KWH by month
    kwh_monthly = data['Total'].resample(SAMPLE_METHOD).sum()

    # Compute savings
    savings_monthly = cost_monthly_res - cost_monthly_ToD
    res_total = round(cost_monthly_res.sum(), 2)
    tod_total = round(cost_monthly_ToD.sum(), 2)
    savings_total = round(savings_monthly.sum(), 2)

    # Plot 1 - Consumption
    axarr[0, 0].plot(kwh_monthly.index, kwh_monthly)
    axarr[0, 0].set_title('Consumption by Month (kWh)')
    axarr[0, 0].axhline(US_AVERAGE, linewidth=1, color='r',
                        ls='--', label='US Residential Average')
    axarr[0, 0].legend()
    format_plots(axarr[0, 0])

    # Plot 2 - Peak vs Off Peak
    axarr[0, 1].plot(consumption_peak.index, consumption_peak, label='Peak')
    axarr[0, 1].plot(consumption_offpeak.index,
                     consumption_offpeak, label='Off Peak')
    axarr[0, 1].set_title('Consumption by Month, Peak vs Off Peak')
    axarr[0, 1].legend()
    format_plots(axarr[0, 1])

    # Plot 3 -  Services
    axarr[1, 0].plot(cost_monthly_res.index, cost_monthly_res,
                     label='Standard RES Service')
    axarr[1, 0].plot(cost_monthly_ToD.index,
                     cost_monthly_ToD, label='Time of Day Service')
    axarr[1, 0].set_title('Total Cost by Month')
    axarr[1, 0].legend()
    format_plots(axarr[1, 0])

    # Plot 4 - Savings
    axarr[1, 1].plot(cost_monthly_ToD.index, savings_monthly)
    axarr[1, 1].set_title('Total Savings by Month')

    plt.text(0.45, 0.9, "RES Total: $" + str(res_total),
             transform=axarr[1, 1].transAxes)
    plt.text(0.45, 0.8, "ToD Total: $" + str(tod_total),
             transform=axarr[1, 1].transAxes)
    plt.text(0.45, 0.7, "Savings Total: $" + str(savings_total),
             transform=axarr[1, 1].transAxes)
    format_plots(axarr[1, 1])

    # Export
    f.subplots_adjust(wspace=0.25, hspace=0.35)
    f.set_size_inches(11, 7)
    f.savefig('DTE.pdf', bbox_inches='tight')
    f.clf()
