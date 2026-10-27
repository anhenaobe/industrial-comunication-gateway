#include "diagnostics.h"
#include "network.h"

#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(poc_main, LOG_LEVEL_INF);

int main(void)
{
	int64_t next_alive = 0;
	bool network_ready;

	diagnostics_init();
	network_ready = poc_network_init() == 0;
	if (!network_ready) {
		LOG_ERR("Network setup failed; M0 heartbeat remains active");
	}
	for (;;) {
		int64_t now = k_uptime_get();

		if (now >= next_alive) {
			diagnostics_tick();
			next_alive = now + 1000;
		}
		if (network_ready) {
			poc_network_tick();
		}
		k_sleep(K_MSEC(100));
	}
	return 0;
}
