#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"

class FrameProcessor {
public:
    void executeProcessing(cv::Mat& frame, KeyProcessor::WorkMode mode);
};
