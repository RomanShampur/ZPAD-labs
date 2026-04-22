#pragma once
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <thread>
#include <mutex>
#include <atomic>

class FaceDetector {
public:
    FaceDetector();
    ~FaceDetector();
    void pushData(const cv::Mat& src);
    cv::Rect fetchResult();

private:
    void recognitionTask();
    cv::dnn::Net detectorNet;
    std::thread worker;
    std::mutex dataMtx;
    std::atomic<bool> isRunning{true};
    cv::Mat frameBuffer;
    cv::Rect foundRect;
};
