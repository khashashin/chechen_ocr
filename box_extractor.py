import os
from bs4 import BeautifulSoup


def extract_boxes(document):
    soup = BeautifulSoup(open(document, encoding='utf8'), 'html.parser')
    ocrx_words = soup.find_all('span', class_='ocrx_word')

    boxes = []

    sentence = ''.join([word.text for word in ocrx_words])
    print('Boxing line: ', sentence)

    for word in ocrx_words:
        box_coords = word['title'].split(' ')[1:5]  # get the box coordinates
        box_coords[-1] = box_coords[-1][:-1]  # remove ; from the last coordinate
        box_coords = ' '.join(box_coords)
        boxes.append({
            'sentence': sentence,
            'box': box_coords,
            'word': word.text,
            'page': 0
        })

    return boxes


if __name__ == '__main__':
    for html in os.listdir('./html_box'):
        if html == '.gitkeep':
            continue
        print('Processing html: ' + html)
        boxed = extract_boxes('./html_box/' + html)

        # check if boxes folder exists
        if not os.path.exists('./boxes'):
            os.makedirs('./boxes')
        # check if file exists
        if not os.path.isfile(f'./boxes/{html}.box'):
            # create file but don't open it
            open(f'./boxes/{html}.box', 'w+').close()

        # save boxes to .box file as tsv
        with open(f'./boxes/{html}.box', 'r+', encoding="utf-8") as box_file:
            for box in boxed:
                box_file.write(f'{box["word"]}\t{box["box"]}\t{box["page"]}\n')
