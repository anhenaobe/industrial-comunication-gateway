#ifndef POC_NETWORK_H
#define POC_NETWORK_H

/* Called only by main; no waits for link, DHCP lease or packet delivery. */
int poc_network_init(void);
void poc_network_tick(void);

#endif
