#include <opencv2/opencv.hpp>
#include "CameraProvider.hpp"
#include "FrameProcessor.hpp"
#include "KeyProcessor.hpp"

int main() {
    CameraProvider cam(0);
    FrameProcessor processor;
    KeyProcessor keys;
    cv::Mat frame;

    cv::namedWindow("Lab 3 - OpenCV");

    while (true) {
        if (!cam.getFrame(frame)) break;

        processor.process(frame, keys.currentMode);
        
        cv::putText(frame, "Mode: " + std::to_string((int)keys.currentMode), 
                    {20, 40}, cv::FONT_HERSHEY_SIMPLEX, 1, {0, 255, 0}, 2);

        cv::imshow("Lab 3 - OpenCV", frame);

        int k = cv::waitKey(30);
        if (k == 27) break; // ESC to exit
        keys.process(k);
    }
    return 0;
}
