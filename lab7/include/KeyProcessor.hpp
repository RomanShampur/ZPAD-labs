#pragma once

class KeyProcessor {
public:
    enum class WorkMode { DEFAULT, CANNY, BLUR, INVERT, FACE_DETECTION };
    WorkMode activeMode = WorkMode::DEFAULT;
    
    void updateMode(int keyPress);
};
