if [[ $# != 1 ]]; then
        echo "./ping.sh ip.list"
        exit
fi

if [[ -f ./${1}.alive.txt ]]; then
        rm ./${1}.alive.txt
fi

if [[ -f ./${1}.dead.txt ]]; then
        rm ./${1}.dead.txt
fi

while read host; do
        ping -c2 $host >/dev/null & 2>/dev/null
        if [[ $? = 0 ]]; then
                echo "$host is up."
                echo "$host" >> ./${1}.alive.txt
        else
                echo "$host is down." >> ./${1}.dead.txt
        fi
done<${1}
