This repo will store work concerning networking within it

Listed projects include:
  1) raspberrypi_car_server and raspberrypi_car_client

1)
These server/client models were applied to multiple Raspberry Pi to simulate swarm communication. A WSN strategy known as [1] Multiple Aggregator Multiple Chain (MAMC) was implemented to split the clients into X regions within which hosts a chaining structure where a node farthest from the base station sends information to the node second farthest from the base station, prompting the second node to send the first node's information alongside its own to the node third farthest from the base station and so on until each unit's data meets the aggregator node, the one closest to the base station within its group. The aggregator node then sends everyone's data to the base station, leaving it for the user to interpret.

This is done for the sake of saving processing power which increases a network's lifespan.

[1] P. Harichandan, A. Jaiswal and S. Kumar, "Multiple Aggregator Multiple Chain routing protocol for heterogeneous wireless sensor networks," 2013 INTERNATIONAL CONFERENCE ON SIGNAL PROCESSING AND COMMUNICATION (ICSC), Noida, India, 2013, pp. 127-131, doi: 10.1109/ICSPCom.2013.6719769. keywords: {Wireless sensor networks;Computational modeling;Routing protocols;Simulation;Routing;Nickel;Multiple Chain;Data Aggregation;Routing;Wireless Sensor Network;Heterogeneity},
