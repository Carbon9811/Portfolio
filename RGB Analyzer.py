import cv2
import numpy as np
import os

def truncate(n, decimals=0):
    '''Truncates number to required number of decimals'''
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def arith_avg(variable=[None]):
    '''Takes a simple arithmatic average of items in a list'''
    result = sum(variable)/len(variable)
    return result

def threshold(values_list = [None],threshold = 0):
    result = []
    for value in values_list:
        if sum(value) > threshold:
            result.append(value)
    return result

def img_bin_function(image):
    h,w,bpp = np.shape(image)
    bgr_values = []
    for py in range(2,h-2,5):
        for px in range(2,w-2,5):
            blue_intensity = []
            green_intensity = []
            red_intensity = []
            for y in range(py-2,py+2):
                for x in range(px-2,px+2):
                    blue_intensity.append(image[y][x][0])
                    green_intensity.append(image[y][x][1])
                    red_intensity.append(image[y][x][2])
            bgr_values.append([int(round(arith_avg(blue_intensity))),int(round(arith_avg(green_intensity))),int(round(arith_avg(red_intensity)))])
    return bgr_values
            
def clr_contribution(bgr_val):
    color_contribution = {
        "blue" : 0,
        "green" : 0,
        "red" : 0,
        "orange" : 0,
        "pink" : 0
    }
    for bgr in bgr_val:
        b = bgr[0]
        g = bgr[1]
        r = bgr[2]
        if b > r and b > 2*g:
            color_contribution["blue"] += 1
        if g > r and g > 2*b:
            color_contribution["green"] += 1
        if r > 4*b and r > 4*g:
            color_contribution["red"] += 1
        if (r > g and b > g) and (r > b and not r > 3 * b):
            color_contribution["pink"] += 1
        if (r > b and g > b) and (r > g and not r > 3 * g):
            color_contribution["orange"] += 1
    return color_contribution

save_dir = input('Input a filename: ')
i = 1
for filename in os.listdir("C:\\Users\\david\\Desktop\\Image Analysis"):
    img = cv2.imread(os.path.join("C:\\Users\\david\\Desktop\\Image Analysis",filename))
    if img is not None:
        bgr_values = []
        bgr_val = img_bin_function(m)
        filtered_bgr_values = threshold(bgr_val,5)
        color_contribution = clr_contribution(filtered_bgr_values)

        total_color = 0
        for key in color_contribution:
            total_color += color_contribution[key]
            
        print(f'Image {i} done, writing file')
            
        with open(save_dir, 'a') as f:
            for color in color_contribution:
                f.write(str(color_contribution[color] / total_color)+'\t')
            f.write('\n')
            f.close()
        
        print(f'Done writing image {i}')
            
    i += 1