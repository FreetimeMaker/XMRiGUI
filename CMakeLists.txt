cmake_minimum_required (VERSION 4.3)

project ("XMRiGUI")

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Qt6
find_package(Qt6 REQUIRED COMPONENTS Widgets Gui Core Network)
qt_standard_project_setup()

# Define source files
set(PROJECT_SOURCES
    "XMRiGUI.cpp"
    "XMRiGUI.h"
)

# Add executable
qt_add_executable(XMRiGUI ${PROJECT_SOURCES})

# Target properties
if(WIN32)
    set_target_properties(XMRiGUI PROPERTIES WIN32_EXECUTABLE TRUE)
endif()

# Link libraries
target_link_libraries(XMRiGUI PRIVATE Qt6::Widgets Qt6::Gui Qt6::Core Qt6::Network)

# Assets kopieren (optional, falls du sie im Build-Ordner haben willst)
if(WIN32)
    set(WIN_ASSET_DIR "C:/Users/jamie/OneDrive/Documentos/datasaver/Git/XMRiGUI Windows")
    if(EXISTS ${WIN_ASSET_DIR})
        file(COPY "${WIN_ASSET_DIR}/xmrigui.png" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
    endif()
else()
    set(LIN_ASSET_DIR "C:/Users/jamie/OneDrive/Documentos/datasaver/Git/XMRiGUI")
    if(EXISTS ${LIN_ASSET_DIR})
        file(COPY "${LIN_ASSET_DIR}/xmrigui.png" DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
    endif()
endif()
