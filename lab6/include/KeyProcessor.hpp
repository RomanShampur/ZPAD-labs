#pragma once
#include <opencv2/opencv.hpp>

enum class ProcessMode { NORMAL, CANNY, BLUR, INVERT, GLITCH };

class KeyProcessor {
public:
    ProcessMode currentMode = ProcessMode::NORMAL;
    void process(int key) {
        if (key == 'n' || key == 'N') currentMode = ProcessMode::NORMAL;
        else if (key == 'c' || key == 'C') currentMode = ProcessMode::CANNY;
        else if (key == 'b' || key == 'B') currentMode = ProcessMode::BLUR;
        else if (key == 'i' || key == 'I') currentMode = ProcessMode::INVERT;
        else if (key == 'g' || key == 'G') currentMode = ProcessMode::GLITCH;
    }
};
