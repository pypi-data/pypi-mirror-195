def belah_ketupat(**kwargs):
    d1=kwargs.get('d1',0)
    d2=kwargs.get('d2',0)
    s=kwargs.get('s',0)
    luas=(0.5*d1*d2)
    keliling=(4*s)
    return luas,keliling
