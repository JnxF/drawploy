import math

net = [
  383,
  668,
  416,
  287,
  473,
  296,
  437,
  669
]

vm = [
  574,
  267,
  650,
  264,
  652,
  318,
  577,
  321
]


def compute_centre(bounding):
    x = bounding[0] + (bounding[0] - bounding[3])/2
    y = bounding[1] + (bounding[1] - bounding[7])/2
    return x, y


cen1 = compute_centre(net)
cen2 = compute_centre(vm)


def compute_distance(obj1, obj2):
    return math.sqrt(pow(obj2[0]-obj1[0], 2) + pow(obj2[1]-obj1[1], 2))


dist = compute_distance(cen1, cen2)

print(dist)