import sys
import datetime
import time
import re
import os
from pathlib import Path
from voice_input import VoiceRecodeAndRecongnize as vrar
from one_stroke_path import save_edge_points, TSP
#from image_search import image_search


LOG_FILE_DIR_PATH = str(Path(__file__).parent) + "/../log/"
LIMITED_TURN = 6

def run_game(turn):
    turn_counter = 1
    player_word_log = []
    npc_word_log = []
    # dt_now = datetime.datetime.now()
    # log_file_name = str(dt_now.year) + "-" + str(dt_now.month) + "-" \
    #                 + str(dt_now.day) + "-" + str(dt_now.hour) + "h" \
    #                 + str(dt_now.minute) + "m" + str(dt_now.second) + "s.json"
    # log_file_path = LOG_FILE_DIR_PATH + log_file_name
    # try:
    #     with open(log_file_path,x)as f:
    #         f.write("")
    # except FileExistsError:
    #     print("同名のログファイルが存在しています。")
    #     sys.exit()

    while True:
        print ("+++++++++ 第" + str(turn_counter) + "目 +++++++++")
        word = vrar()
        if word in player_word_log:
            print ("すでに使った単語です。")
            sys.exit()
        elif re.fullmatch(r".*[\u3093]", word) != None:
            print ("語尾に「ん」があります。")
            sys.exit()
        player_word_log.append(word)
        #image_search_path = image_search(word, npc_word_log)
        image_search_path = "ねこ.png"
        if image_search_path == None:
            print ("辞書に適切な画像が存在しません。")
            sys.exit()

        #path generation
        image_file_name = os.path.basename(image_search_path)
        print (image_file_name)
        image_name = os.path.splitext(image_file_name)[0]
        npc_word_log.append(image_name)
        this_file_path = str(Path(__file__).parent)
        image_path = this_file_path + "/../dic/" + image_file_name
        output_path = this_file_path + "/../output/"
        edge_points_path = output_path + image_name + "_edge_points.csv"
        start_time = time.time()
        print (edge_points_path)
        print (image_path)
        save_edge_points(image_path, edge_points_path)
        tsp = TSP(edge_points_path,alpha=1.0,beta=16.0,Q=1.0e3,vanish_ratio = 0.8)
        tsp.solve(1)
        print ("processing time : " + str(round(time.time()-start_time, 2)) + " seconds")
        tsp.path_save(output_path + image_name +"_best_order.csv")
        # with open (log_file_path, w) as f:
        #     f
        # if turn_counter >= turn:
        #     break
        turn_counter +=1
    
    print (player_word_log)
    print (npc_word_log)


if __name__=="__main__":
    argvs = sys.argv
    print (argvs)
    if len(argvs) <= 1:
        print ("ターン数を入力してください。")
        sys.exit()
    turn = int(argvs[1])
    if turn >= LIMITED_TURN:
        print ("ターン数を" + str(turn) +"にして下さい。")
        sys.exit()
    else:
        run_game(turn)