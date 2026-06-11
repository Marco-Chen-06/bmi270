#ifndef BMI270_H
#define BMI270_H

#include "main.h"
#include <stdio.h>
#include <stdint.h>

int bmi270_init_hc(I2C_HandleTypeDef *hi2c);
int bmi270_write_byte(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, uint8_t byte);
int bmi270_read_byte(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, uint8_t *byte);

#endif
