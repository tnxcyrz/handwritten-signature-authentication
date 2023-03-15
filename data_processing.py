import os
import random

def split_train_validation(x, percentage=0.6):
  train_size = int(len(x) * percentage)

  train = random.sample(x, train_size)
  validation = [v for v in x if v not in train]

  return (train, validation)

def get_set_triplets(legit_names, forged_names):
  set_triplets = [(legit_name, forged_name, '0') for legit_name in legit_names for forged_name in forged_names]

  for name in legit_names:
    for distinct_name in legit_names:
      if name != distinct_name:
        set_triplets.append((name, distinct_name, '1'))

  return set_triplets

def write_csv_file(file_name, lines):
  with open(file_name, 'w') as file:
    header_line = 'image_1,image_2,legit_pair'
    file_lines = '\n'.join([header_line] + lines)

    file.writelines(file_lines)

def process_raw_train_data(random_seed):
  random.seed(random_seed)

  raw_train_dir_legit = 'data_set/train/genuine/'
  raw_train_dir_forgeries = 'data_set/train/forgeries/'

  legit_names = [file_name for file_name in os.listdir(raw_train_dir_legit)]
  forged_names = [file_name for file_name in os.listdir(raw_train_dir_forgeries)]

  signature_ids = list(set([file_name[:3] for file_name in legit_names]))

  train_lines = []
  validation_lines = []

  for signature_id in signature_ids:
    id_legit_names = [raw_train_dir_legit + name for name in legit_names if name[:3] == signature_id]
    id_forged_names = [raw_train_dir_forgeries + name for name in forged_names if name[4:7] == signature_id]

    train_legit_names, validation_legit_names = split_train_validation(id_legit_names)
    train_forged_names, validation_forged_names = split_train_validation(id_forged_names)

    train_triplets = get_set_triplets(train_legit_names, train_forged_names)
    validation_triplets = get_set_triplets(validation_legit_names, validation_forged_names)

    train_lines.extend([','.join(triplet) for triplet in train_triplets])
    validation_lines.extend([','.join(triplet) for triplet in validation_triplets])

  train_csv_file_name = 'data_set/train.csv'
  validation_csv_file_name = 'data_set/validation.csv'

  write_csv_file(train_csv_file_name, train_lines)
  write_csv_file(validation_csv_file_name, validation_lines)

def get_test_set_quartets(reference_names, questioned_names):
  test_quartets = []

  for ref_name in reference_names:
    for distinct_ref_name in reference_names:
      if ref_name != distinct_ref_name:
        legit_pair = '1'
        questioned = '0'

        test_quartets.append((ref_name, distinct_ref_name, legit_pair, questioned))

    for quest_name in questioned_names:
      legit_pair = '1' if len(ref_name) == len(quest_name) else '0'
      questioned = '1'

      test_quartets.append((ref_name, quest_name, legit_pair, questioned))

  return test_quartets

def write_test_csv_file(file_name, lines):
  with open(file_name, 'w') as file:
    header_line = 'image_1,image_2,legit_pair,questioned'
    file_lines = '\n'.join([header_line] + lines)

    file.writelines(file_lines)

def process_raw_test_data(random_seed):
  random.seed(random_seed)
  
  raw_test_dir_reference = 'data_set/test/reference/'
  raw_test_dir_questioned = 'data_set/test/questioned/'

  test_lines = []

  for signature_id in os.listdir(raw_test_dir_reference):
    reference_dir = raw_test_dir_reference + signature_id
    questioned_dir = raw_test_dir_questioned + signature_id

    reference_names = [name for name in os.listdir(reference_dir)]
    questioned_names = [name for name in os.listdir(questioned_dir)]

    test_quartets = get_test_set_quartets(reference_names, questioned_names)
    test_lines.extend([','.join(quartet) for quartet in test_quartets])

  test_csv_file_name = 'data_set/test.csv'
  write_test_csv_file(test_csv_file_name, test_lines)
