#include "CameraProvider.hpp"

CameraProvider::CameraProvider(int deviceID) {
    cap.open(deviceID);
}
bool CameraProvider::getFrame(cv::Mat& frame) {
    return cap.read(frame);
}
