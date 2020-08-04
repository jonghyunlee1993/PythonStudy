import tensorflow as tf
import codecs
import csv


file_path = './check_util/dnn_submission.tsv'
lines = []
with codecs.open(file_path, 'r', encoding='utf-8', errors='replace') as fdata:
    rdr = csv.reader(fdata, delimiter="\t")
    for line in rdr:
        lines.append(line)


def submission_csv_write(writer, lines, fix_line_idx, flag):
    for i, line in enumerate(lines):
        new_line = lines[i]
        if i == fix_line_idx:
            new_line[3] = 'Pass' if flag else 'Fail'
        writer.writerow(new_line)


def train_dataset_check(dataset):
  try:
    dataset_flag = True
    batch_size_flag = True
    image_shape_flag = True
    if not isinstance(dataset, tf.data.Dataset):
      print('train_dataset의 객체가 제대로 구성되지 않았습니다. 지문을 다시 확인하시기 바랍니다.')
      dataset_flag = False

    example = next(iter(dataset))

    if example[0].shape[0] != 128:
      print('미니배치 크기가 기존에 정의한 크기와 다릅니다. 이전에 우리가 정의한 배치크기를 인자로 활용했는지 확인하시기 바랍니다.')
      batch_size_flag = False

    image_shape = example[0].shape[1]
    if image_shape != 784:
      print('train_dataset의 차원이 잘못되었습니다. Dataset을 reshape 했는지 확인하시기 바랍니다.')
      image_shape_flag = False

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 1, dataset_flag)
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 2, batch_size_flag)
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 3, image_shape_flag)

    if dataset_flag and batch_size_flag and image_shape_flag:
      print('train_dataset을 잘 구현하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')


def test_dataset_check(dataset):
  try:
    dataset_flag = True
    batch_size_flag = True
    image_shape_flag = True
    if not isinstance(dataset, tf.data.Dataset):
      print('test_dataset의 객체가 제대로 구성되지 않았습니다. 지문을 다시 확인하시기 바랍니다.')
      dataset_flag = False

    example = next(iter(dataset))

    if example[0].shape[0] != 128:
      print('미니배치 크기가 기존에 정의한 크기와 다릅니다. 이전에 우리가 정의한 배치크기를 인자로 활용했는지 확인하시기 바랍니다.')
      batch_size_flag = False

    image_shape = example[0].shape[1]
    if image_shape != 784:
      print('test_dataset의 차원이 잘못되었습니다. Dataset을 reshape 했는지 확인하시기 바랍니다.')
      image_shape_flag = False

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 4, dataset_flag)
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 5, batch_size_flag)
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 6, image_shape_flag)

    if dataset_flag and batch_size_flag and image_shape_flag:
      print('test_dataset을 잘 구현하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')


def model_check(model):
  dense_flag = True
  bn_flag = True
  relu_flag = True
  all_dense_num_filters = []
  all_bn_num_features = []
  num_relu = 0

  try:
    for layer in model.layers:
      if 'dense' in layer.name:
        all_dense_num_filters.append(layer.weights[0].shape)
      if 'batch_normalization' in layer.name:
        all_bn_num_features.append(layer.weights[0].shape)
      if 're_lu' in layer.name:
        num_relu += 1


    if len(all_dense_num_filters) != 2:
      print('지문의 지시보다 더 많거나 적은 dense layer가 설계되었습니다. 지문을 다시 확인하시기 바랍니다.')
      dense_flag = False

    if len(all_bn_num_features) != 1:
      print('지문의 지시보다 더 많거나 적은 Bach normalization layer가 설계되었습니다. 지문을 다시 확인하시기 바랍니다.')
      bn_flag = False

    if num_relu != 1:
      print('지문의 지시보다 더 많거나 적은 ReLU 함수가 설계되었습니다. 지문을 다시 확인하시기 바랍니다.')
      relu_flag = False

    if all_dense_num_filters[0][1] != 512:
      print('첫번째 dense layer의 출력 feature 수가 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.')
      dense_flag = False

    if all_dense_num_filters[1][1] != 10:
      print('두번째 dense layer의 출력 feature 수가 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.')
      dense_flag = False

    if all_bn_num_features[0] != 512:
      print('첫번째 Batch normalization layer의 feature 수가 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.')
      bn_flag = False

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 7, dense_flag)
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 8, bn_flag)
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 9, relu_flag)

    if dense_flag and bn_flag and relu_flag:
      print('네트워크를 잘 구현하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')


def compile_check(model):

  opt_flag = True
  loss_flag = True
  metric_flag = True

  try:
    opt = str(model.optimizer)
    loss = model.loss

    if 'adam' not in opt:
      opt_flag = False
      print('optimizer를 확인해주세요.')
    if 'sparse' not in str(loss).lower():
      loss_flag = False
      print('loss를 확인해주세요.')
    if 'accuracy' not in model.metrics_names:
      metric_flag = False
      print('metric을 확인해주세요.')

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 10, opt_flag)

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 11, loss_flag)

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 12, metric_flag)

    if opt_flag and loss_flag and metric_flag:
      print('compile을 잘 정의하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')

def accuracy_check(model):

  acc_flag = True

  try:
    acc = model.metrics[0].result()
    if acc < 0.85:
      acc_flag = False
      print("Model Accuracy가 낮습니다. 하이퍼파라미터 숫자를 조절해보세요.")

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 13, acc_flag)

    if acc_flag:
      print('fit을 잘 정의하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')

def test_check(model):

  acc_flag = True

  try:
    acc = model.metrics[0].result()
    if acc < 0.80:
      acc_flag = False
      print("Test Accuracy가 낮습니다. Model의 구조와 Data Input, Output을 확인해주세.")

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 14, acc_flag)

    if acc_flag:
      print('모델 성능이 기준치를 넘었습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')

