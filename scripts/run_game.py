import sys
import datetime
import time
import re
import os
from pathlib import Path
from voice_input import VoiceRecodeAndRecongnize as vrar
from one_stroke_path import interface_one_stroke_path
from image_search import SearchUsableImagePath


LOG_FILE_DIR_PATH = str(Path(__file__).parent) + "/../log/"
LIMITED_TURN = 6
center_paper = [0.4, 0]
width =0.01
size_picture = 0.1

def positioning(turn, center_paper, size_picture, width):
    if turn <= 3:
        center_picture_x = center_paper[0] + (width + size_picture)/2
    elif turn >= 4:
        center_picture_x = center_paper[0] - (width + size_picture)/2
    else:
        print ("不正な入力1（ターン数）")
        exit()

    if turn == 1 or turn == 4:
        center_picture_y = center_paper[1] + size_picture*(3/2) + width
    elif turn == 2 or turn == 5:
        center_picture_y = center_paper[1]
    elif turn == 3 or turn == 6:
        center_picture_y = center_paper[1] - size_picture*(3/2) + width
    else:
        print ("不正な入力2（ターン数）")
        exit()
    center_picture = [center_picture_x, center_picture_y]
    print (center_picture)
    return center_picture

def run_game(turn):
    turn_counter = 1
    player_word_log = []
    npc_word_log = []

    while True:
        print ("+++++++++ 第" + str(turn_counter) + "ターン目 +++++++++")
        word = vrar()
        if word in player_word_log:
            print ("すでに使った単語です。")
            sys.exit()
        elif re.fullmatch(r".*[\u3093]", word) != None:
            print ("語尾に「ん」があります。")
            sys.exit()

        player_word_log.append(word)

        image_search_path = SearchUsableImagePath(word, npc_word_log)
        # image_search_path = "ねこ.png"
        if image_search_path == None:
            print ("辞書に適切な画像が存在しません。")
            sys.exit()

        #path generation
        center_picture = positioning(turn_counter,center_paper, size_picture, width)
        image_file_name = os.path.basename(image_search_path)
        image_name = os.path.splitext(image_file_name)[0]
        print (image_name)
        npc_word_log.append(image_name)
        trajectory_path = interface_one_stroke_path(image_file_name, center_picture, size_picture, True)


        if turn_counter >= turn:
            print ("ひきわけ規定ターンが終了しました。")
            break
        turn_counter +=1

    print ("----------------------------------------")
    print ("プレイヤー側の回答履歴：" + str(player_word_log))
    print ("システム側の回答履歴：" + str(npc_word_log))
    print ("----------------------------------------")


if __name__=="__main__":
    argvs = sys.argv
    if len(argvs) <= 1:
        print ("ターン数を入力してください。")
        sys.exit()
    turn = int(argvs[1])
    if turn >= LIMITED_TURN:
        print ("ターン数を" + str(turn) +"にして下さい。")
        sys.exit()
    else:
        run_game(turn)