#include "KeyProcessor.hpp"

KeyProcessor::KeyProcessor() : currentMode(NORMAL) {}

void KeyProcessor::processKey(int key) {
    switch (key) {
        case '1': currentMode = NORMAL; break;
        case '2': currentMode = INVERT; break;
        case '3': currentMode = BLUR; break;
        case '4': currentMode = CANNY; break;
        case '5': currentMode = GRAY; break;
    }
}

KeyProcessor::Mode KeyProcessor::getMode() {
    return currentMode;
}
