# Image forgery detection

> Watch your Up-Convolution: CNN Based Generative Deep Neural Networks are Failing to Reproduce Spectral Distributions (CVPR 2020)
> https://openaccess.thecvf.com/content_CVPR_2020/html/Durall_Watch_Your_Up-Convolution_CNN_Based_Generative_Deep_Neural_Networks_Are_CVPR_2020_paper.html

- [Watch your Up-Convolution 정리](https://github.com/Sang-Yeong/Research/blob/master/watch_your_up_conv.pdf)
- [Azimuth Integral 구현](https://github.com/Sang-Yeong/Research/blob/master/Azimuth_integral.ipynb)
- Idea
	- GAN, AE 와 같은 생성석 신경망; Up-Convolution 기법 사용
		- 보간을 이용한 up-conv
		- 전치된 conv
    - Up-Conv이 **스펙트럼 왜곡을 유발**한다는 사실 발견 --> 딥페이크 검출기 제안
    - 스펙트럼 왜곡을 보정할 수 있는 Spectral Reularization 제안
    	- --> GAN 모델 안정화 & 시각적 출력 품질 향상

<img src='./git_assets/watch_your_up_conv.JPG' width=700>


- Keyword
	1. Sampling method
	2. Frequency domain
	3. Fourier Transform
	4. Azimuth Integral

---


> Exposing digital forgeries by detecting traces of resampling
> https://ieeexplore.ieee.org/document/1381775

- Idea
	- 이미지 위조 --> 이미지의 기본 통계 변화 분석
	- interpolated signals & their derivatives ← 감지 가능한 **특정 주기 속성** 존재

- Resampling signals
이웃 픽셀과의 상관성을 갖는 주기적 sample을 찾음으로써 detect 가능
<img src='./git_assets/resampling_singals.JPG' width=700>

- Resampling Images
<img src='./git_assets/resampling_images.JPG' width=700>