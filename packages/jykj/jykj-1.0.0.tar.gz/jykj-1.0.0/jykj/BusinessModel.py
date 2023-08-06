
import numpy as np

def rela_to_abs(arr, size):
    '''
    相对坐标转换为绝对, arr为[center_x, center_y, width, height]
    '''
    w, h = size[0], size[1]
    if (np.array(arr) <= 1).all():
        b = np.array([w, h, w, h])
        return arr*b
    else:
        return arr


def pnpoly(verts, testx, testy):
    '''
    判断点在多边形内, PNPoly算法
    '''
    vertx = [xyvert[0] for xyvert in verts]
    verty = [xyvert[1] for xyvert in verts]
    nvert = len(verts)
    c = False
    j = nvert - 1
    for i in range(nvert):
        if ((verty[i] > testy) != (verty[j] > testy)) and (testx < (vertx[j]-vertx[i])*(testy-verty[i])/(verty[j]-verty[i])+vertx[i]):
            c = not c
        j = i
    return c


def person_in_area(json_dict, area, resolution):

    persons = [i for i in json_dict['objects'] if i["name"].upper() == "PERSON"]
    if persons:
        persons_coords = [
            [i['relative_coordinates']["center_x"], i['relative_coordinates']["center_y"]+i['relative_coordinates']["height"]*0.45, i['relative_coordinates']["width"], i['relative_coordinates']["height"]] for i in persons]
        for i in persons_coords:
            i = rela_to_abs(i, resolution)
            for j in area:
                if pnpoly(j, i[0], i[1]):
                    return True
    return False


if __name__ == '__main__':
    json_dict = {"frame_id": 1,
                 "time":"2023-01-01 00:00:00",
                 "objects": [{"class_id":2, "name":"Person",
                               "relative_coordinates":{"center_x":0.934244, "center_y":0.586283, "width":0.102538, "height":0.358813}, 
                                "confidence":0.857021}]}
    area = [[[960, 0], [1920, 0], [1920, 1080], [960, 1080]]]
    resolution = [1920, 1080]
    print(person_in_area(json_dict=json_dict, area=area, resolution=resolution))
