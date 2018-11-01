import os

if __name__ == '__main__':
    index = 0
    source = 'Codec_source/'
    if not os.path.exists(source):
        os.makedirs(source)
    index = 0
    total = int(input())
    total = 1000 if total >= 1000 else total
    page = int(total / 50) if total % 50 == 0 else int(total / 50) + 1
    while index < page:
        s = input()
        print(s)
        f = open(source + str(index) + '.txt', 'w', encoding='utf-8')
        f.write(s)
        f.close()
        index += 1
