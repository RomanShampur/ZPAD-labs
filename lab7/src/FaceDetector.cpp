#include "FaceDetector.hpp"

FaceDetector::FaceDetector() {
    detectorNet = cv::dnn::readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel");
    worker = std::thread(&FaceDetector::recognitionTask, this);
}

FaceDetector::~FaceDetector() {
    isRunning = false;
    if (worker.joinable()) worker.join();
}

void FaceDetector::pushData(const cv::Mat& src) {
    std::lock_guard<std::mutex> lock(dataMtx);
    src.copyTo(frameBuffer);
}

cv::Rect FaceDetector::fetchResult() {
    std::lock_guard<std::mutex> lock(dataMtx);
    return foundRect;
}

void FaceDetector::recognitionTask() {
    while (isRunning) {
        cv::Mat input;
        {
            std::lock_guard<std::mutex> lock(dataMtx);
            if (frameBuffer.empty()) continue;
            frameBuffer.copyTo(input);
        }
        cv::Mat blob = cv::dnn::blobFromImage(input, 1.0, cv::Size(300, 300), cv::Scalar(104, 177, 123));
        detectorNet.setInput(blob);
        cv::Mat output = detectorNet.forward();
        cv::Mat results(output.size[2], output.size[3], CV_32F, output.ptr<float>());

        bool found = false;
        for (int i = 0; i < results.rows; i++) {
            if (results.at<float>(i, 2) > 0.5) {
                int x1 = results.at<float>(i, 3) * input.cols;
                int y1 = results.at<float>(i, 4) * input.rows;
                int x2 = results.at<float>(i, 5) * input.cols;
                int y2 = results.at<float>(i, 6) * input.rows;
                std::lock_guard<std::mutex> lock(dataMtx);
                foundRect = cv::Rect(cv::Point(x1, y1), cv::Point(x2, y2));
                found = true;
                break;
            }
        }
        if (!found) {
            std::lock_guard<std::mutex> lock(dataMtx);
            foundRect = cv::Rect(0,0,0,0);
        }
    }
}
