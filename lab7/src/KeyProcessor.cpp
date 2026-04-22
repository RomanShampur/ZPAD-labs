#include "KeyProcessor.hpp"

void KeyProcessor::updateMode(int keyPress) {
    if (keyPress == 'n' || keyPress == 'N') activeMode = WorkMode::DEFAULT;
    else if (keyPress == 'c' || keyPress == 'C') activeMode = WorkMode::CANNY;
    else if (keyPress == 'b' || keyPress == 'B') activeMode = WorkMode::BLUR;
    else if (keyPress == 'i' || keyPress == 'I') activeMode = WorkMode::INVERT;
    else if (keyPress == 'f' || keyPress == 'F') activeMode = WorkMode::FACE_DETECTION;
}
