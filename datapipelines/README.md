**Deploying datapipelines on KPS**

use KPS cli to deploy the following pipelines:

**scanner_message**

This pipeline will handle scanner message received over MQTT sensor. Message is transposed using read_scanner_function.

`kps create -f scanner-message.yaml`

