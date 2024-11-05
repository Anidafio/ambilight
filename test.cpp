//do not work
#include <dxcam/dxcam.h>
#include <chrono>
#include <iostream>

void testCapturePerformance(int frames) {
    dxcam::DXCam camera;  // Initialize DXCam
    camera.start();       // Start the camera capture

    auto start_time = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < frames; ++i) {
        auto frame = camera.grab();  // Capture frame from GPU
        if (!frame.data) {
            std::cerr << "Failed to capture frame " << i << std::endl;
            continue;
        }
        // Optionally save one frame for verification (uncomment to save)
        /*
        if (i == rand() % frames) {
            frame.save("random_screenshot.png");
            std::cout << "Saved a screenshot at frame " << i << " as 'random_screenshot.png'\n";
        }
        */
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed_time = end_time - start_time;

    std::cout << "Time to capture " << frames << " frames: " << elapsed_time.count() << " seconds" << std::endl;
    std::cout << "Average time per frame: " << (elapsed_time.count() / frames) << " seconds" << std::endl;
    std::cout << "Average FPS: " << (frames / elapsed_time.count()) << " FPS" << std::endl;

    camera.stop();  // Stop the camera capture
}

int main() {
    int frames = 30;  // Number of frames to capture
    testCapturePerformance(frames);
    return 0;
}