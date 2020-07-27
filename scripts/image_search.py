import sys
import os
import random

path = "PBL_eshiritori/dic/"

def SearchUsableImagePath(prev_word: str, word_log: list, search_path = path) -> str:
    prev_word = prev_word.replace('ー','')
    prev_word = prev_word.replace('ゃ','や')
    prev_word = prev_word.replace('ゅ','ゆ')
    prev_word = prev_word.replace('ょ','よ')
    prev_word = prev_word.replace('っ','つ')
    next_initial = prev_word[-1]
#    search_path = search_path + next_initial
    image_list = []
    for p in os.listdir(search_path):
        image_list.append(os.path.splitext(os.path.basename(p))[0])
    connectable_image_list = [s for s in image_list if s.startswith(next_initial)]
    usable_image_list = list(set(connectable_image_list) - set(word_log))
    if not usable_image_list:
        return None 
    selected_image =  usable_image_list[random.randint(1,len(usable_image_list))-1]
    return search_path + [i for i in os.listdir(search_path) if selected_image in i][0]

if __name__=="__main__":
    argvs = sys.argv
    keyword = argvs[1]
    print("Input word: "+ keyword)
    test_word_log = ['ねこ','こたつ']
    image_search_path = SearchUsableImagePath(keyword, test_word_log)
    if image_search_path == None:
        print ("辞書に適切な画像が存在しません。")
    print(image_search_path)

