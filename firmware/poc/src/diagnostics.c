#include "diagnostics.h"

#include <zephyr/drivers/gpio.h>
#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(poc_diag, LOG_LEVEL_INF);

#if DT_NODE_HAS_STATUS(DT_ALIAS(led0), okay)
static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios);
static bool led_ready;
#endif

void diagnostics_init(void)
{
	LOG_INF("%s v%s | board=%s", POC_APP_NAME, POC_APP_VERSION, CONFIG_BOARD);
#if DT_NODE_HAS_STATUS(DT_ALIAS(led0), okay)
	led_ready = gpio_is_ready_dt(&led) &&
		    gpio_pin_configure_dt(&led, GPIO_OUTPUT_INACTIVE) == 0;
	if (!led_ready) {
		LOG_WRN("Activity LED unavailable; console heartbeat remains active");
	}
#endif
}

void diagnostics_tick(void)
{
	LOG_INF("alive uptime_ms=%lld", (long long)k_uptime_get());
#if DT_NODE_HAS_STATUS(DT_ALIAS(led0), okay)
	if (led_ready && gpio_pin_toggle_dt(&led) != 0) {
		led_ready = false;
		LOG_WRN("Activity LED write failed");
	}
#endif
}
