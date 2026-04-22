#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"

class FrameProcessor {
public:
    void process(cv::Mat& frame, ProcessMode mode);
private:
    void applyGlitch(cv::Mat& frame);
};
