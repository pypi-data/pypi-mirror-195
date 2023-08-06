def base(volume, lenght, height):
    base = volume/(lenght*height)
    return base

def lenght(volume, base, height):
    lenght = volume/(base*height)
    return lenght

def height(volume, lenght, base):
    height = volume/(lenght*base)
    return height