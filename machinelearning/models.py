import nn


class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):

        #Tính điểm do perceptron ấn định cho một điểm dữ liệu x
        return nn.DotProduct(self.w, x)

    def get_prediction(self, x):
        #Tính tích vô hướng cho một điểm dữ liệu
        if nn.as_scalar(self.run(x)) >= 0.0:
            return 1
        else:
            return -1

    def train(self, dataset):
        #Đào tạo perceptron cho đến khi hội tụ
        while True:
            flag = True
            batchsize = 1
            for x, y in dataset.iterate_once(batchsize):
                y = nn.as_scalar(y)
                if self.get_prediction(x) != y:
                    flag = False
                    self.w.update(x, y)
            if flag:
                break


class RegressionModel(object):
    def __init__(self):
        # Khởi tạo tham số mô hình
        self.w1 = nn.Parameter(1, 50)
        self.w2 = nn.Parameter(50, 30)
        self.w3 = nn.Parameter(30, 1)
        self.b1 = nn.Parameter(1, 50)
        self.b2 = nn.Parameter(1, 30)
        self.b3 = nn.Parameter(1, 1)

    def run(self, x):
        #Chạy mô hình cho một loạt các ví dụ
        feature_1_linear = nn.Linear(x, self.w1)
        feature_1_addbias = nn.AddBias(feature_1_linear, self.b1)
        feature_1_relu = nn.ReLU(feature_1_addbias)
        second = nn.ReLU(
            nn.AddBias(nn.Linear(feature_1_relu, self.w2), self.b2))
        third = nn.AddBias(nn.Linear(second, self.w3), self.b3)
        return third

    def get_loss(self, x, y):
        #Tính toán tổn thất các ví dụ trên
        check = self.run(x)
        return nn.SquareLoss(check, y)
        ""

    def train(self, dataset):
        # Train mô hình
        while True:
            batch = 4
            learningrate = -0.05
            for (x, y) in dataset.iterate_once(batch):
                loss = self.get_loss(x, y)
                result = nn.gradients(
                    loss,
                    [self.w1, self.b1, self.w2, self.b2, self.w3, self.b3])
                self.w1.update(result[0], learningrate)
                self.b1.update(result[1], learningrate)
                self.w2.update(result[2], learningrate)
                self.b2.update(result[3], learningrate)
                self.w3.update(result[4], learningrate)
                self.b3.update(result[5], learningrate)
            if nn.as_scalar(loss) < 0.002:
                break


class DigitClassificationModel(object):
    def __init__(self):
        # Khởi tạo tham số mô hình
        self.w1 = nn.Parameter(784, 200)
        self.b1 = nn.Parameter(1, 200)
        self.w2 = nn.Parameter(200, 100)
        self.b2 = nn.Parameter(1, 100)
        self.w3 = nn.Parameter(100, 10)
        self.b3 = nn.Parameter(1, 10)


    def run(self, x):
        #Chạy mô hình cho các ví dụ
        layer1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        layer2 = nn.ReLU(nn.AddBias(nn.Linear(layer1, self.w2), self.b2))
        layer3 = nn.AddBias(nn.Linear(layer2, self.w3), self.b3)

        return layer3

    def get_loss(self, x, y):
        #Tính toán tổn thất các ví dụ trên
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        #Train mô hình
        learningrate = -0.08
        batch_size = 10
        while True:
            for x, y in dataset.iterate_once(batch_size):
                loss = self.get_loss(x, y)
                grad = nn.gradients(loss, [
                    self.w1, self.w2, self.w3,self.b1, self.b2,self.b3
                ])
                self.w1.update(grad[0], learningrate)
                self.w2.update(grad[1], learningrate)
                self.w3.update(grad[2], learningrate)
                self.b1.update(grad[3], learningrate)
                self.b2.update(grad[4], learningrate)
                self.b3.update(grad[5], learningrate)
            print(dataset.get_validation_accuracy())
            if dataset.get_validation_accuracy() >= 0.975:
                return


class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Khởi tạo tham số mô hình
        self.i_w = nn.Parameter(self.num_chars, 256)
        self.i_b = nn.Parameter(1, 256)
        self.x_w = nn.Parameter(self.num_chars, 256)
        self.h_w = nn.Parameter(256, 256)
        self.b = nn.Parameter(1, 256)
        self.out_w = nn.Parameter(256, len(self.languages))
        self.out_b = nn.Parameter(1, len(self.languages))

    def run(self, xs):
        #Chạy mô hình cho các ví dụ
        h_i = nn.ReLU(nn.AddBias(nn.Linear(xs[0], self.i_w), self.i_b))
        for char in xs[1:]:
            h_i = nn.ReLU(nn.AddBias(nn.Add(nn.Linear(char, self.x_w),nn.Linear(h_i, self.h_w)), self.b))
        output = nn.AddBias(nn.Linear(h_i, self.out_w), self.out_b)
        return output

    def get_loss(self, xs, y):
        # Tính toán tổn thất các ví dụ trên
        y_hat = self.run(xs)
        return nn.SoftmaxLoss(y_hat, y)

    def train(self, dataset):
        # Train mô hình
        learningrate=-0.1
        batch_size=100
        while True:
            for x, y in dataset.iterate_once(batch_size):
                loss = self.get_loss(x,y)
                grad = nn.gradients(loss, [self.i_w, self.i_b, self.x_w,self.h_w,self.b,self.out_w,self.out_b])
                self.i_w.update(grad[0], learningrate)
                self.i_b.update(grad[1], learningrate)
                self.x_w.update(grad[2], learningrate)
                self.h_w.update(grad[3], learningrate)
                self.b.update(grad[4], learningrate)
                self.out_w.update(grad[5], learningrate)
                self.out_b.update(grad[6], learningrate)

            print(dataset.get_validation_accuracy())
            if dataset.get_validation_accuracy() >= 0.86:
                return
