import datasets
from setfit import SetFitModel
import argparse

def result_postprocessing(result_proba):
    label_keys = {'1':'positive',
                  '0':'negative',
                  '2':'neutral'}
    negative_value = result_proba[0,0]
    positive_value = result_proba[0,1]
    if abs(negative_value - positive_value) < 0.2:
        class_predict = 2
    else:
        class_predict = result_proba.argmax()
    print('neg value', negative_value, 'positive value', positive_value)
    return label_keys[str(class_predict)]

def get_args():
    # create the argument parser
    parser = argparse.ArgumentParser()

    # add the arguments
    parser.add_argument("-w", "--weight_folder", default="", type=str, help="config file path")
    
    # parse the arguments
    args = parser.parse_args()

    # print the arguments
    return args

if __name__ == '__main__':
    args = get_args()
    if args.weight_folder == '':
        model = SetFitModel.from_pretrained("randypang/indo-review-sentiment-minilm3"
        )
    else:
        model = SetFitModel.from_pretrained(args.weight_folder)
    
    while True:
        text = input('write a review:')
        if text == 'exit':
            break
        result = model.predict_proba([text])
        postproc_result = result_postprocessing(result)
        print('text {} is: a {} review'.format(text, postproc_result))