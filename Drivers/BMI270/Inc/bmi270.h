#ifndef BMI270_H
#define BMI270_H

#include "main.h"
#include <stdio.h>
#include <stdint.h>
#include <stddef.h>

int bmi270_init_hc(I2C_HandleTypeDef *hi2c);
int bmi270_write(I2C_HandleTypeDef *hi2c, uint16_t memAddr,
		const uint8_t *pData, uint16_t size);
int bmi270_read(I2C_HandleTypeDef *hi2c, uint16_t memAddr, uint8_t *pData,
		uint16_t size);
int bmi270_write_byte(I2C_HandleTypeDef *hi2c, uint16_t memAddr, uint8_t byte);
int bmi270_read_byte(I2C_HandleTypeDef *hi2c, uint16_t memAddr, uint8_t *byte);

#endif
