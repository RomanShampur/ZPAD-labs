#pragma once
#include <opencv2/opencv.hpp>

class CameraProvider {
public:
    CameraProvider(int deviceIndex);
    bool grabFrame(cv::Mat& output);
private:
    cv::VideoCapture videoSource;
};
