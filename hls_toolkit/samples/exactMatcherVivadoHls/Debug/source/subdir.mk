################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
OBJS += \
./source/exactMatcher.o 

CPP_DEPS += \
./source/exactMatcher.d 


# Each subdirectory must supply rules for building sources it contributes
source/exactMatcher.o: /home/nic30/Documents/workspace/hw_synthesis/hw_synthesis_helpers/hls_toolkit/samples/exactMatcherVivadoHls/src/exactMatcher.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -DAESL_TB -D__llvm__ -D__llvm__ -I/opt/Xilinx/Vivado_HLS/2015.2/lnx64/tools/auto_cc/include -I/opt/Xilinx/Vivado_HLS/2015.2/lnx64/tools/systemc/include -I/home/nic30/Documents/workspace/hw_synthesis/hw_synthesis_helpers/hls_toolkit/samples -I/opt/Xilinx/Vivado_HLS/2015.2/include/ap_sysc -I/opt/Xilinx/Vivado_HLS/2015.2/include/etc -I/opt/Xilinx/Vivado_HLS/2015.2/include -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


