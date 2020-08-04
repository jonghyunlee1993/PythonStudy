import os
import glob
import numpy as np

import tensorflow as tf
import codecs
import csv

IMG_SIZE = 150

file_path = './check_util/cnn_submission.tsv'
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


def dataset_check(output_dir):
  try:
    all_train_cat = glob.glob(os.path.join(output_dir, 'train', 'cat', '*'))
    all_train_dog = glob.glob(os.path.join(output_dir, 'train', 'dog', '*'))
    all_val_cat = glob.glob(os.path.join(output_dir, 'val', 'cat', '*'))
    all_val_dog = glob.glob(os.path.join(output_dir, 'val', 'dog', '*'))
    all_test_cat = glob.glob(os.path.join(output_dir, 'test', 'cat', '*'))
    all_test_dog = glob.glob(os.path.join(output_dir, 'test', 'dog', '*'))
  
    print('훈련용 고양이 이미지 개수:', len(all_train_cat))
    print('훈련용 강아지 이미지 개수:', len(all_train_dog))
    print('검증용 고양이 이미지 개수:', len(all_val_cat))
    print('검증용 강아지 이미지 개수:', len(all_val_dog))
    print('테스트용 고양이 이미지 개수:', len(all_test_cat))
    print('테스트용 강아지 이미지 개수:', len(all_test_dog))
  
    flag = True
    if len(all_train_cat) != 1000: flag = False
    if len(all_train_dog) != 1000: flag = False
    if len(all_val_cat) != 500: flag = False
    if len(all_val_dog) != 500: flag = False
    if len(all_test_cat) != 1000: flag = False
    if len(all_test_dog) != 1000: flag = False

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 1, flag)
  
    if flag:
      print('dataset이 제대로 구성되어 있습니다! 이어서 진행하셔도 좋습니다.')
    else:
      print('dataset이 제대로 구성되어 있지 않습니다. 경로가 올바른지 확인해보세요.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')


def resize_fn_check(resize):
  try:
    h = w = tf.random.uniform([], minval=100, maxval=200, dtype=tf.int32)
    image = tf.random.uniform([h, w, 3], minval=0, maxval=255, dtype=tf.int32)
    new_h = tf.random.uniform([], minval=100, maxval=200, dtype=tf.int32)
    new_w = tf.random.uniform([], minval=100, maxval=200, dtype=tf.int32)
    image = resize(image, new_h, new_w)

    flag = True
    if image.shape[0] != new_h.numpy() or image.shape[1] != new_w.numpy():
      print('원하는 사이즈로 resize가 되지 않습니다! 코드구현을 제대로했는지 다시 검토하시기 바랍니다.')
      flag = False
    else:
      print('resize 함수를 잘 구현 하셨습니다! 이어서 진행하셔도 좋습니다.')

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 2, flag)
      
  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')



def random_crop_fn_check(random_crop):
  try:
    h = w = tf.random.uniform([], minval=180, maxval=200, dtype=tf.int32)
    image = tf.random.uniform([h, w, 3], minval=0, maxval=255, dtype=tf.int32)
    image = random_crop(image)
  
    flag = True
    if image.shape[0] != IMG_SIZE or image.shape[1] != IMG_SIZE:
      print('원하는 사이즈로 crop이 되지 않습니다! 코드구현을 제대로했는지 다시 검토하시기 바랍니다.')
      flag = False
      
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 3, flag)

    if flag:
      print('random_crop 함수를 잘 구현 하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')



def normalize_fn_check(normalize):
  try:
    flag = True
    for _ in range(10): # test for 10 random images
      h = w = tf.random.uniform([], minval=100, maxval=200, dtype=tf.int32)
      image = tf.dtypes.cast(tf.random.uniform([h, w, 3], minval=0, maxval=255, dtype=tf.int32), tf.float32)
      image = normalize(image)
  
      if np.max(image.numpy()) > 1.0 or np.min(image.numpy()) < -1.0:
        print('[-1, 1]의 범위로 normalize 되지 않습니다! 코드구현을 제대로했는지 다시 검토하시기 바랍니다.')
        flag = False
        break
  
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 4, flag)
  
    if flag:
      print('normalize 함수를 잘 구현 하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')



def central_crop_fn_check(central_crop):
  try:
    h = w = tf.random.uniform([], minval=180, maxval=200, dtype=tf.int32)
    image = tf.random.uniform([h, w, 3], minval=0, maxval=255, dtype=tf.int32)
    image = central_crop(image)

    flag = True
    if image.shape[0] != IMG_SIZE or image.shape[1] != IMG_SIZE:
      print('원하는 사이즈로 crop이 되지 않습니다! 코드구현을 제대로했는지 다시 검토하시기 바랍니다.')
      flag = False
    else:
      print('central_crop 함수를 잘 구현 하셨습니다! 이어서 진행하셔도 좋습니다.')

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 5, flag)
      
  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')


def customized_dataset_check(dataset):

  example = next(iter(dataset))
  flag = True

  try:
    image_shape = example[0][0].shape
    if image_shape != np.array([150,150,3]):
      print('함수가 반환하는 img의 크기가 올바르지 않습니다. resize 과정에서 이미지 크기를 150으로 고정하는 부분을 실수로 수정했는지 확인하시기 바랍니다.')
      flag = False

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 6, flag)

    if flag:
      print('tf.data.Dataset을 이용하여 train_dataset을 잘 구현하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')




def model_check(model):
  conv_flag = True
  bn_flag = True
  relu_flag = True
  pool_flag = True
  dense_flag = True
  flatten_flag = False

  all_conv_num_filters = []
  all_conv_kernel_size = []
  all_bn_num_features = []
  all_maxpool_kernel_size = []
  num_relu = 0
  all_dense_units = []

  try:
    for layer in model.layers:
      if 'conv' in layer.name:
        for layer in layer.layers:
          if 'conv' in layer.name:
            all_conv_num_filters.append(layer.weights[0].shape[-1])
            all_conv_kernel_size.append(layer.weights[0].shape[0:2])
          if 'batch_normalization' in layer.name:
            all_bn_num_features.append(layer.weights[0].shape[0])
          if 'max_pooling2d' in layer.name:
            all_maxpool_kernel_size.append(layer.pool_size)
          if 're_lu' in layer.name:
            num_relu += 1
      else:
        if 'dense' in layer.name:
          all_dense_units.append(layer.kernel.shape[-1])

      if 'flatten' in layer.name:
        flatten_flag = True

    if not flatten_flag:
      print("Flatten Layer가 추가되지 않았습니다.")
  
    if len(all_conv_kernel_size) != 4:
      print('지문의 지시보다 더 많거나 적은 convolution layer가 설계되었습니다. 지문을 다시 확인하시기 바랍니다.')
      conv_flag = False
  
    if len(all_bn_num_features) != 4:
      print('지문의 지시보다 더 많거나 적은 batch normalization layer가 설계되었습니다. 지문을 다시 확인하시기 바랍니다.')
      bn_flag = False
  
    if num_relu != 4:
      print('지문의 지시보다 더 많거나 적은 ReLU 함수가 설계되었습니다. 지문을 다시 확인하시기 바랍니다.')
      relu_flag = False
  
    if len(all_maxpool_kernel_size) != 4:
      print('지문의 지시보더 더 많거나 적은 maxpooling layer가 설계되었습니다. 지문을 다시 확인하시기 바랍니다.')
      pool_flag = False
  
    if len(all_dense_units) != 2:
      print('지문의 지시보다 더 많거나 적은 dense layer가 설계되었습니다. 지문을 다시 확인하시기 바랍니다.')
      dense_flag = False
  
    target_num_filters = [32, 64, 128, 128]
    target_kernel_size = (3, 3)
    target_maxpool_kernel_size = (2, 2)
    target_dense_units = [512, 2]
  
    for i, (conv_channels, target) in enumerate(zip(all_conv_num_filters, target_num_filters)):
      if conv_channels != target:
        print('{}번째 convolution layer의 출력 채널 수가 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.'.format(i + 1))
        conv_flag = False
  
    for i, k_size in enumerate(all_conv_kernel_size):
      if k_size != target_kernel_size:
        print('{}번째 convolution layer의 필터 크기가 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.'.format(i + 1))
        conv_flag = False
  
    all_bn_num_features = []
    for i, (num_filter, target) in enumerate(zip(all_bn_num_features, target_num_filters)):
      if num_filter != target:
        print('{}번째 batch normalization layer의 feature 수가 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.'.format(i + 1))
        bn_flag = False
  
    for i, k_size in enumerate(all_maxpool_kernel_size):
      if k_size != target_maxpool_kernel_size:
        print('{}번째 maxpooling layer의 필터 크기가 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.'.format(i + 1))
        pool_flag = False
  
    for i, (dense_unit, target) in enumerate(zip(all_dense_units, target_dense_units)):
      if dense_unit != target:
        print('{}번째 dense layer의 출력 feature 수가 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.'.format(i + 1))
        dense_flag = False

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 7, conv_flag)
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 8, bn_flag)
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 9, relu_flag)
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 10, pool_flag)
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 11, dense_flag)

    if conv_flag and bn_flag and relu_flag and pool_flag and dense_flag and flatten_flag:
      print('네트워크를 잘 구현하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')

def callback_check(cp):
  weights_flag = True
  save_flag = True

  try:
    if not cp.save_weights_only:
      weights_flag = False
      print("save_weights_only를 설정해주세요.")

    if cp.save_freq != 'epoch':
      save_flag = False
      print("save_freq를 확인해주세요.")

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 12, weights_flag)

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 13, save_flag)

    if save_flag and weights_flag:
      print("callback을 잘 정의하셨습니다! 이어서 진행하셔도 좋습니다.")

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

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 14, opt_flag)

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 15, loss_flag)

    if opt_flag and loss_flag and metric_flag:
      print('compile을 잘 정의하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')

def accuracy_check(model):

  acc_flag = True

  try:
    acc = model.metrics[0].result()
    if acc < 0.75 :
      acc_flag = False
      print("Model Accuracy가 낮습니다. 하이퍼파라미터 숫자를 조절해보세요.")

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 16, acc_flag)

    if acc_flag:
      print('fit을 잘 정의하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')

def test_check(model):

  acc_flag = True

  try:
    acc = model.metrics[0].result()
    if acc < 0.70:
      acc_flag = False
      print("Test Accuracy가 낮습니다. Model의 구조와 Data Input, Output을 확인해주세요.")

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 17, acc_flag)

    if acc_flag:
      print('모델 성능이 기준치를 넘었습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')

def final_dense_check(new_model):
  flag = True
  all_dense_units = []

  try:
    for layer in new_model.layers:
      if 'dense' in layer.name:
        all_dense_units.append(layer.kernel.shape[-1])
  
    if all_dense_units[0] != 256:
      print('첫번째 dense layer의 출력 feature 수가 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.')
      flag = False
    if all_dense_units[1] != 2:
      print('마지막 dense layer의 출력 feature 수가 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.')
      flag = False
    
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 18, flag)
  
    if flag:
      print('dense layer 잘 수정하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')
