#include "FrameProcessor.hpp"

void FrameProcessor::process(cv::Mat& frame, ProcessMode mode) {
    switch (mode) {
        case ProcessMode::CANNY:
            cv::cvtColor(frame, frame, cv::COLOR_BGR2GRAY);
            cv::Canny(frame, frame, 100, 200);
            cv::cvtColor(frame, frame, cv::COLOR_GRAY2BGR);
            break;
        case ProcessMode::BLUR:
            cv::GaussianBlur(frame, frame, cv::Size(15, 15), 0);
            break;
        case ProcessMode::INVERT:
            cv::bitwise_not(frame, frame);
            break;
        case ProcessMode::GLITCH:
            applyGlitch(frame);
            break;
        default: break;
    }
}

void FrameProcessor::applyGlitch(cv::Mat& frame) {
    std::vector<cv::Mat> channels;
    cv::split(frame, channels);
    // Зсуваємо канали для ефекту глітчу
    cv::copyMakeBorder(channels[0], channels[0], 0, 0, 10, 0, cv::BORDER_REPLICATE);
    channels[0] = channels[0](cv::Rect(0, 0, frame.cols, frame.rows));
    cv::merge(channels, frame);
}
