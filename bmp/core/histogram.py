
class BMPHistogram:
    def __init__(self, rgb_array):
        self.red   = [0]*256
        self.green = [0]*256
        self.blue  = [0]*256
        self.commn = [0]*256
        for (r, g, b) in zip(rgb_array[0::3], rgb_array[1::3], rgb_array[2::3]):
            self.red[r]  +=1
            self.green[g]+=1
            self.blue[b] +=1
            lum = int(0.3*r+0.59*g+0.11*b)
            self.commn[lum]+=1
