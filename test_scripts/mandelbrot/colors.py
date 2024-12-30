from math import log

def value_to_color(n: int, max_depth: int):
    color = [0, 0, 0]
    if n < 0:
        return [250, 250, 250]
    if n == max_depth:
        color

    def catet(n, power=2):
        return (255 ** power - n ** power) ** 1/power

    if n > 4:
        k = log(n + 1, 1.0010)
    else:
        k = n * 20
    # k = (n**0.25)*250*1.3-130

    if 0 < k % 765 < 510:
        color[0] = catet(abs(255 - k % 765))
    if 255 < k % 765 < 765:
        color[1] = catet(abs(510 - k % 765))
    if 510 < k % 765 < 765:
        color[2] = catet(abs(765 - k % 765))
    if 0 <= k % 765 < 255 and k > 255:
        color[2] = catet(abs(0 - k % 765))

    for i in range(3):
        color[i] = max(0, min(color[i], 255))
    return color
