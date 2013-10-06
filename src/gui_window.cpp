#include <iostream>

#include <GL/glew.h>
#include <GL/glfw.h>
#include <glm/glm.hpp>


class GUIWindow
{
  int height;
  int widht;
  char *title;
public:
    int createWindow(std::string *title);
};

int GUIWindow::createWindow(std::string *title)
{
  int quit = 0;
  int window_closed = 0;

  if (!glfwInit()) {
    std::cerr << "Failed to initialize GLFW!" << std::endl;
    return -1;
  }

  glfwOpenWindowHint(GLFW_FSAA_SAMPLES, 4);  // 4x antialiasing

  // force latest opengl version
  // glfwOpenWindowHint(GLFW_OPENGL_VERSION_MAJOR, 3);
  // glfwOpenWindowHint(GLFW_OPENGL_VERSION_MINOR, 3);
  // glfwOpenWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

  // open a window and create its OpenGL context
  if (!glfwOpenWindow(1024, 768, 0, 0, 0, 0, 32, 0, GLFW_WINDOW)) {
      std::cerr << "Failed to open GLFW window!" << std::endl;
      glfwTerminate();
      return -1;
  }

  // initialize GLEW
  glewExperimental = true; // Needed in core profile
  glfwSetWindowTitle(title->c_str());
  glfwEnable(GLFW_STICKY_KEYS); // enable sticky keys such as ESC
  if (glewInit() != GLEW_OK) {
      std::cerr << "Failed to initialize GLEW!" << std::endl;
      return -1;
  }

  // while ESC key is not pressed or the window not closed
  while (quit == 0 && window_closed == 0) {
    glfwSwapBuffers();

    // break conditions
    quit = (glfwGetKey(GLFW_KEY_ESC) == GLFW_PRESS);
    window_closed = !(glfwGetWindowParam(GLFW_OPENED));
  }

  return 0;
}

int main()
{
  std::string *gui_title = new std::string("TESTING");
  GUIWindow *gui_window = new GUIWindow();

  gui_window->createWindow(gui_title);

  delete gui_window;
  delete gui_title;
  return 0;
}
