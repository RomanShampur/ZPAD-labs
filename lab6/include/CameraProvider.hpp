#pragma once
#include <opencv2/opencv.hpp>

class CameraProvider {
    cv::VideoCapture cap;
public:
    CameraProvider(int deviceID = 0);
    bool getFrame(cv::Mat& frame);
};
