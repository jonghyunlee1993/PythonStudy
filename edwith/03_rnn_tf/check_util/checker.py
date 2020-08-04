import tensorflow as tf
import codecs
import csv


file_path = './check_util/rnn_submission.tsv'
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

def version(num):

  if num != '2.0.0':
    print("TensorFlow 버전이 2.0.0 이 아닙니다.")
    print("!pip install tensorflow==2.0.0 으로 버전을 맞춰주세요.")
    print("자세한 설치 방법은 https://www.tensorflow.org/install 을 참고하세요.")
  else:
    print("TensorFlow 2.0.0 버전을 사용하고 있습니다.")

def customized_dataset_check(dataset):

  example = next(iter(dataset))

  try:
    flag = True
    sequences_shape = example[0].shape
    if len(sequences_shape) != 3:
      print('dataset의 input seqeuences shape이 올바르지 않습니다. 지문을 다시 확인하시기 바랍니다.')
      flag = False
    targets_shape = example[1].shape
    if len(targets_shape) != 1:
      print('dataset의 target seqeuences shape이 올바르지 않습니다. 지문을 다시 확인하시기 바랍니다.')
      flag = False

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 1, flag)

    if flag:
      print('tf.data.Dataset을 잘 구현하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')


def model_check(model):
  try:
    lstm_flag = True
    dense_flag = True
    all_rnn_shapes = []
    all_dense_num_features = []

    for layer in model.layers:
      if 'lstm' in layer.name:
        all_rnn_shapes.append(layer.weights[0].shape)
      if 'dense' in layer.name:
        all_dense_num_features.append(layer.weights[0].shape)

    if len(all_rnn_shapes) != 2:
      print('LSTM의 layer 갯수가 올바르지 않습니다. 지문을 다시 확인하시기 바랍니다.')
      lstm_flag = False

    if all_rnn_shapes[0][0] != 9:
      print('LSTM input shape이 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.')
      lstm_flag = False

    if all_rnn_shapes[0][1] != 100 * 4:
      print('첫번째 LSTM layer의 output shape이 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.')
      lstm_flag = False

    if all_rnn_shapes[1][1] != 100 * 4:
      print('두번째 LSTM layer의 output shape이 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.')
      lstm_flag = False

    if len(all_dense_num_features) != 1:
      print('Dense layer 갯수가 올바르지 않습니다. 지문을 다시 확인하시기 바랍니다.')
      dense_flag = False

    if all_dense_num_features[0][1] != 1:
      print('Dense layer의 output shape이 잘못되었습니다. 지문을 다시 확인하시기 바랍니다.')
      dense_flag = False

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 2, lstm_flag)
    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 3, dense_flag)

    if lstm_flag and dense_flag:
      print('네트워크를 잘 구현하셨습니다! 이어서 진행하셔도 좋습니다.')
      print('''같은 모델을 class형식으로 짜면 다음과 같이 짤 수 있습니다.

class my_model(tf.keras.Model):
    def __init__(self, hidden_sizes):
        super(my_model, self).__init__(name = '')
        self.lstm_a = layers.LSTM(hidden_sizes[0], return_sequences = True)
        self.lstm_b = layers.LSTM(hidden_sizes[-1], return_sequences = False)
        self.dense = layers.Dense(1)
        
    def call(self, input_tensor, training = False):
        x = self.lstm_a(input_tensor)
        x = self.lstm_b(x)
        x = self.dense(x)
        
        return x
''')

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
      submission_csv_write(wr, lines, 4, weights_flag)

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 5, save_flag)

    if save_flag and weights_flag:
      print("callback을 잘 정의하셨습니다! 이어서 진행하셔도 좋습니다.")

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')

def compile_check(model):

  opt_flag = True
  loss_flag = True

  try:
    opt = str(model.optimizer)
    loss = model.loss

    if 'adam' not in opt:
      opt_flag = False
      print('optimizer를 확인해주세요.')
    if 'mean' not in str(str(model.loss).lower()) and 'mse' not in str(model.loss).lower():
      loss_flag = False
      print('loss를 확인해주세요.')

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 6, loss_flag)

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 7, opt_flag)

    if opt_flag and loss_flag :
      print('compile을 잘 정의하셨습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')

def performance_check(test, base):

  per_flag = True

  try:
    if test > base:
      per_flag = False
      print("Baseline 보다 성능이 낮습니다. 모델 학습을 확인해주세요.")

    with codecs.open(file_path, 'w', encoding='utf-8', errors='replace') as f:
      wr = csv.writer(f, delimiter='\t')
      submission_csv_write(wr, lines, 8, per_flag)

    if per_flag:
      print('Model 성능이 Baseline 보다 좋습니다! 이어서 진행하셔도 좋습니다.')

  except:
    print('체크 함수를 실행하는 도중에 문제가 발생했습니다. 코드 구현을 완료했는지 다시 검토하시기 바랍니다.')
