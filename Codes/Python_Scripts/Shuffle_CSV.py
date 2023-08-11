from csv_shuffler import csv_shuffler

shuffler = csv_shuffler.ShuffleCSV(input_file='./data.csv',header=True, batch_size=20)

shuffler.shuffle_csv()