from enum import Enum
from functools import reduce
from collections import Counter
from io import BytesIO
from reportlab.platypus import Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
import numpy as np
import pandas as pd
import random
import re
import squarify
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
from matplotlib.markers import MarkerStyle
import rasterio
import rasterio.plot
import geopandas as gpd

IMAGE_WIDTH = 200
IMAGE_HEIGHT = 200
MEDIUM_FONT_SIZE = 11
MAX_HF = 30


class Align(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class Utils:
    @staticmethod
    def p(text, size=8, bold=False, color='#000', align=Align.CENTER):

        if bold:
            font = 'mb'
        else:
            font = 'ml'

        if np.isreal(text):
            if np.isnan(text):
                text = '-'
            else:
                text = int(text)

        ps = ParagraphStyle('mystyle',
                            alignment=align.value,
                            fontSize=size,
                            fontName=font,
                            textColor=color)
        return Paragraph(str(text), ps)

    @staticmethod
    def em(text, emYes=True):
        if str(text).strip() == 'Yes' or str(text).strip() == '1' or str(text).strip() == '1.0':
            result = Utils.p(
                'Yes', 7, emYes == True, '#FF0000' if emYes else '#000000')
        elif str(text).strip() == '0' or str(text).strip() == '0.0':
            result = Utils.p(
                'No', 7, emYes == False, '#FF0000' if emYes == False else '#000000')
        else:
            result = Utils.p(text, 7)
        return result

    @staticmethod
    def n(val):
        if np.isreal(val):
            if np.isnan(val):
                val = '-'
            else:
                val = int(val)

        return val

    @staticmethod
    def short(text):
        """Shorten a text by removing some words"""
        rep = {
            ' *health *center': '',
            ' *health *ceanter': '',
            ' +H[./]*C': '',
            ' *health *post': '',
            ' *heslth *post': '',
            ' *Haelth *Post': '',
            ' *Health *Poat': '',
            ' *hospital': '',
            ' +h[./]*p': '',
            ' {2,}': ''}

        return reduce(lambda a, kv: re.sub(*kv, a, flags=re.I), rep.items(), text)

    @staticmethod
    def make_autopct(values):
        def autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            # return '{p:.0f}% ({v:d})'.format(p=pct, v=val)
            return '{v:d}'.format(v=val)
        return autopct

    @staticmethod
    def get_colors(n):
        all_colors = list(plt.cm.colors.cnames.keys())
        random.seed(100)

        return random.choices(all_colors, k=n)

    @staticmethod
    def rearrange(data, label_field_name, value_field_name):
        sorted_data = data.sort_values(by=[value_field_name])
        splited = np.split(sorted_data, [int(len(sorted_data)/2)], axis=0)
        splited[0].set_index(np.arange(0, len(splited[0])*2, 2), inplace=True)
        splited[1].set_index(np.arange(1, len(splited[1])*2, 2), inplace=True)
        result = pd.concat(splited).sort_index(axis=0)

        return (result[label_field_name], result[value_field_name])

    @staticmethod
    def col2row(data):
        d = []
        i = 0
        c = 0
        r = -1
        for index, wr in data.iterrows():
            if i % 3 == 0:
                d.append(
                    [(Utils.short(wr['name_hp']), wr['mb_2008_y']), ('', ''), ('', ''), ('', '')])
                c = 1
                r += 1
            else:
                d[r][c] = (Utils.short(wr['name_hp']), wr['mb_2008_y'])
                c += 1
            i += 1
        return d

    @staticmethod
    def fixOverLappingText(text):
        sigFigures = 1
        positions = [(round(item.get_position()[1], sigFigures), item)
                     for item in text]

        overLapping = Counter((item[0] for item in positions))
        overLapping = [key for key, value in overLapping.items() if value >= 2]

        for key in overLapping:
            textObjects = [text for position,
                           text in positions if position == key]

            if textObjects:

                # If bigger font size scale will need increasing
                scale = 0.05
                spacings = np.linspace(
                    0, scale*len(textObjects), len(textObjects))
                for shift, textObject in zip(spacings, textObjects):
                    textObject.set_y(key + shift)

    @staticmethod
    def generate_tree_map(labels, sizes):

        colors = [plt.cm.Spectral(i/float(len(labels)))
                  for i in range(len(labels))]

        # Draw Plot
        fig = plt.figure()
        squarify.plot(sizes=sizes, label=labels, color=colors,
                      alpha=.8, text_kwargs={'fontsize': 14})
        plt.axis('off')

        return Utils.generate_image(fig)

    @staticmethod
    def generate_bar_chart(category, data, ylabel=''):

        # fig = plt.figure()
        fig, ax = plt.subplots(1, 1)
        plt.bar(np.array(category), np.array(
            data), color='#0085B7', zorder=3)
        plt.rc('xtick', labelsize=MEDIUM_FONT_SIZE)
        ax.grid(zorder=0)

        for i, val in enumerate(data):
            if np.isreal(val) and np.isnan(val):
                val = 0
            plt.text(i, val, int(val), horizontalalignment='center',
                     verticalalignment='bottom', rotation=70, fontdict={'fontweight': 500, 'size': MEDIUM_FONT_SIZE})

        plt.ylim(bottom=0)
        plt.ylabel(ylabel)
        plt.gca().set_xticklabels(category, rotation=60, horizontalalignment='right')

        return Utils.generate_image(fig)

    @staticmethod
    def generate_pie_chart(categories, data):
        colors = plt.cm.Dark2.colors

        fig, ax = plt.subplots(figsize=(8, 6))

        wedges, texts, autotexts = ax.pie(data,
                                          autopct=Utils.make_autopct(data), shadow=False, startangle=-40, colors=colors,
                                          pctdistance=0.85, explode=[0.01]*data.__len__(), textprops=dict(size=MEDIUM_FONT_SIZE))

        # Utils.fixOverLappingText(texts)

        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=None, zorder=0, va="center")

        for t, p in zip(categories, wedges):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang-0.01)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(t, xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment, **kw)

        # Label font size
        plt.setp(autotexts, size=MEDIUM_FONT_SIZE)  # , weight="bold")
        plt.rcParams['font.size'] = 14

        # draw circle
        # centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        # fig = plt.gcf()
        # fig.gca().add_artist(centre_circle)

        # legend
        # ax.legend(wedges, categories,
        #           title="Health Posts",
        #           loc="center left",
        #           bbox_to_anchor=(0.9, 0, 0, 1))

        return Utils.generate_image(fig)

    @staticmethod
    def generate_stacked_bar_chart(categories, values, color_label, ylabel):
        width = 0.8
        X = np.arange(len(categories))
        n = len(values)
        charts = []
        patches = []

        fig, ax = plt.subplots(1, 1)

        for i in range(n):
            charts.append(plt.bar(X - width/2. + i/float(n)*width, values[i],
                                  width=width/float(n), align="edge", color=color_label[i][0], zorder=3))
            patches.append(mpatches.Patch(
                color=color_label[i][0], label=color_label[i][1]))
        plt.xticks(X, categories)
        plt.ylim(bottom=0)

        ax.grid(zorder=0)

        # write values for each stacked box
        for chart in charts:
            for bar in chart:
                w, h = bar.get_width(), bar.get_height()
                h = 0 if np.isnan(h) else h
                plt.text(bar.get_x() + w/2, bar.get_y() + h + 0.3,
                         "{:.0f}".format(h), ha="center",
                         va="center", fontdict={'fontweight': 500, 'size': MEDIUM_FONT_SIZE, 'color':  'black'})

        plt.ylabel(ylabel)
        plt.legend(handles=patches,
                   loc="center left",
                   bbox_to_anchor=(1, 0, 0, 1))
        plt.gca().set_xticklabels(categories, rotation=60, horizontalalignment='right')
        plt.rc('xtick', labelsize=MEDIUM_FONT_SIZE)

        return Utils.generate_image(fig)

    @staticmethod
    def generate_map(region_map, district_map, selected_district=None):
        fig, ax = plt.subplots(1, 2, figsize=(14, 8))
        stratum_color = ['#aaa389', '#42c81d', '#f3f625', '#6c081f']

        # Plot the raster image
        with rasterio.open("assets/images/ETH_satellite_trimmed.tif") as raster:
            rasterio.plot.show(raster, ax=ax[0], cmap='gist_earth')

        # Plot the regions
        region_map.geometry.boundary.plot(
            color=None, edgecolor='black', linewidth=0.3, ax=ax[0])

        # Draw all districts
        district_map.plot(column='Group', cmap=ListedColormap(stratum_color),
                          linewidth=0.3, ax=ax[0], edgecolor='black', categorical=True, legend=True, legend_kwds={'loc': 'lower right', 'framealpha': 1, 'fontsize': 16})

        # Mark the target district and plot it in the second axis
        if not selected_district.empty:
            # take district's centroid
            district_centroid = gpd.GeoDataFrame(
                crs=None, geometry=[selected_district.centroid.iloc[0]])

            # Buffer point and plot it
            circle = gpd.GeoDataFrame(
                crs=None, geometry=district_centroid.buffer(.6))

            circle.plot(ax=ax[0], linewidth=2,
                        facecolor='white', edgecolor='red', alpha=0.6)

            # Draw the district separately in the second axis
            selected_district.plot(ax=ax[1], cmap=ListedColormap(
                stratum_color[int(selected_district.iloc[0]['Group'])]))

            # Plot a point marker on top of the district using the district's centroid as a center
            district_centroid.plot(ax=ax[0], color='red', markersize=1)

        # custom legend text
        labels = [
            'Free (API 0)',
            'Low (API 0-5)',
            'Medium (API 5-100)',
            'High (API >100)'
        ]

        leg = ax[0].get_legend()
        for text, label in zip(leg.get_texts(), labels):
            text.set_text(label)

        # tick text size
        for i in range(2):
            ax[i].tick_params(labelsize=16)

        return Utils.generate_image(fig)

    @staticmethod
    def generate_image(fig):
        fig.tight_layout()

        imgdata = BytesIO()
        fig.savefig(imgdata, format='png')
        imgdata.seek(0)  # rewind the data
        plt.close()

        return Image(imgdata, width=IMAGE_WIDTH, height=IMAGE_HEIGHT, kind='proportional')
