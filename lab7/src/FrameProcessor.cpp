#include "FrameProcessor.hpp"

void FrameProcessor::executeProcessing(cv::Mat& frame, KeyProcessor::WorkMode mode) {
    if (frame.empty()) return;
    
    if (mode == KeyProcessor::WorkMode::CANNY) {
        cv::cvtColor(frame, frame, cv::COLOR_BGR2GRAY);
        cv::Canny(frame, frame, 100, 200);
        cv::cvtColor(frame, frame, cv::COLOR_GRAY2BGR);
    } else if (mode == KeyProcessor::WorkMode::BLUR) {
        cv::GaussianBlur(frame, frame, cv::Size(15, 15), 0);
    } else if (mode == KeyProcessor::WorkMode::INVERT) {
        cv::bitwise_not(frame, frame);
    }
}
