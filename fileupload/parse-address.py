import csv
file_path = '../django-jquery-file-upload/media/pictures/pge_gas_billing_data_2257080156_2017-09-01_to_2017-12-22_shwVdKH.csv'
with open(file_path, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    lst = list(reader)
    sentence = str(lst[1])
    sentence_split = sentence.split(",")
    word = sentence_split[3].replace("']", "")
    print(word[3:])
