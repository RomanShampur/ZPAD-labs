#include "CameraProvider.hpp"

CameraProvider::CameraProvider(int deviceIndex) {
    videoSource.open(deviceIndex);
}

bool CameraProvider::grabFrame(cv::Mat& output) {
    if (!videoSource.isOpened()) return false;
    return videoSource.read(output);
}
