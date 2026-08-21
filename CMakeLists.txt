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

# Install rules
if(UNIX AND NOT APPLE)
    install(TARGETS XMRiGUI DESTINATION bin)
    install(FILES linux/xmrigui.desktop DESTINATION share/applications)
    install(FILES xmrigui.png DESTINATION share/icons/hicolor/256x256/apps)

    # Optionally install the bundled xmrig if it exists
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/linux/xmrig")
        install(PROGRAMS linux/xmrig DESTINATION bin)
    endif()
endif()

# Packaging (CPack)
set(CPACK_PACKAGE_NAME "xmrigui")
set(CPACK_PACKAGE_VENDOR "FreetimeMaker")
set(CPACK_PACKAGE_CONTACT "https://github.com/FreetimeMaker/XMRiGUI")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "A modern GUI for XMRig and other miners")
set(CPACK_PACKAGE_VERSION "1.8.0")
set(CPACK_RESOURCE_FILE_README "${CMAKE_CURRENT_SOURCE_DIR}/README.md")

if(UNIX AND NOT APPLE)
    set(CPACK_GENERATOR "DEB;RPM")

    # Debian specific
    set(CPACK_DEBIAN_PACKAGE_MAINTAINER "FreetimeMaker")
    set(CPACK_DEBIAN_PACKAGE_DEPENDS "libqt6widgets6, libqt6gui6, libqt6core6, libqt6network6")

    # RPM specific
    set(CPACK_RPM_PACKAGE_REQUIRES "qt6-qtbase-gui, qt6-qtbase")
endif()

include(CPack)

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
