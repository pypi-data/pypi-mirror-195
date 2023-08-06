import json
import os
import urllib
from addict import Dict
from folium import folium, features
import folium
import requests
from PIL import Image


class ShapeOperations:
    """
    Shape Operatings
    Draw Line
    Add Point
    """
    def __init__(self, map):
        self.map = map

    def addPoint(self, kwargs: Dict,
                 area: float = None,
                 color: str = 'darkgreen',
                 type: str = 'point'):
        """
        Add point
        """
        if type == 'point':
            image_paths = set()
            obj_ids = set()
            img_urls = set()
            params = Dict(kwargs)
            int_keys = [key for key in params if isinstance(key, int)]
            for i in range(2, max(int_keys) + 1, 2):
                if i in params:
                    area = "{:.3f}".format(float(area))
                    html = "<section class='container' style='width:450px'> \
                                <div class='value'> \
                                    <b>Area = </b> {area} square meter </br>\
                                    <b>Classname = </b> {classname} </br>\
                                    <b>Toplam intersect = </b> {Toplamintersect} </br>\
                                </div>" \
                        .format(area=area,
                                classname=params.classname,
                                Toplamintersect=i/2)
                    objectImage_1 = os.path.join(os.getcwd(), params[i].detectedPath_1)
                    objectImage_2 = os.path.join(os.getcwd(), params[i].detectedPath_2)
                    objId_1 = params[i].objId_1
                    objId_2 = params[i].objId_2
                    imgUrl_1 = params[i].imgUrl_1
                    imgUrl_2 = params[i].imgUrl_2
                    image_paths.add(objectImage_1)
                    image_paths.add(objectImage_2)
                    obj_ids.add(objId_1)
                    obj_ids.add(objId_2)
                    img_urls.add(imgUrl_1)
                    img_urls.add(imgUrl_2)

                    html += "<div class='image-container'>"
                    for path in image_paths:
                        html += f"<img src='{path}' style='width:auto;height:80px;'>"
                    html += "</div>"

                    html += "<div class='url-container'>"
                    for url in img_urls:
                        html += f"<a href='{url}'>Panorama Url</a> "
                    html += "</div>"

                    html += "<div class='value'>"
                    for obj_id in obj_ids:
                        html += f"<b>ObjectId = {obj_id}</b></br>"
                    html += "</div>"

            svg_icon_path = os.path.join(os.getcwd(), 'Config', 'icon', params.classname + '.png')

            icon = folium.DivIcon(html=f"""
                                            <div>
                                            <img src = "{svg_icon_path}" width="30px" "/>
                                            </div>""")

            mk = features.Marker([params.Lat_center, params.Lon_center],
                                 popup=html, icon=icon)

            mk_p = folium.Circle([params.Lat_center, params.Lon_center],  # noqa
                                 radius=2,
                                 fill=True,
                                 fill_color="yellow",
                                 color="yellow",
                                 fill_opacity=0.4)

            self.map.add_child(mk)
            self.map.add_child(mk_p)

        if type == 'paired':
            for point in kwargs:
                mk = features.Marker(point,
                                     popup=None, icon=folium.Icon(color=color, icon_color='#FFFF00'))

                self.map.add_child(mk)

    def addPolyline(self, des, classname, obj, color):
        """
        Poly line drawing
        """
        folium.PolyLine(
            locations=des,
            color=color,
            opacity=4,
            tooltip=classname + "-" + str(obj),
            weight=4
        ).add_to(self.map)
        pass

    def triggerMapOperations(self, mapDrawPoint):
        """
        processing coming point data
        """

        for key, params in mapDrawPoint.items():
            params = Dict(params)
            if params.mapOp == "polyline":
                self.addPolyline(des=params.desPoint, classname=params.classname, obj=key, color=params.color)
            elif params.mapOp == "point":
                self.addPoint(kwargs=params.point, area=params.object['area'], color="red", type=params.mapOp)
            elif params.mapOp == "paired":
                pass
                # self.addPoint(kwargs=params.pairedPoint, area=None, color="gray", type=params.mapOp)
            else:
                continue
