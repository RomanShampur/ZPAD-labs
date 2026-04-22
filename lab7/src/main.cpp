#include <opencv2/opencv.hpp>
#include "CameraProvider.hpp"
#include "FrameProcessor.hpp"
#include "KeyProcessor.hpp"
#include "FaceDetector.hpp"

int main() {
    CameraProvider camera(0);
    FrameProcessor processor;
    KeyProcessor keys;
    FaceDetector detector;
    cv::Mat frame;

    while (true) {
        if (!camera.grabFrame(frame)) continue;

        if (keys.activeMode == KeyProcessor::WorkMode::FACE_DETECTION) {
            detector.pushData(frame);
            cv::Rect face = detector.fetchResult();
            if (face.width > 0) cv::rectangle(frame, face, {0, 255, 0}, 2);
        } else {
            processor.executeProcessing(frame, keys.activeMode);
        }

        cv::imshow("KPI Lab 7", frame);
        int k = cv::waitKey(1);
        if (k == 27) break;
        keys.updateMode(k);
    }
    return 0;
}
