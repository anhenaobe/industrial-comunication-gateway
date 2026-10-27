cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(gateway_poc VERSION 0.1.0 LANGUAGES C)

target_sources(app PRIVATE src/main.c src/diagnostics.c src/network.c)
target_compile_options(app PRIVATE -Wall -Wextra -Werror)
