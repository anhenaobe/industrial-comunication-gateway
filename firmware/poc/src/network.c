#include "network.h"
#include "diagnostics.h"

#include <errno.h>
#include <stdint.h>
#include <string.h>
#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>
#include <zephyr/net/net_if.h>
#include <zephyr/net/dhcpv4.h>
#include <zephyr/net/ethernet.h>
#include <zephyr/net/socket.h>
#include <zephyr/sys/printk.h>

LOG_MODULE_REGISTER(poc_net, LOG_LEVEL_INF);

static struct net_if *iface;
static struct sockaddr_in peer;
static int udp_socket = -1;
static bool destination_set;
static int last_state = -1;
static uint32_t sequence;
static int64_t next_send;
static uint32_t last_ipv4;

static void close_socket(void)
{
	if (udp_socket >= 0) {
		(void)zsock_close(udp_socket);
		udp_socket = -1;
	}
}

int poc_network_init(void)
{
	iface = net_if_get_first_by_type(&NET_L2_GET_NAME(ETHERNET));
	if (iface == NULL || !device_is_ready(net_if_get_device(iface))) {
		LOG_ERR("Ethernet device unavailable");
		iface = NULL;
		return -ENODEV;
	}

	if (CONFIG_POC_DEST_IPV4[0] != '\0') {
		uint32_t addr;

		if (zsock_inet_pton(AF_INET, CONFIG_POC_DEST_IPV4, &peer.sin_addr) != 1) {
			LOG_ERR("Invalid destination IPv4; transmission disabled");
			return -EINVAL;
		}
		addr = ntohl(peer.sin_addr.s_addr);
		if ((addr >> 24) == 0 || (addr >> 24) == 127 || (addr >> 24) >= 224) {
			LOG_ERR("Destination must be a unicast PC IPv4 address");
			return -EINVAL;
		}
		peer.sin_family = AF_INET;
		peer.sin_port = htons(CONFIG_POC_UDP_PORT);
		destination_set = true;
		LOG_INF("UDP destination %s:%d interval=%d ms", CONFIG_POC_DEST_IPV4,
			CONFIG_POC_UDP_PORT, CONFIG_POC_SEND_INTERVAL_MS);
	} else {
		LOG_WRN("UDP TX disabled: set CONFIG_POC_DEST_IPV4 to the receiver PC");
	}

#if defined(CONFIG_POC_DHCP)
	net_dhcpv4_start(iface);
	LOG_INF("DHCP started (no blocking lease wait)");
#else
	struct in_addr local, mask, gateway;

	if (zsock_inet_pton(AF_INET, CONFIG_POC_LOCAL_IPV4, &local) != 1 ||
	    zsock_inet_pton(AF_INET, CONFIG_POC_NETMASK, &mask) != 1 ||
	    zsock_inet_pton(AF_INET, CONFIG_POC_GATEWAY, &gateway) != 1 ||
	    net_if_ipv4_addr_add(iface, &local, NET_ADDR_MANUAL, 0) == NULL ||
	    !net_if_ipv4_set_netmask_by_addr(iface, &local, &mask)) {
		LOG_ERR("Static IPv4 configuration failed");
		return -EINVAL;
	}
	net_if_ipv4_set_gw(iface, &gateway);
	LOG_INF("Static IPv4 %s mask=%s gateway=%s", CONFIG_POC_LOCAL_IPV4,
		CONFIG_POC_NETMASK, CONFIG_POC_GATEWAY);
#endif
	return 0;
}

void poc_network_tick(void)
{
	struct in_addr *local;
	int state;
	int64_t now = k_uptime_get();

	if (iface == NULL) {
		return;
	}
	local = net_if_ipv4_get_global_addr(iface, NET_ADDR_PREFERRED);
	state = !net_if_is_carrier_ok(iface) ? 0 :
		(!net_if_is_up(iface) || local == NULL ? 1 : 2);
	if (state != last_state) {
		LOG_INF("Network: %s", state == 0 ? "link down" :
			(state == 1 ? "link up, waiting for IPv4" : "link up, IPv4 ready"));
		last_state = state;
	}
	if (state != 2) {
		close_socket();
		last_ipv4 = 0;
		return;
	}
	if (local->s_addr != last_ipv4) {
		char text[NET_IPV4_ADDR_LEN];

		close_socket();
		last_ipv4 = local->s_addr;
		LOG_INF("IPv4 address: %s", net_addr_ntop(AF_INET, local, text, sizeof(text)));
	}
	if (!destination_set || now < next_send) {
		return;
	}
	next_send = now + CONFIG_POC_SEND_INTERVAL_MS;
	if (net_ipv4_is_addr_bcast(iface, &peer.sin_addr)) {
		LOG_ERR("Refusing a subnet broadcast destination");
		return;
	}
	if (udp_socket < 0) {
		udp_socket = zsock_socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
		if (udp_socket < 0) {
			LOG_WRN("socket failed errno=%d; will retry", errno);
			return;
		}
	}
	/* Diagnostic text only, unrelated to future RS-485 industrial framing.
	 * Increment per attempt: a successful send is local acceptance, not delivery.
	 */
	char message[128];
	uint32_t seq = sequence++;
	int length = snprintk(message, sizeof(message),
		"poc=gateway version=" POC_APP_VERSION " seq=%u uptime_ms=%lld\n",
		seq, (long long)now);

	if (length < 0 || (size_t)length >= sizeof(message)) {
		LOG_ERR("Heartbeat formatting exceeded the fixed buffer");
		return;
	}
	int sent = zsock_sendto(udp_socket, message, length, ZSOCK_MSG_DONTWAIT,
			       (const struct sockaddr *)&peer, sizeof(peer));

	if (sent != length) {
		LOG_WRN("UDP send seq=%u failed result=%d errno=%d", seq, sent, errno);
		close_socket();
	} else {
		LOG_INF("UDP seq=%u accepted locally (%d bytes); reception unconfirmed", seq, sent);
	}
}
