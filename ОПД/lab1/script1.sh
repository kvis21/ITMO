#!/usr/bin/bash
mkdir lab0
cd ./lab0

echo -e "step 1"

mkdir blitzle6
mkdir blitzle6/exeggutor
mkdir blitzle6/kricketune
mkdir blitzle6/hypno
touch blitzle6/excadrill
touch blitzle6/tyranitar

mkdir magcargo1
mkdir magcargo1/leafeon
mkdir magcargo1/butterfree
touch magcargo1/squirtle
touch magcargo1/liepard

mkdir munna8
mkdir munna8/electrike
mkdir munna8/klink
touch munna8/eelektross
touch munna8/wailmer

touch banette4
touch charmander7
touch lumineon0

echo -e "Возможности Overland=6 Surface=4 Sky=6 Jump=3 Power3=0\nIntelligence=4 Invisibility=0 Phasing=0\nStealth=0" > banette4
echo -e "Возможности Overland=6 Surface=4 Burrow=10\nJump=3 Power=3 Intelligence=4 Groundshaper=0" > blitzle6/excadrill
echo -e "Тип покемона\nROCK_DARK" > blitzle6/tyranitar
echo -e "Ходы Body Slam Counter Defense Curl\nDouble-Edge Dynamicpunch Fire Pledge Fire Punch Fury Cutter Heat Wave\nIron Tail Mega Kick Mega Punch Mud-Slap Outrage Rage Seismic Toss\nSleep Talk Snore Swift Thunderpunch" > charmander7
echo -e "Развитые способности\nWater Veil" > lumineon0
echo -e "Способности TorrentShell Armor Rock\nHead" > magcargo1/squirtle
echo -e "weight=82.7 height=43.0 atk=9 def=5" > magcargo1/liepard
echo -e "Ходы\nAcid\xc7\x82 Aqua Tail Bind Bounce Charge Beam\xc7\x82 Crunch\xc7\x82 Crush Claw\xc7\x82\nDischarge\xc7\x82 Drain Punch Fire Punch Gastro Acid Giga Drain Headbutt\xc7\x82\nIron Tail Knock off Magnet Rise Signal Beam Sleep Talk Snore Spark\xc7\x82\nSuper Fang Superpower Thunder Wave\xc7\x82" > munna8/eelektross
echo -e "Живет Ocean" > munna8/wailmer

echo -e "\nstep 2"
chmod 060 banette4
chmod u=wr,g=r,o= blitzle6/excadrill
chmod 044 blitzle6/tyranitar
chmod u=rw,g=w,o=w charmander7
chmod u=r,g=,o=r lumineon0
chmod 062 magcargo1/squirtle
chmod 060 magcargo1/liepard
chmod 624 munna8/eelektross
chmod 444 munna8/wailmer
chmod u=wx,g=x,o=x blitzle6/exeggutor
chmod u=rx,g=rwx,o=rw blitzle6/kricketune
chmod u=rx,g=rwx,o=wx blitzle6/hypno
chmod 700 magcargo1/butterfree
chmod 753 magcargo1/leafeon
chmod 511 munna8/klink
chmod u=wx,g=rw,o=wx munna8/electrike
chmod 307 blitzle6
chmod 335 magcargo1
chmod 751 munna8

echo -e "\nstep 3"

ln banette4 magcargo1/squirtlebanette
ls -i magcargo1/squirtlebanette
ls -i banette4
ls -i magcargo1/squirtlebanette banette4


cat munna8/eelektross munna8/wailmer > charmander7_60

cat munna8/eelektross
echo -e '\n'
cat munna8/wailmer
echo -e '\n'
cat charmander7_60

chmod 760 banette4
cat banette4 > munna8/eelektrossbanette
cat banette4
echo -e '\n'
cat munna8/elektrossbanette
chmod 060 banette4

ln -s blitzle6 Copy_67
ls -li Copy_67

chmod 763 munna8
ls -lR munna8 #проверка
cp -R munna8 munna8/electrike #команда
ls -lR munna8/electrike/munna8 #проверка
chmod 363 munna8/electrike


cp banette4 munna8/electrike
chmod 763 munna8/electrike
ls munna8/electrike/banette4
chmod 363

cd munna8
ln -s ../lumineon0 eelektrosslumineon
ls -li eelektrosslumineon
cat ../lumineon0
cat eelektrosslumineon
cd ..

echo -e "\nstep 4"
chmod 707 blitzle6
chmod 735 magcargo1
chmod 711 blitzle6/exeggutor
chmod magcargo1/liepard
chmod blitzle6/tyranitar
chmod magcargo1/squirtle
wc -l ./ ./* ./*/* ./*/*/* ./*/*/*/* 2>&1 | grep -v 'Is a directory' | grep '/b' | grep -v '/b.*/[^b]' | sort -nr
#wc -l 2>&1 $(ls -R | grep -ve '\/$\|:$' | grep '^b') | sort -rn
chmod 307 blitzle6
chmod 335 magcargo1
chmod 311 blitzle6/exeggutor

ls -lRT 2>&1 | grep -E ':[0-9][0-9] [0-9]{4} m'  | sort -nk 9 -k7M -nk 6 -nk 8 | tail -n 2

chmod 720 blitzle6/tyranitar magcargo1/squirtle magcargo1/liepard
cat blitzle6/tyranitar magcargo1/squirtle magcargo1/liepard 2>/tmp/2.err | grep -vi 'l$'
chmod 044 blitzle6/tyranitar
chmod 060 magcargo1/squirtle
chmod 062 magcargo1/liepard
#ls -lR 2>&1 | grep ' m' | sort -k 7 | tail -n 2
#ls -lR 2>&1 | grep ' ..... m' | sort -k 7,6
ls -lRT 2>&1 | grep ' m.*\b'  | sort -nk 9 -nk 7 -nk 6 -nk 8 | tail -n 2

ls -laRT | grep ' [0-9][0-9][0-9][0-9] [^ ]*tte' | sort -nk 5

ls -lRT 2>/dev/null | grep ' [0-9][0-9][0-9][0-9] e' | sort -nrk 2 | head -n 4



#dop
ls -Rl | grep -vE "([^ ]+ +){4}0 |^d" | grep -E "([^ ]+ +){7}"| sort -nk5 | head -n 1


