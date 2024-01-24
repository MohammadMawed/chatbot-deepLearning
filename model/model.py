import tflearn
import tensorflow as tf

def build_and_train_model(train_x, train_y, model_file):
    tf.compat.v1.reset_default_graph()
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
    model.save(model_file)
    return model

def load_model(model_file, train_x, train_y):
    tf.compat.v1.reset_default_graph()
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    try:
        model.load(model_file)
    except:
        model = build_and_train_model(train_x, train_y, model_file)
    return model
