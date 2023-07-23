Audio Visualizer

The Audio Visualizer is a Python application that captures audio from the default input device and provides a real-time visualization of the audio waveform. It utilizes the PyQt5 and PyAudio libraries to create the graphical user interface and process the audio data.
Usage

    Install the required dependencies:
        PyQt5
        PyAudio
        NumPy
        Matplotlib

    Launch the application by running the Python script.

    The Audio Visualizer window will appear on the screen, displaying the live audio waveform.

Features

    Real-time visualization: The application continuously captures audio from the default input device and updates the graphical representation of the audio waveform in real-time.

    Draggable window: The application window can be moved by clicking and dragging it with the left mouse button.

    Frameless window: The window is frameless, providing a clean and minimalistic interface.

    Always on top: The application window always stays on top of other windows, ensuring that the audio visualization is readily visible.

    Dark theme: The application window adopts a dark theme, creating an aesthetically pleasing and immersive visual experience.

Configuration

The application provides a few customizable parameters:

    Audio capture settings: The CHUNK, FORMAT, CHANNELS, and RATE constants can be modified to adjust the audio capture settings according to your preferences or requirements.

    Update interval: The update_visualizer method is responsible for updating the audio visualization. The update interval is currently set to 1 millisecond (1ms). Adjust this value to control the refresh rate of the visualization.

    Window size: The initial size of the application window is set to 20% of the screen width and 20% of the screen height. You can modify this to suit your display preferences.

License

Borrowed stuff from MIT - so probably under MIT license.
