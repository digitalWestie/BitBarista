v0.1 Plan: 

Flask: 

GET "/" - js polls "/state", if okay shows offers else shows state

GET "/status" - shows results from various read states

GET "/state" - checks if machine is on and warmed up

GET "/sell/<offer>" - js checks "/state" if not shows state, if ready generates an address, calculates amount for item, renders page w/ qr, js polls blockchain.info for tx for 30 seconds: 

  - On timeout (nothing rcvd): Check for payment again? / Cancel (redirect to "/")
  - On fail (reason: not enough, other?): Check for payment again? / Cancel (redirect to "/")
  - On success (>= amount rcvd): Redirect to "/sell/<offer>/paid?<txparams>"

GET "/sell/<offer>/paid?<txparams>" - returns received msg, polls "/state" showing state, once ready press cof button, polls "/state" again until vending state is over and shows "we're done!" then redirect to "/"

NB- for v0.2 /paid stage will have a cancel & refund option, and a refund for when things go wrong.

v0.2

GET "/refund?txdetails=<txdetails>" - Checks refund hasn't been carried out already then shows "Refunding X to Y", send request to API to refund txdetails:amount to txdetails:address, then polls for result

  - On success: show "done" msg then redirect to "/"
  - On timeout: Show "Try again?"
  - On error: Show "Try again?"

