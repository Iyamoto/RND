
base = '<ОтчетИспКод КодВидПост="{}" ДатаПост="{}" СумДенСред="{}" СумИспСрок="{}"></ОтчетИспКод>'

with open("in.csv") as f:
    lis = [line.split(';') for line in f]        # create a list of lists
    sum = 0
    for i, x in enumerate(lis):
        num = x[2].strip().replace(' ', '').replace(',', '.')
        num = int(round(float(num), 0))
        sum += num
        print(base.format(x[0], x[1], num, num))

    print(int(sum))
