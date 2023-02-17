import os
import subprocess

def writeResults(zone, ergebnisarray, dateiname):
    if os.path.exists(zone + "/" + zone + dateiname):
        with open(zone + "/" + zone + dateiname, "r") as f:
            old_entries = set(f.read().splitlines())

        new_entries = set(ergebnisarray).difference(old_entries)
        if len(new_entries) > 0:
            if not os.path.exists(zone + "/neue_eintraege/"):
                os.mkdir(zone + "/neue_eintraege/")
            with open(zone + "/neue_eintraege/" + zone + dateiname + "_NEU", "w") as f:
                for entry in new_entries:
                    try:
                        f.write(str(entry) + "\n")
                    except:
                        print(str(entry) + " An oopsie whoopsie occured! \n")
    else:
        with open(zone + "/" + zone + dateiname, "w") as f:
            for entry in ergebnisarray:
                try:
                    f.write(str(entry) + "\n")
                except:
                    print(str(entry) + " Funktioniert nicht! \n")

if __name__ == "__main__":
    zonen = os.listdir("zonen/")

    for zone in zonen:
        if not os.path.exists(zone):
            os.mkdir(zone)

    for zone in zonen:

        working = []
        timeouts = []
        notFounds = []
        connectionRefused = []

        with open("zonen/" + zone) as f:
            hosts = f.readlines()

        filteredHosts = []

        for host in hosts:
            if not host.startswith(" ") and not host.startswith("@") and not host.startswith(";") and not host.startswith("_") and not host.startswith("\n"):
                filteredHosts.append(host.split(" ", 1)[0])

        for host in filteredHosts:
            fqdn = host + "." + zone
            print("Test fuer: " + fqdn)
            nc = subprocess.run(["nc", "-vz", "-w", "1" , fqdn , "443"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(nc.stderr)
            if "TIMEOUT" in nc.stderr:
                timeouts.append(fqdn)
            elif nc.returncode == 0:
                working.append(fqdn)
            elif "Connection refused" in nc.stderr:
                connectionRefused.append(fqdn)
            else:
                notFounds.append(fqdn)

        writeResults(zone, working, "_geht.txt")
        writeResults(zone, timeouts, "_timeout.txt")
        writeResults(zone, notFounds, "_notFound.txt")
        writeResults(zone, connectionRefused, "_refused.txt")