#include "bmi270.h"
#include "bmi270_hw.h"

#define I2C_INT_TIMEOUT_MS 100

// 0 means i2c busy, 1 means i2c complete
static volatile uint8_t i2c_done = 0;

// 0 means no error. HAL_I2C_ErrorCallback updates this value on an error
static volatile uint32_t i2c_err = 0;

/*
 * i2c_wait: Intended to be used as a busy wait, but in our driver layer,
 * so that when this becomes rtos aware, we can deal with it more easily than with
 * polling.
 * Basically, if the i2c bus is dead for however long time timeout is, we abort
 * the transaction.
 */
static int i2c_wait(I2C_HandleTypeDef *hi2c) {
	uint32_t start = HAL_GetTick();
	while (!i2c_done) {
		if ((HAL_GetTick() - start > I2C_INT_TIMEOUT_MS) || i2c_err != 0) {
			HAL_I2C_Master_Abort_IT(hi2c, (BMI270_I2C_DEFAULT_ID << 1));
			return -1;
		}
	}
	return 0;
}

// hardcoded bmi270 init
int bmi270_init_hc(I2C_HandleTypeDef *hi2c) {
	uint8_t byte_data = 0x00;

	bmi270_write_byte(hi2c, (BMI270_I2C_DEFAULT_ID << 1), byte_data);

	bmi270_read_byte(hi2c, (BMI270_I2C_DEFAULT_ID << 1), &byte_data);

	printf("Ret val: %x\r\n", byte_data);
	return 0;
}

int bmi270_write_byte(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, uint8_t byte) {
	i2c_err = 0;
	i2c_done = 0;
	HAL_I2C_Master_Transmit_IT(hi2c, DevAddress, &byte, 1);
	if (i2c_wait(hi2c) == -1) {
		printf("I2C aborted during bmi270_write_byte(). Possible error: %ld \r\n", i2c_err);
		return -1;
	}
	return 0;
}

int bmi270_read_byte(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, uint8_t *byte) {
	i2c_err = 0;
	i2c_done = 0;
	HAL_I2C_Master_Receive_IT(hi2c, DevAddress, byte, 1);
	if (i2c_wait(hi2c) == -1) {
		printf("I2C aborted during bmi270_read_byte(). Possible error: %ld \r\n", i2c_err);
		return -1;
	}
	return 0;
}

void HAL_I2C_MasterTxCpltCallback(I2C_HandleTypeDef * hi2c) {
	i2c_done = 1;
}

//
void HAL_I2C_MasterRxCpltCallback(I2C_HandleTypeDef * hi2c) {
	i2c_done = 1;
}

// HAL callback for transfer errors
void HAL_I2C_ErrorCallback(I2C_HandleTypeDef * hi2c) {
	i2c_done = 1;
	i2c_err = HAL_I2C_GetError(hi2c);
}

// HAL callback for HAL_I2C_Master_Abort_IT()
void HAL_I2C_AbortCpltCallback(I2C_HandleTypeDef * hi2c) {
	printf("I2C Aborted.\r\n");
}

