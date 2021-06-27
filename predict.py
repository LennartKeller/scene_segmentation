import os

import shutil
from code.utils.preprocess import read_json
from code.utils.postprocess import post_process
import subprocess


def reset_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)


if __name__ == "__main__":
    test_folder = "data/test"
    temp_folder = "data/tmp"
    pred_folder = "predictions"
    model_file = "model/model.tar.gz"

    test_files = sorted(os.listdir("data/test"))
    reset_folder(temp_folder)
    for test_file in test_files:
        test_file_path = os.path.join(test_folder, test_file)
        test_file = test_file + "l"
        read_json(test_file_path, temp_folder, split=test_file)
        print("#" * 10, "predicting: ", test_file)
        subprocess.run('code/scripts/predict.sh {} {} {}'.format(model_file, str(os.path.join(temp_folder, test_file)), test_file), shell=True)
        predicted_file_tmp_dir = os.path.join(pred_folder, test_file + ".pred")
        print("post-processing")
        post_process(os.path.join(test_folder, test_file), predicted_file_tmp_dir)
        os.remove(predicted_file_tmp_dir)
        print("done" + "#" * 15)

    #shutil.rmtree(temp_folder)
