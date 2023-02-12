# Simple script with playwright to check the status of a bitwarden container on my docker server.

If the bitwarden container is showing healthy it simply exits, if it shows that it's unhealthy (which seems to happen once a week or so, hence the need for this script) it will restart the bitwarden container and then exit. 
