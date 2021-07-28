import cv2
import matplotlib.pyplot as plt
import numpy as np
import imageio
import glob

from scipy import ndimage
from skimage.data import shepp_logan_phantom
from skimage.transform import radon, rescale


class Mahdian_estimator:
    def __init__(self):
        self.roi_size = 128
        self.steps = 180
        self.window = 10
        self.threshold = 5


    def roi_selection(self, image):
        width, height = image
        roi_box = []

        for h in range(height - self.roi_size):
            for w in range(width - self.roi_size):
                roi_box.append(image[w:w + self.roi_size, h:h + self.roi_size])  # ROI (128x128)
        return roi_box


    def signal_deriv(self, data, flag):
        # 1차원 signal 2차미분
        if flag == 1:
            kernel = [1, -2, 1]
            conv_ = []
            for i in range(data.shape[0]):
                if i == 0:
                    conv_.append(data[i] * kernel[1] + data[i + 1] * kernel[2])
                elif i == data.shape[0] - 1:
                    conv_.append(data[i - 1] * kernel[0] + data[i] * kernel[1])
                else:
                    conv_.append(data[i - 1] * kernel[0] + data[i] * kernel[1] + data[i + 1] * kernel[2])
            result = conv_

        # 2차원 signal 2차미분
        else:
            result = cv2.Laplacian(data, cv2.CV_8U, ksize=3)

        return result


    def radon_trans(self, data):
        res = np.zeros((len(data[0]), self.steps), dtype='float64')
        for s in range(self.steps):
            rotation = ndimage.rotate(data, -s * 180 / self.steps, reshape=False).astype('float64')
            res[:, s] = sum(rotation)
        return res


    def autocovariance(self, data):
        total_r_p = {}
        for s in range(self.steps):
            # signal 2차미분 수행
            p_t = self.signal_deriv(data[:, s], 1)

            # search for periodicity
            m = np.mean(p_t)
            r_p = []
            for k in range(len(p_t) // 2):
                sum_ = 0
                for i in range(len(p_t) // 2):
                    sum_ += (p_t[(i + k)] - m) * (p_t[i] - m)
                r_p.append(sum_)  # k에 대하여 r_p (len(k), len(i))

            total_r_p[s] = r_p  # theta에 대하여 total_r_p {(theta): [(k),(i)]}

        return total_r_p


    def fft(self, data):
        f_s = []
        for s in range(self.steps):
            f = abs(np.fft.fft(data[s]))
            f_s.append(np.fft.fftshift(f))

        return f_s


    def find_peak(self, data):
        index = len(data[0])
        peak_angle = []

        for t in range(self.steps):
            value = np.array(data[t])

            for i in range(index):
                if i + self.window <= index:
                    m = np.mean(value[i:i + self.window])
                if value[i] > (m * self.threshold):
                    peak_angle.append(t)

        peak_angle = list(set(peak_angle))
        peak_angle.sort()
        return peak_angle



if __name__ == '__main__':

    file_name = glob.glob('./assets/captured_image/*.*')
    whole_acc = []

    for i in range(5):
        suc_detection = []
        for img_name in file_name:
            # 적용할 이미지 불러오기
            img = cv2.imread(img_name)
            b, g, r = cv2.split(img)
            img = cv2.merge([r, g, b])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # JPEG compression
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 97]
            result, encimg = cv2.imencode('.jpg', img, encode_param)

            if False == result:
                print('could not encode image!')
                quit()

            # decode from jpeg format
            img = cv2.imdecode(encimg, 1)

            # 이미지 변환하기
            # 1. resize
            factor = 0.55 + (0.5*i)
            img = cv2.resize(img, dsize=(0, 0), fx=factor, fy=factor, interpolation=cv2.INTER_LINEAR)

            # 2. rotation
            # rotation_angle = 1
            # height, width = img.shape
            # matrix = cv2.getRotationMatrix2D((width / 2, height / 2), rotation_angle, 1)
            # img = cv2.warpAffine(img, matrix, (width, height))

            # 3. skewing



            # Mahdian estimator
            estimator = Mahdian_estimator()
            deri_img = estimator.signal_deriv(img, flag=2)  # step2. derivative
            sinogram = estimator.radon_trans(deri_img)  # step3. radon transform
            r_p = estimator.autocovariance(sinogram)  # step4. auto-covariance
            s_fft = estimator.fft(r_p)  # step5. fft
            peak = estimator.find_peak(s_fft)  # step6. find 2 peaks


            if len(peak) >= 2:
                suc_detection.append(img_name)

        print(f'{factor}-detection acc: {len(suc_detection)/len(file_name)}')
        whole_acc.append((factor, len(suc_detection)/len(file_name)))



    # # show results
    # plt.figure(figsize=(25, 6))
    #
    # plt.subplot(211)
    # plt.plot(s_fft[peak[0]])
    # plt.title("theta: {}".format(peak[0]))
    #
    # plt.subplot(212)
    # plt.plot(s_fft[peak[1]])
    # plt.title("theta: {}".format(peak[1]))
    #
    # plt.show()






