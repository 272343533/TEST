import tensorflow as tf 
from tensorflow import keras
from keras.datasets import imdb
import numpy as np
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Embedding
from keras.layers import GlobalAveragePooling1D
#from plot import plot
"""
���ı���ʽ��Ӱ����Ϊ�����桱�򡰸��桱Ӱ��������һ����Ԫ���ࣨ�ֳ�Ϊ������ࣩ��ʾ����Ҳ��һ����Ҫ�ҹ㷺���õĻ���ѧϰ���⡣

TensorFlow �а��� IMDB ���ݼ��������ѶԸ����ݼ�������Ԥ����
��Ӱ�����ִ����У�ת��Ϊ�������У�����ÿ��������ʾ�ֵ��е�һ���ض��ִʡ�

https://blog.csdn.net/Feynman1999/article/details/84292840

"""

# ���� num_words=10000 �ᱣ��ѵ�������г���Ƶ����ǰ 10000 λ���ִʡ�Ϊȷ�����ݹ�ģ���ڿɹ����ˮƽ�������ִʽ���������
# imdb = keras.datasets.imdb
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

# ��һ��ѵ�����Ĵ�С
print("Training entries: {}, labels: {}".format(len(train_data), len(train_labels)))

# ��һ��ѵ����ɶ�� ������Ӱ�� һ�����ֶ�Ӧ�ֵ��е�һ������
print(train_data[0],'\n',len(train_data[0]))
print(train_data[1],'\n',len(train_data[1]))
print(type(train_data))
# ���Կ����ı��ĳ��Ȳ�����ͬ ��������һ����Ҫ��ͬά���������������� ������Կ�������취



# ������ת�����ִ�
word_index = imdb.get_word_index()
word_index = {k:(v+3) for k,v in word_index.items()}
word_index["<PAD>"] = 0  # û�г��ֵ��ֵ����еĴ�
word_index["<START>"] = 1# ��ʼ����
word_index["<UNK>"] = 2  # unknown
word_index["<UNUSED>"] = 3
# ��ȡ������-���ʡ���Ӧ�ֵ�
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

# ��ȡ������-���֡���Ӧ�ֵ�
change_word_index = dict([(key, value) for (key, value) in word_index.items()])

# ������ת��Ϊ�ı�
def decode_review(text):
    return ' '.join([reverse_word_index.get(i,'?') for i in text]) # ���ֵ���ȡ����Ӧ�ĵ���  û�о�ȡ'?'

# ���ı�ת��Ϊ����
def text_to_index(text, word_index):
    return ' '.join([word_index.get(word,'?') for word in text])

# ��IMDB���浽�ʻ��ļ�
def save_list(lines, filename):
	# convert lines to a single blob of text
	data = '\n'.join(lines)
	file = open(filename, 'w',encoding="utf-8")
	file.write(data)
	file.close()




#tokens = [str(key)+"|"+str(value) for (key, value) in word_index.items()]
tokens = [str(key) for (key, value) in word_index.items()]
print(len(tokens))
#save_list(tokens, r'E:\��ʱ���Գ���\pytest\vocab2.txt')





# �ʻ�����
def decode_review1(text):
    for i in text:
        a = reverse_word_index.get(i,'?')
        print(a)
    return ' '.join([reverse_word_index.get(i,'?') for i in text]) # ���ֵ���ȡ����Ӧ�ĵ���  û�о�ȡ'?'

#print(decode_review1(train_data[0]))

# test ������ת�����ִ�
print(decode_review(train_data[0]))








# Ϊ��ʹ���������ά����ͬ ����ȡmax_length��Ϊά��
# ���ǽ�ʹ�� pad_sequences ���������ȱ�׼��
train_data = keras.preprocessing.sequence.pad_sequences(train_data, 
                                                        value = word_index["<PAD>"],
                                                        padding='post',
                                                        maxlen=256)

test_data = keras.preprocessing.sequence.pad_sequences(test_data, 
                                                       value = word_index["<PAD>"],
                                                       padding='post',
                                                       maxlen=256)                            

#  �鿴����֮�������
print(train_data[0],'\n',len(train_data[0]))


# input shape is the vocabulary count used for the movie reviews (10,000 words)
vocab_size = 10000

model = keras.Sequential()
# �ò������������Ĵʻ���в���ÿ���ִ�-������Ƕ��������
# ģ���ڽ���ѵ��ʱ��ѧϰ��Щ��������Щ������������������һ��ά�ȡ�
model.add(Embedding(vocab_size,16)) # batch * sequence * 16
# ͨ��������ά����ƽ��ֵ�����ÿ����������һ�����ȹ̶������������
# ������ģ�ͱ��ܹ��Ծ����ܼ򵥵ķ�ʽ������ֳ��ȵ����롣
model.add(GlobalAveragePooling1D())
model.add(Dense(16, activation=tf.nn.relu))
model.add(Dense(1,activation=tf.nn.sigmoid))
model.summary() # ��һ��ģ�͵Ŀ��


# ģ����ѵ��ʱ��Ҫһ����ʧ������һ���Ż�������������һ����Ԫ��������
# ��ģ�ͻ����һ�����ʣ�Ӧ�� S �ͼ�����ĵ�����Ԫ�㣩��
# ������ǽ�ʹ�� binary_crossentropy ��ʧ������
model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# ��ԭʼѵ�������з���� 10000 ������������һ����֤��(validation)��
x_val = train_data[:10000]
partial_x_train = train_data[10000:]

y_val = train_labels[:10000]
partial_y_train = train_labels[10000:]

# ���� 512 ��������С����ѵ��ģ�� 40 �����ڡ��⽫�� x_train �� y_train �����е�������������
#  40 �ε�������ѵ���ڼ䣬���ģ������֤���� 10000 �������ϵ���ʧ��׼ȷ�ʣ�
history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=22,
                    batch_size=512,
                    validation_data=(x_val, y_val), # ʵʱ��֤
                    verbose=1)

# ����ģ��
results = model.evaluate(test_data, test_labels)
print(results)

# model.fit() ����һ�� History ���󣬸ö������һ���ֵ䣬���а���ѵ���ڼ䷢�������������
history_dict = history.history
print(history_dict.keys())

# ������һ���ļ���ĺ��� ������ͼ
# plot(history_dict)
